import os
from typing import List, Dict
import httpx
from .ai_service import AiService


class OllamaAiService(AiService):
    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.timeout_seconds = float(os.getenv("AI_TIMEOUT", "60"))

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
        prompt = f"""You are a professional job analyst. Analyze this job posting and extract the key requirements, responsibilities, and skills needed.

Job Posting:
{job_posting_text}

Please provide a concise summary in 3 bullet points focusing on:
1. Key responsibilities
2. Required skills and qualifications  
3. Preferred experience

Summary:"""
        return await self._generate(prompt, temperature=0.3, max_tokens=300)

    async def summarize_cv(self, cv_text: str) -> str:
        prompt = f"""You are a professional CV analyst. Analyze this CV and extract the key qualifications, skills, and experience.

CV:
{cv_text}

Please provide a concise summary in 3 bullet points focusing on:
1. Key skills and qualifications
2. Relevant experience
3. Notable achievements

Summary:"""
        return await self._generate(prompt, temperature=0.3, max_tokens=300)

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
        
        base_prompt = f"""You are a professional cover letter writer. Write a {tone} cover letter for the position '{title}' at '{company}'.

Key requirements:
- Tone: {tone}
- Position: {title}
- Company: {company}
- Highlight these matched skills: {matched}
- Length: Maximum 220 words
- Structure: Professional greeting, 2-3 paragraphs, professional closing

Guidelines:
- Start with a strong opening that shows enthusiasm for the role
- Connect your skills and experience to the job requirements
- Show understanding of the company and role
- End with a call to action for an interview
- Use professional but engaging language

Cover Letter:"""
        
        if custom_instructions:
            base_prompt += f"\n\nAdditional instructions: {custom_instructions}"
        
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


