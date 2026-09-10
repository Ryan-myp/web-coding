"""
Skill Runner - Skills 执行引擎
"""
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional


class SkillRunner:
    """Skill 执行器"""
    
    def __init__(self, registry: 'SkillRegistry' = None):
        self.registry = registry
    
    def run_skill(self, skill_name: str, command: str, args: dict = None) -> Dict:
        """运行 Skill 命令"""
        skill = self.registry.get_skill(skill_name) if self.registry else None
        if not skill:
            return {"error": f"Skill not found: {skill_name}"}
        
        skill_path = Path(skill["path"])
        script_path = skill_path / "scripts" / f"{command}.py"
        
        if not script_path.exists():
            # 尝试其他脚本路径
            alt_scripts = [
                skill_path / "scripts" / f"{command}.sh",
                skill_path / "scripts" / "qguard.py",  # code-quality-guard
            ]
            for alt in alt_scripts:
                if alt.exists():
                    script_path = alt
                    break
            else:
                return {"error": f"No script found for command: {command}"}
        
        cmd = ["python3", str(script_path)]
        if args:
            for k, v in args.items():
                cmd.extend([f"--{k}", str(v)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                try:
                    return {"success": True, "result": __import__('json').loads(result.stdout)}
                except:
                    return {"success": True, "result": result.stdout}
            else:
                return {"error": result.stderr}
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_file(self, filepath: str, language: str = "python") -> Dict:
        """分析文件"""
        return self.run_skill("code-quality-guard", "analyze", {
            "path": filepath,
            "language": language
        })
    
    def analyze_directory(self, dirpath: str, language: str = "python") -> Dict:
        """分析目录"""
        return self.run_skill("code-quality-guard", "analyze", {
            "path": dirpath,
            "language": language
        })
    
    def security_check(self, path: str) -> Dict:
        """安全检查"""
        return self.run_skill("code-quality-guard", "security", {"path": path})
    
    def generate_guide(self, intent: str, language: str = "python") -> str:
        """生成代码生成指南"""
        result = self.run_skill("code-quality-guard", "guide", {
            "intent": intent,
            "language": language
        })
        return result.get("result", "")
