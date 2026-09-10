"""
Skill Registry - Skills 注册与管理
"""
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import hashlib


class SkillRegistry:
    """Skills 注册表"""
    
    def __init__(self, registry_path: str = None):
        self.registry_path = Path(registry_path or "~/.web-coding/registry.json").expanduser()
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.skills = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """加载注册表"""
        if self.registry_path.exists():
            try:
                return json.loads(self.registry_path.read_text())
            except:
                return {"skills": [], "installed_at": {}}
        return {"skills": [], "installed_at": {}}
    
    def _save_registry(self):
        """保存注册表"""
        self.registry_path.write_text(json.dumps(self.skills, indent=2, ensure_ascii=False))
    
    def install_skill(self, skill_path: str) -> Dict:
        """安装 Skill"""
        path = Path(skill_path)
        if not path.exists():
            return {"error": f"Path not found: {skill_path}"}
        
        skill_md = path / "SKILL.md"
        if not skill_md.exists():
            return {"error": f"SKILL.md not found: {skill_path}"}
        
        # 解析 SKILL.md 获取元数据
        content = skill_md.read_text()
        name = path.name
        version = "1.0.0"
        description = ""
        
        # 尝试从内容提取描述
        for line in content.split('\n'):
            if line.startswith('description:') or line.startswith('# '):
                description = line.replace('# ', '').replace('description:', '').strip()
                break
        
        skill_info = {
            "name": name,
            "path": str(path),
            "version": version,
            "description": description,
            "installed_at": datetime.now().isoformat(),
            "enabled": True,
            "metadata": self._extract_metadata(path),
        }
        
        # 检查是否已安装
        existing = self._find_skill(name)
        if existing:
            self.skills["skills"][self.skills["skills"].index(existing)] = skill_info
        else:
            self.skills["skills"].append(skill_info)
        
        self._save_registry()
        return {"success": True, "skill": skill_info}
    
    def uninstall_skill(self, name: str) -> Dict:
        """卸载 Skill"""
        skill = self._find_skill(name)
        if not skill:
            return {"error": f"Skill not found: {name}"}
        
        self.skills["skills"].remove(skill)
        self._save_registry()
        return {"success": True}
    
    def list_skills(self) -> List[Dict]:
        """列出所有已安装的 Skills"""
        return self.skills.get("skills", [])
    
    def get_skill(self, name: str) -> Optional[Dict]:
        """获取单个 Skill"""
        return self._find_skill(name)
    
    def _find_skill(self, name: str) -> Optional[Dict]:
        """查找 Skill"""
        for skill in self.skills.get("skills", []):
            if skill.get("name") == name:
                return skill
        return None
    
    def search_skills(self, query: str) -> List[Dict]:
        """搜索 Skills"""
        query = query.lower()
        return [
            s for s in self.skills.get("skills", [])
            if query in s.get("name", "").lower() 
            or query in s.get("description", "").lower()
        ]
    
    def _extract_metadata(self, skill_path: Path) -> Dict:
        """提取 Skill 元数据"""
        metadata = {
            "scripts": [],
            "features": [],
            "languages": [],
        }
        
        # 扫描 scripts 目录
        scripts_dir = skill_path / "scripts"
        if scripts_dir.exists():
            for f in scripts_dir.glob("*.py"):
                metadata["scripts"].append(f.name)
        
        # 扫描 features 目录
        features_dir = skill_path / "features"
        if features_dir.exists():
            for f in features_dir.glob("*.py"):
                metadata["features"].append(f.name)
        
        # 检测支持的语言
        lang_keywords = ["python", "typescript", "go", "java", "rust", "csharp", "php"]
        for kw in lang_keywords:
            if (skill_path / f"{kw}_analyzer.py").exists() or                (skill_path / "scripts" / f"{kw}_analyzer.py").exists():
                metadata["languages"].append(kw)
        
        return metadata
    
    def get_skill_stats(self) -> Dict:
        """获取统计信息"""
        skills = self.list_skills()
        return {
            "total": len(skills),
            "enabled": len([s for s in skills if s.get("enabled")]),
            "by_language": self._count_by_language(skills),
        }
    
    def _count_by_language(self, skills: List[Dict]) -> Dict:
        """按语言统计"""
        counts = {}
        for skill in skills:
            langs = skill.get("metadata", {}).get("languages", [])
            for lang in langs:
                counts[lang] = counts.get(lang, 0) + 1
        return counts


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Skill Registry CLI")
    parser.add_argument("action", choices=["list", "install", "uninstall", "search", "stats"])
    parser.add_argument("target", nargs="?", default=None)
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    registry = SkillRegistry()
    
    if args.action == "list":
        skills = registry.list_skills()
        if args.json:
            print(json.dumps(skills, indent=2))
        else:
            for s in skills:
                status = "✅" if s.get("enabled") else "❌"
                print(f"{status} {s['name']} v{s.get('version', '?')} - {s.get('description', 'N/A')}")
    
    elif args.action == "install":
        if not args.target:
            print("Error: target path required")
            return
        result = registry.install_skill(args.target)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ Installed: {result['skill']['name']}")
    
    elif args.action == "uninstall":
        if not args.target:
            print("Error: skill name required")
            return
        result = registry.uninstall_skill(args.target)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ Uninstalled: {args.target}")
    
    elif args.action == "search":
        if not args.target:
            print("Error: search query required")
            return
        results = registry.search_skills(args.target)
        for r in results:
            print(f"- {r['name']}: {r.get('description', 'N/A')}")
    
    elif args.action == "stats":
        stats = registry.get_skill_stats()
        print(f"Total skills: {stats['total']}")
        print(f"Enabled: {stats['enabled']}")
        print(f"By language: {json.dumps(stats['by_language'], indent=2)}")


if __name__ == "__main__":
    main()
