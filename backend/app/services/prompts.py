def build_cover_letter_prompt(job_info, cv_skills, skill_matches, tone: str) -> str:
    company = job_info.get("company_name", "Company")
    title = job_info.get("position_title", "Role")
    matched = ", ".join([m["skill"] for m in skill_matches if m.get("matched")]) or "relevant skills"
    return (
        f"Write a {tone} cover letter for '{title}' at '{company}'. "
        f"Emphasize: {matched}. Keep under 220 words, fluent English."
    )


