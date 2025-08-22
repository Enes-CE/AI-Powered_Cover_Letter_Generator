import os
from typing import List, Dict
import httpx
from .ai_service import AiService


class OllamaAiService(AiService):
    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct")
        self.timeout_seconds = float(os.getenv("AI_TIMEOUT", "30"))

    async def _generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 600) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "options": {"temperature": temperature, "num_predict": max_tokens},
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            return data.get("response", "")

    async def summarize_job_posting(self, job_posting_text: str) -> str:
        return await self._generate(f"Summarize this job posting in 3 bullet points:\n{job_posting_text}")

    async def summarize_cv(self, cv_text: str) -> str:
        return await self._generate(f"Summarize this CV in 3 bullet points:\n{cv_text}")

    async def draft_cover_letter(
        self,
        job_info: Dict,
        cv_skills: List[str],
        skill_matches: List[Dict],
        tone: str,
        custom_instructions: str = None,
        variants: int = 1
    ) -> str | List[str]:
        company = job_info.get("company_name", "Company")
        title = job_info.get("position_title", "Role")
        matched = ", ".join([m["skill"] for m in skill_matches if m.get("matched")]) or "relevant skills"
        
        base_prompt = (
            f"Write a {tone} cover letter for the position '{title}' at '{company}'. "
            f"Highlight these matched skills: {matched}. Keep it under 220 words."
        )
        
        if custom_instructions:
            base_prompt += f"\n\nCustom instructions: {custom_instructions}"
        
        if variants == 1:
            return await self._generate(base_prompt, temperature=0.6, max_tokens=700)
        else:
            # Generate multiple variants with different temperatures
            results = []
            temperatures = [0.6, 0.7, 0.8, 0.9, 1.0]
            for i in range(min(variants, len(temperatures))):
                variant_prompt = f"{base_prompt}\n\nVariant {i+1}:"
                result = await self._generate(variant_prompt, temperature=temperatures[i], max_tokens=700)
                results.append(result)
            return results


