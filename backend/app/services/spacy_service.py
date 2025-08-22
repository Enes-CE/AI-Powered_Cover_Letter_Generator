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
        doc = self.nlp(text)
        candidates: List[str] = []

        # 1) Proper noun chunks and nouns
        for token in doc:
            if token.is_stop:
                continue
            if token.lemma_.lower() in self.extra_stop_terms:
                continue
            if token.pos_ in {"PROPN", "NOUN"} and len(token.text) > 2:
                candidates.append(token.text.lower())

        # 2) Noun chunks (multi-word terms)
        for chunk in doc.noun_chunks:
            phrase = chunk.text.strip().lower()
            if len(phrase) > 2 and not all(w.isdigit() for w in phrase.split()):
                candidates.append(phrase)

        # 3) Gazetteer lookup in raw text for common tech skills
        text_lower = text.lower()
        for skill in self.technical_skills:
            if skill in text_lower:
                candidates.append(skill)

        # Normalize and deduplicate
        normalized: List[str] = []
        seen = set()
        for c in candidates:
            c = re.sub(r"\s+", " ", c).strip()
            if c and c not in seen:
                seen.add(c)
                normalized.append(c)
        return normalized

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
            matched = j in cv_set or any(j in s or s in j for s in cv_set)
            confidence = 1.0 if j in cv_set else (0.7 if matched else 0.0)
            evidence = "Direct match" if j in cv_set else ("Partial match" if matched else "")
            matches.append({
                "skill": js,
                "matched": matched,
                "confidence": confidence,
                "cv_evidence": evidence,
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
