"""
Skill Registry - Skills 注册与管理
"""
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


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
        self.registry_path.write_text(json.dumps(self.skills, indent=2))
    
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
