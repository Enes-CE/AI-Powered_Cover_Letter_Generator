from __future__ import annotations

from typing import Protocol, List, Dict


class AiService(Protocol):
    async def summarize_job(self, text: str) -> str: ...
    async def summarize_cv(self, text: str) -> str: ...
    async def draft_cover_letter(
        self,
        job_info: Dict[str, str],
        cv_skills: List[str],
        skill_matches: List[Dict],
        tone: str,
    ) -> str: ...


