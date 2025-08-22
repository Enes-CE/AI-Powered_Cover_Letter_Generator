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
        years_exp = job_info.get("years_of_experience", "")
        achievements = job_info.get("key_achievements", "")
        matched = ", ".join([m["skill"] for m in skill_matches if m.get("matched")]) or "relevant skills"
        
        # Detect language from job posting and CV
        job_text = job_info.get("job_posting_text", "")
        cv_text = job_info.get("cv_text", "")
        
        # Enhanced language detection
        turkish_words = ["ve", "ile", "için", "bu", "bir", "da", "de", "gibi", "olarak", "üzerinde", "yazılım", "geliştirici", "deneyim", "konularında", "uzmanım", "arıyoruz", "gerekli", "şart"]
        english_words = ["the", "and", "with", "for", "this", "a", "an", "in", "on", "at", "software", "developer", "experience", "skills", "required", "looking", "need"]
        
        turkish_count = sum(1 for word in turkish_words if word in job_text.lower() or word in cv_text.lower())
        english_count = sum(1 for word in english_words if word in job_text.lower() or word in cv_text.lower())
        
        is_turkish = turkish_count > english_count
        
        if is_turkish:
            base_prompt = f"""Sen profesyonel bir ön yazı yazarısın. '{company}' şirketindeki '{title}' pozisyonu için {tone} bir ön yazı yaz.

İŞ İLANI:
{job_info.get('job_posting_text', '')}

CV BİLGİLERİ:
{job_info.get('cv_text', '')}

Temel gereksinimler:
- Ton: {tone}
- Pozisyon: {title}
- Şirket: {company}
- Bu eşleşen yetenekleri vurgula: {matched}
- Uzunluk: Maksimum 250 kelime
- Yapı: Profesyonel selamlama, 2-3 paragraf, profesyonel kapanış

Dahil edilecek ek bağlam:
{f"- Deneyim yılı: {years_exp}" if years_exp else ""}
{f"- Ana başarılar: {achievements}" if achievements else ""}

Yönergeler:
- İş ilanındaki spesifik gereksinimlere odaklan
- CV'deki gerçek deneyimleri ve başarıları kullan
- Role olan heyecanını gösteren güçlü bir açılışla başla
- Yeteneklerini ve deneyimini iş gereksinimleriyle bağla
- Şirket ve rol hakkında anlayış göster
- Verilen başarıları ve deneyimi detaylı şekilde dahil et
- Mülakat için bir çağrı ile bitir
- Profesyonel ama etkileyici dil kullan
- Her seferinde farklı bir yaklaşım kullan
- Kişisel ve özgün ol

Ön Yazı:"""
        else:
            base_prompt = f"""You are a professional cover letter writer. Write a {tone} cover letter for the position '{title}' at '{company}'.

JOB POSTING:
{job_info.get('job_posting_text', '')}

CV INFORMATION:
{job_info.get('cv_text', '')}

Key requirements:
- Tone: {tone}
- Position: {title}
- Company: {company}
- Highlight these matched skills: {matched}
- Length: Maximum 250 words
- Structure: Professional greeting, 2-3 paragraphs, professional closing

Additional context to include:
{f"- Years of experience: {years_exp}" if years_exp else ""}
{f"- Key achievements: {achievements}" if achievements else ""}

Guidelines:
- Focus on specific requirements from the job posting
- Use real experiences and achievements from the CV
- Start with a strong opening that shows enthusiasm for the role
- Connect your skills and experience to the job requirements
- Show understanding of the company and role
- Include provided achievements and experience in detail
- End with a call to action for an interview
- Use professional but engaging language
- Use a different approach each time
- Be personal and unique

Cover Letter:"""
        
        if custom_instructions:
            base_prompt += f"\n\nAdditional instructions: {custom_instructions}"
        
        if variants == 1:
            return await self._generate(base_prompt, temperature=0.6, max_tokens=700)
        else:
            # Generate multiple variants with different approaches
            results = []
            
            # Different temperature and prompt variations for more diverse results
            variations = [
                {"temp": 0.7, "suffix": "Lütfen başarıları ve somut sonuçları vurgula." if is_turkish else "Please emphasize achievements and concrete results."},
                {"temp": 0.8, "suffix": "Lütfen şirket değerleri ve kültürüne odaklan." if is_turkish else "Please focus on company values and culture."},
                {"temp": 0.9, "suffix": "Lütfen yaratıcı bir açılış ve benzersiz bir yaklaşım kullan." if is_turkish else "Please use a creative opening and unique approach."},
                {"temp": 0.75, "suffix": "Lütfen teknik yetenekleri ve problem çözme becerilerini öne çıkar." if is_turkish else "Please highlight technical skills and problem-solving abilities."},
                {"temp": 0.85, "suffix": "Lütfen liderlik deneyimi ve takım çalışmasını vurgula." if is_turkish else "Please emphasize leadership experience and teamwork."}
            ]
            
            for i in range(min(variants, len(variations))):
                variant_prompt = f"{base_prompt}\n\n{variations[i]['suffix']}"
                result = await self._generate(variant_prompt, temperature=variations[i]['temp'], max_tokens=700)
                results.append(result)
            
            return results


