"""
NLP Service for keyword extraction and text analysis
"""

import re
import nltk
from typing import List, Dict, Tuple
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('chunkers/maxent_ne_chunker')
except LookupError:
    nltk.download('maxent_ne_chunker')

try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

class NLPService:
    """NLP service for text analysis and keyword extraction"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        # Add common job-related stop words
        self.stop_words.update([
            'experience', 'years', 'required', 'preferred', 'skills', 'knowledge',
            'ability', 'responsibilities', 'duties', 'qualifications', 'requirements'
        ])
        
        # Common technical skills and keywords
        self.technical_skills = {
            'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'php', 'ruby'],
            'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring', 'express', 'laravel'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'ml_ai': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'nlp', 'ai'],
            'tools': ['git', 'jira', 'confluence', 'slack', 'figma', 'adobe', 'photoshop']
        }
        
        # Job titles and positions
        self.job_titles = [
            'software engineer', 'developer', 'programmer', 'data scientist', 'analyst',
            'manager', 'lead', 'architect', 'consultant', 'specialist', 'coordinator'
        ]
        
        # Company indicators
        self.company_indicators = [
            'inc', 'corp', 'llc', 'ltd', 'company', 'enterprises', 'solutions', 'technologies'
        ]
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        if not text:
            return []
        
        text = text.lower()
        extracted_skills = []
        
        # Extract skills from technical_skills dictionary
        for category, skills in self.technical_skills.items():
            for skill in skills:
                if skill in text:
                    extracted_skills.append(skill)
        
        # Extract additional skills using POS tagging
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        
        # Look for nouns and proper nouns that might be skills
        for word, tag in pos_tags:
            if tag.startswith('NN') and len(word) > 2 and word.lower() not in self.stop_words:
                # Check if it looks like a technical term
                if self._is_technical_term(word):
                    extracted_skills.append(word.lower())
        
        return list(set(extracted_skills))  # Remove duplicates
    
    def extract_job_info(self, text: str) -> Dict[str, str]:
        """Extract job information from posting"""
        if not text:
            return {}
        
        text_lower = text.lower()
        
        # Extract job title
        job_title = self._extract_job_title(text)
        
        # Extract company name
        company_name = self._extract_company_name(text)
        
        # Extract experience requirements
        experience = self._extract_experience_requirement(text)
        
        return {
            'position_title': job_title,
            'company_name': company_name,
            'required_experience': experience
        }
    
    def extract_key_requirements(self, text: str) -> List[str]:
        """Extract key requirements from job posting"""
        if not text:
            return []
        
        requirements = []
        sentences = sent_tokenize(text)
        
        # Look for sentences that contain requirement indicators
        requirement_indicators = [
            'required', 'preferred', 'must have', 'should have', 'need', 'looking for',
            'candidate should', 'applicant must', 'requirements', 'qualifications'
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(indicator in sentence_lower for indicator in requirement_indicators):
                # Extract skills from this sentence
                skills = self.extract_skills_from_text(sentence)
                requirements.extend(skills)
        
        return list(set(requirements))
    
    def analyze_cv_skills(self, cv_text: str) -> List[str]:
        """Analyze CV and extract skills"""
        if not cv_text:
            return []
        
        return self.extract_skills_from_text(cv_text)
    
    def match_skills(self, job_skills: List[str], cv_skills: List[str]) -> List[Dict]:
        """Match job skills with CV skills"""
        matches = []
        
        for job_skill in job_skills:
            matched = False
            confidence = 0.0
            evidence = ""
            
            # Direct match
            if job_skill.lower() in [skill.lower() for skill in cv_skills]:
                matched = True
                confidence = 1.0
                evidence = f"Direct match: {job_skill}"
            
            # Partial match
            elif any(job_skill.lower() in skill.lower() or skill.lower() in job_skill.lower() 
                    for skill in cv_skills):
                matched = True
                confidence = 0.7
                evidence = f"Partial match: {job_skill}"
            
            # Category match (e.g., if job asks for "python" and CV has "programming")
            elif self._check_category_match(job_skill, cv_skills):
                matched = True
                confidence = 0.5
                evidence = f"Category match: {job_skill}"
            
            matches.append({
                'skill': job_skill,
                'matched': matched,
                'confidence': confidence,
                'cv_evidence': evidence
            })
        
        return matches
    
    def find_missing_skills(self, job_skills: List[str], cv_skills: List[str]) -> List[str]:
        """Find skills that are required but missing from CV"""
        cv_skills_lower = [skill.lower() for skill in cv_skills]
        missing = []
        
        for job_skill in job_skills:
            if not any(job_skill.lower() in skill or skill in job_skill.lower() 
                      for skill in cv_skills_lower):
                missing.append(job_skill)
        
        return missing
    
    def generate_recommendations(self, skill_matches: List[Dict], missing_skills: List[str]) -> List[str]:
        """Generate recommendations based on skill analysis"""
        recommendations = []
        
        # Count matched skills
        matched_count = sum(1 for match in skill_matches if match['matched'])
        total_count = len(skill_matches)
        
        if matched_count < total_count * 0.5:
            recommendations.append("Consider highlighting your most relevant skills more prominently")
        
        if missing_skills:
            recommendations.append(f"Consider learning or gaining experience in: {', '.join(missing_skills[:3])}")
        
        # Specific recommendations based on missing skills
        for skill in missing_skills[:2]:
            if 'python' in skill.lower():
                recommendations.append("Python is highly valued - consider taking a Python course")
            elif 'react' in skill.lower() or 'javascript' in skill.lower():
                recommendations.append("Frontend development skills are in demand - consider learning React/JavaScript")
            elif 'machine learning' in skill.lower() or 'ai' in skill.lower():
                recommendations.append("AI/ML skills are trending - consider learning basic machine learning concepts")
        
        return recommendations
    
    def _is_technical_term(self, word: str) -> bool:
        """Check if a word looks like a technical term"""
        # Check for camelCase, PascalCase, or contains numbers
        if re.search(r'[A-Z][a-z]|[0-9]', word):
            return True
        
        # Check if it's in our technical skills
        word_lower = word.lower()
        for skills in self.technical_skills.values():
            if word_lower in skills:
                return True
        
        return False
    
    def _extract_job_title(self, text: str) -> str:
        """Extract job title from text"""
        # Look for common job title patterns
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            for title in self.job_titles:
                if title in line_lower:
                    return line.strip()
        
        return "Software Engineer"  # Default
    
    def _extract_company_name(self, text: str) -> str:
        """Extract company name from text"""
        # Simple extraction - look for company indicators
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            for indicator in self.company_indicators:
                if indicator in line_lower:
                    return line.strip()
        
        return "Tech Company"  # Default
    
    def _extract_experience_requirement(self, text: str) -> str:
        """Extract experience requirement from text"""
        # Look for experience patterns
        experience_patterns = [
            r'(\d+)[\+]?\s*years?\s*experience',
            r'experience.*?(\d+)[\+]?\s*years?',
            r'(\d+)[\+]?\s*years?\s*in',
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text.lower())
            if match:
                years = match.group(1)
                return f"{years}+ years"
        
        return "3+ years"  # Default
    
    def _check_category_match(self, job_skill: str, cv_skills: List[str]) -> bool:
        """Check if job skill matches any CV skill category"""
        job_skill_lower = job_skill.lower()
        
        # Check if job skill is in any category that CV skills belong to
        for category, skills in self.technical_skills.items():
            if job_skill_lower in skills:
                # Check if CV has any skill from this category
                for cv_skill in cv_skills:
                    if cv_skill.lower() in skills:
                        return True
        
        return False
