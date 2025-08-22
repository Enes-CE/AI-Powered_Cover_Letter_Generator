"""
SpaCy-based NLP service for keyword extraction and text analysis
"""

from typing import List, Dict
import re
import spacy


class SpaCyService:
    """NLP service powered by spaCy"""

    def __init__(self):
        # Load small English model (installed via: python -m spacy download en_core_web_sm)
        self.nlp = spacy.load("en_core_web_sm")
        # Common stop terms in job postings beyond default stop words
        self.extra_stop_terms = {
            "experience",
            "years",
            "required",
            "preferred",
            "skills",
            "knowledge",
            "ability",
            "responsibilities",
            "duties",
            "qualifications",
            "requirements",
        }
        # Technical skills gazetteer for simple string lookup augmentation
        self.technical_skills = {
            "python",
            "java",
            "javascript",
            "typescript",
            "c++",
            "c#",
            "go",
            "rust",
            "php",
            "ruby",
            "react",
            "angular",
            "vue",
            "django",
            "flask",
            "fastapi",
            "spring",
            "express",
            "laravel",
            "mysql",
            "postgresql",
            "mongodb",
            "redis",
            "sqlite",
            "oracle",
            "sql server",
            "aws",
            "azure",
            "gcp",
            "docker",
            "kubernetes",
            "terraform",
            "jenkins",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "nlp",
            "ai",
            "git",
            "jira",
            "confluence",
            "slack",
            "figma",
        }

    def extract_skills_from_text(self, text: str) -> List[str]:
        if not text:
            return []
        
        text_lower = text.lower()
        skills_found = []
        
        # 1) First priority: Look for known technical skills in the text
        for skill in self.technical_skills:
            if skill in text_lower:
                skills_found.append(skill)
        
        # 2) Look for skill patterns like "experience with X", "knowledge of Y", "proficient in Z"
        skill_patterns = [
            r"experience\s+(?:with|in)\s+([a-zA-Z0-9\s\+\#\.]+?)(?:\s|\.|,|$)",
            r"knowledge\s+(?:of|in)\s+([a-zA-Z0-9\s\+\#\.]+?)(?:\s|\.|,|$)",
            r"proficient\s+(?:with|in)\s+([a-zA-Z0-9\s\+\#\.]+?)(?:\s|\.|,|$)",
            r"skilled\s+(?:with|in)\s+([a-zA-Z0-9\s\+\#\.]+?)(?:\s|\.|,|$)",
            r"expertise\s+(?:with|in)\s+([a-zA-Z0-9\s\+\#\.]+?)(?:\s|\.|,|$)",
            r"familiar\s+(?:with|in)\s+([a-zA-Z0-9\s\+\#\.]+?)(?:\s|\.|,|$)",
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                skill = match.strip()
                if len(skill) > 2 and skill not in skills_found:
                    skills_found.append(skill)
        
        # 3) Look for capitalized terms that might be technologies (e.g., React, Python, AWS)
        doc = self.nlp(text)
        for token in doc:
            if (token.is_title or token.is_upper) and len(token.text) > 2:
                skill = token.text.lower()
                # Only add if it looks like a real technology
                if (skill not in skills_found and 
                    skill not in self.extra_stop_terms):
                    skills_found.append(skill)
        
        # 4) Look for multi-word technical terms (e.g., "machine learning", "deep learning")
        text_lower = text.lower()
        multi_word_skills = [
            "machine learning", "deep learning", "artificial intelligence", "data science",
            "web development", "mobile development", "cloud computing", "devops",
            "software engineering", "full stack", "front end", "back end",
            "user experience", "user interface", "database management", "api development"
        ]
        
        for skill in multi_word_skills:
            if skill in text_lower and skill not in skills_found:
                skills_found.append(skill)
        
        # 5) Filter out common non-skill words and clean up skills
        filtered_skills = []
        non_skill_words = {
            # English non-skill words
            "experience", "years", "required", "preferred", "skills", "knowledge", 
            "ability", "responsibilities", "duties", "qualifications", "requirements",
            "team", "work", "project", "development", "software", "application",
            "system", "technology", "platform", "framework", "library", "tool",
            "methodology", "process", "approach", "strategy", "solution", "service",
            "needed", "engineer", "scientist", "developer", "analyst", "manager",
            "machine", "learning", "deep", "data", "analysis", "neural", "networks",
            
            # Turkish non-skill words
            "görev", "tanımı", "şirketin", "için", "ile", "ve", "bu", "bir", "da", "de",
            "gibi", "olarak", "üzerinde", "yazılım", "geliştirici", "deneyim", 
            "konularında", "uzmanım", "arıyoruz", "gerekli", "şart", "yıl", "yıllık",
            "pozisyon", "rol", "sorumluluk", "nitelik", "beceri", "yetenek", "bilgi",
            "uygulama", "sistem", "teknoloji", "platform", "çerçeve", "kütüphane",
            "araç", "metodoloji", "süreç", "yaklaşım", "strateji", "çözüm", "hizmet",
            "mühendis", "geliştirici", "analist", "yönetici", "makine", "öğrenme",
            "derin", "veri", "analiz", "sinir", "ağları", "deneyim", "yıllar",
            "gerekli", "tercih", "yetenekler", "bilgi", "sorumluluk", "görevler",
            "nitelikler", "gereksinimler", "takım", "iş", "proje", "geliştirme"
        }
        
        for skill in skills_found:
            # Clean up the skill
            skill = skill.strip().lower()
            # Remove trailing punctuation and common words
            skill = re.sub(r'[.,;!?]+$', '', skill)
            skill = re.sub(r'\s+(required|needed|preferred|experience|years?)\s*$', '', skill)
            
            # Additional validation for real skills
            is_real_skill = (
                skill not in non_skill_words and 
                len(skill) > 2 and 
                len(skill.split()) <= 3 and  # Max 3 words per skill
                not skill.endswith('.') and
                not skill.isdigit() and  # Not just numbers
                not any(char.isdigit() for char in skill) and  # No numbers in skill names
                skill not in ['ve', 'ile', 'için', 'bu', 'bir', 'da', 'de', 'gibi', 'olarak']
            )
            
            if is_real_skill:
                filtered_skills.append(skill)
        
        return filtered_skills[:10]  # Return top 10 most relevant skills

    def extract_job_info(self, text: str) -> Dict[str, str]:
        if not text:
            return {}
        doc = self.nlp(text)

        # Company name: prefer ORG entities
        company = "Tech Company"
        for ent in doc.ents:
            if ent.label_ == "ORG":
                company = ent.text.strip()
                break

        # Position title: heuristic - first title-like noun chunk or line containing common terms
        position = self._guess_title(text)

        # Experience: regex search
        experience = self._extract_experience_requirement(text)

        return {
            "position_title": position,
            "company_name": company,
            "required_experience": experience,
        }

    def extract_key_requirements(self, text: str) -> List[str]:
        if not text:
            return []
        doc = self.nlp(text)
        indicators = {
            "required",
            "preferred",
            "must have",
            "should have",
            "need",
            "requirements",
            "qualifications",
            "responsibilities",
        }
        reqs: List[str] = []
        for sent in doc.sents:
            sent_lower = sent.text.lower()
            if any(ind in sent_lower for ind in indicators):
                reqs.extend(self.extract_skills_from_text(sent.text))
        # dedupe
        out, seen = [], set()
        for r in reqs:
            if r not in seen:
                seen.add(r)
                out.append(r)
        return out

    def analyze_cv_skills(self, cv_text: str) -> List[str]:
        return self.extract_skills_from_text(cv_text or "")

    def match_skills(self, job_skills: List[str], cv_skills: List[str]) -> List[Dict]:
        cv_set = {s.lower() for s in cv_skills}
        matches: List[Dict] = []
        
        for js in job_skills:
            j = js.lower()
            
            # Check for exact match first
            if j in cv_set:
                matches.append({
                    "skill": js,
                    "matched": True,
                    "confidence": 1.0,
                    "cv_evidence": "Exact match found in CV",
                })
                continue
            
            # Check for partial matches (e.g., "python" matches "python 3.9")
            partial_match = False
            best_match = ""
            for cv_skill in cv_set:
                if j in cv_skill or cv_skill in j:
                    partial_match = True
                    best_match = cv_skill
                    break
            
            if partial_match:
                matches.append({
                    "skill": js,
                    "matched": True,
                    "confidence": 0.8,
                    "cv_evidence": f"Partial match: {best_match}",
                })
            else:
                matches.append({
                    "skill": js,
                    "matched": False,
                    "confidence": 0.0,
                    "cv_evidence": "Not found in CV",
                })
        
        return matches

    def find_missing_skills(self, job_skills: List[str], cv_skills: List[str]) -> List[str]:
        cv_set = {s.lower() for s in cv_skills}
        missing: List[str] = []
        for js in job_skills:
            j = js.lower()
            if not (j in cv_set or any(j in s or s in j for s in cv_set)):
                missing.append(js)
        return missing

    def generate_recommendations(self, skill_matches: List[Dict], missing_skills: List[str]) -> List[str]:
        recs: List[str] = []
        matched_count = sum(1 for m in skill_matches if m["matched"])
        total = len(skill_matches)
        if total and matched_count < total * 0.5:
            recs.append("Highlight your most relevant skills more prominently")
        if missing_skills:
            recs.append("Consider learning: " + ", ".join(missing_skills[:3]))
        return recs

    def _guess_title(self, text: str) -> str:
        doc = self.nlp(text)
        title_keywords = {"engineer", "developer", "scientist", "manager", "analyst", "lead", "architect"}
        for chunk in doc.noun_chunks:
            if any(k in chunk.text.lower() for k in title_keywords):
                return chunk.text.strip()
        return "Software Engineer"

    def _extract_experience_requirement(self, text: str) -> str:
        m = re.search(r"(\d+)[\+]?\s*years?\s*(?:of\s*)?experience", text, flags=re.I)
        if m:
            return f"{m.group(1)}+ years"
        return "3+ years"
