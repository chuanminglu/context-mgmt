#!/usr/bin/env python3
"""
项目类型检测器
自动检测项目类型和技术栈
"""

from pathlib import Path
from typing import Tuple, List

class ProjectDetector:
    """项目类型检测器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
    
    def detect_project_type(self) -> Tuple[str, float]:
        """
        检测项目类型
        返回: (项目类型, 置信度)
        """
        # Web项目检测
        if self._has_web_indicators():
            return "web_project", 0.9
        
        # Python项目检测
        if self._has_python_indicators():
            return "python_project", 0.9
        
        # Java项目检测
        if self._has_java_indicators():
            return "java_project", 0.9
        
        # Node.js项目检测
        if self._has_nodejs_indicators():
            return "nodejs_project", 0.9
        
        # 数据科学项目检测
        if self._has_datascience_indicators():
            return "datascience_project", 0.8
        
        # 移动应用检测
        if self._has_mobile_indicators():
            return "mobile_project", 0.8
        
        # 文档项目检测
        if self._has_documentation_indicators():
            return "documentation", 0.6
        
        # 基于文件扩展名的简单检测
        if any(self.project_root.glob("*.py")):
            return "python_project", 0.7
        elif any(self.project_root.glob("*.js")):
            return "web_project", 0.7
        elif any(self.project_root.glob("*.java")):
            return "java_project", 0.7
        elif any(self.project_root.glob("*.md")):
            return "documentation", 0.6
        
        return "general", 0.5
    
    def get_tech_stack(self) -> List[str]:
        """获取技术栈列表"""
        tech_stack = []
        
        # 后端技术
        if (self.project_root / "requirements.txt").exists() or any(self.project_root.glob("*.py")):
            tech_stack.append("Python")
        
        if (self.project_root / "package.json").exists():
            tech_stack.append("Node.js")
        
        if (self.project_root / "pom.xml").exists() or any(self.project_root.glob("*.java")):
            tech_stack.append("Java")
        
        if (self.project_root / "Cargo.toml").exists() or any(self.project_root.glob("*.rs")):
            tech_stack.append("Rust")
        
        if (self.project_root / "go.mod").exists() or any(self.project_root.glob("*.go")):
            tech_stack.append("Go")
        
        # 前端技术
        if any(self.project_root.glob("**/*.js")):
            tech_stack.append("JavaScript")
        
        if any(self.project_root.glob("**/*.ts")):
            tech_stack.append("TypeScript")
        
        if any(self.project_root.glob("**/*.vue")):
            tech_stack.append("Vue.js")
        
        if any(self.project_root.glob("**/*.jsx")) or any(self.project_root.glob("**/*.tsx")):
            tech_stack.append("React")
        
        # 数据库
        if any(self.project_root.glob("**/*.db")) or any(self.project_root.glob("**/*.sqlite")):
            tech_stack.append("SQLite")
        
        if (self.project_root / "docker-compose.yml").exists():
            tech_stack.append("Docker")
        
        # 项目结构
        if (self.project_root / "backend").exists():
            tech_stack.append("后端开发")
        
        if (self.project_root / "frontend").exists():
            tech_stack.append("前端开发")
        
        if (self.project_root / "api").exists():
            tech_stack.append("API开发")
        
        return tech_stack or ["通用"]
    
    def _has_web_indicators(self) -> bool:
        """检测Web项目指标"""
        indicators = [
            "package.json",
            "webpack.config.js",
            "vite.config.js",
            "next.config.js",
            "nuxt.config.js"
        ]
        return any((self.project_root / indicator).exists() for indicator in indicators)
    
    def _has_python_indicators(self) -> bool:
        """检测Python项目指标"""
        indicators = [
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "Pipfile",
            "manage.py"  # Django
        ]
        return any((self.project_root / indicator).exists() for indicator in indicators)
    
    def _has_java_indicators(self) -> bool:
        """检测Java项目指标"""
        indicators = [
            "pom.xml",
            "build.gradle",
            "gradle.properties"
        ]
        return any((self.project_root / indicator).exists() for indicator in indicators)
    
    def _has_nodejs_indicators(self) -> bool:
        """检测Node.js项目指标"""
        return (self.project_root / "package.json").exists()
    
    def _has_datascience_indicators(self) -> bool:
        """检测数据科学项目指标"""
        indicators = [
            any(self.project_root.glob("*.ipynb")),  # Jupyter notebooks
            (self.project_root / "environment.yml").exists(),  # Conda
            any(self.project_root.glob("**/data/")),  # 数据目录
            any(self.project_root.glob("**/notebooks/")),  # notebook目录
        ]
        return any(indicators)
    
    def _has_mobile_indicators(self) -> bool:
        """检测移动应用项目指标"""
        indicators = [
            "android/",
            "ios/",
            "pubspec.yaml",  # Flutter
            "App.js",  # React Native
            "app.json"  # Expo
        ]
        return any((self.project_root / indicator).exists() for indicator in indicators)
    
    def _has_documentation_indicators(self) -> bool:
        """检测文档项目指标"""
        md_files = list(self.project_root.glob("*.md"))
        indicators = [
            len(md_files) > 3,
            (self.project_root / "docs/").exists(),
            (self.project_root / "mkdocs.yml").exists(),
            (self.project_root / "_config.yml").exists(),  # Jekyll
            (self.project_root / "conf.py").exists(),  # Sphinx
        ]
        return any(indicators)
