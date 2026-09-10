#!/usr/bin/env python3
"""
Auto Install - 自动安装 Skills
"""
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import shutil


class AutoInstaller:
    """自动安装器"""
    
    def __init__(self, config_path: str = None):
        self.config_path = Path(config_path or "~/.web-coding/skills_config.json").expanduser()
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_path.exists():
            try:
                return json.loads(self.config_path.read_text())
            except:
                pass
        return {"default_skills": [], "paths": {}}
    
    def _save_config(self):
        """保存配置"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, indent=2))
    
    def install_from_github(self, repo_url: str, skill_path: str = None, target_dir: str = None) -> Dict:
        """从 GitHub 安装 Skill"""
        # 克隆仓库
        clone_path = Path(target_dir or "~/.web-coding/repos").expanduser() / Path(repo_url).stem
        clone_path.mkdir(parents=True, exist_ok=True)
        
        if not (clone_path / ".git").exists():
            result = subprocess.run(
                ["git", "clone", repo_url, str(clone_path)],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                return {"error": f"Git clone failed: {result.stderr}"}
        
        # 复制 skill 到目标位置
        source = clone_path / skill_path if skill_path else clone_path
        target = Path(target_dir or "~/.agents/skills").expanduser() / source.name
        
        if source.exists():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)
            
            return {
                "success": True,
                "skill_name": source.name,
                "path": str(target),
                "message": f"Installed to {target}"
            }
        else:
            return {"error": f"Source not found: {source}"}
    
    def install_default_skills(self) -> List[Dict]:
        """安装默认 Skills"""
        results = []
        for skill in self.config.get("default_skills", []):
            if skill.get("enabled", True):
                result = self.install_from_github(
                    skill["source"],
                    skill.get("path_in_repo"),
                    skill.get("target_dir")
                )
                results.append(result)
        return results
    
    def list_available_skills(self) -> List[Dict]:
        """列出可安装的 Skills"""
        return self.config.get("default_skills", [])


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Auto Install Skills")
    parser.add_argument("action", choices=["install", "list", "default"])
    parser.add_argument("--repo", help="GitHub repo URL")
    parser.add_argument("--path", help="Path in repo")
    args = parser.parse_args()
    
    installer = AutoInstaller()
    
    if args.action == "list":
        for skill in installer.list_available_skills():
            status = "✅" if skill.get("enabled") else "❌"
            print(f"{status} {skill['name']}: {skill.get('description', '')}")
    
    elif args.action == "default":
        results = installer.install_default_skills()
        for r in results:
            if "error" in r:
                print(f"❌ {r['error']}")
            else:
                print(f"✅ {r['skill_name']} installed to {r['path']}")
    
    elif args.action == "install":
        if not args.repo:
            print("Error: --repo required")
            return
        result = installer.install_from_github(args.repo, args.path)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ {result['skill_name']} installed to {result['path']}")


if __name__ == "__main__":
    main()
