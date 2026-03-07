import yaml
from pathlib import Path

class SkillLoader:
    def __init__(self, skills_dir: str = "skills/", registry_path: str = "skills_registry.yaml"):
        self.skills_dir = Path(skills_dir)
        self.registry_path = Path(registry_path)

    def load_skills(self) -> list:
        registry = self._load_registry()
        skills = []
        for skill_id in registry.get("skills", []):
            skill_info = self._load_skill_metadata(skill_id)
            if skill_info:
                skills.append(skill_info)
        return skills

    def _load_registry(self) -> dict:
        if not self.registry_path.exists():
            return {"skills": []}
        with open(self.registry_path, "r") as f:
            return yaml.safe_load(f) or {"skills": []}

    def _load_skill_metadata(self, skill_id: str) -> dict:
        skill_path = self.skills_dir / skill_id / "SKILL.md"
        if not skill_path.exists():
            return None

        # Simple metadata extraction (can be improved)
        with open(skill_path, "r") as f:
            content = f.read()
            return {
                "id": skill_id,
                "path": str(skill_path.parent),
                "description": content.split("\n")[0].replace("#", "").strip()
            }

if __name__ == "__main__":
    loader = SkillLoader()
    skills = loader.load_skills()
    print(f"Loaded {len(skills)} skills.")
    for skill in skills:
        print(f" - {skill['id']}: {skill['description']}")
