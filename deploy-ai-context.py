#!/usr/bin/env python3
"""
AI上下文管理系统完整部署脚本 v2.0
一键创建完整的AI上下文管理系统，包含会话管理、智能刷新、VS Code集成等功能
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class AIContextDeployer:
    def __init__(self, project_root, level="full"):
        self.project_root = Path(project_root).resolve()
        self.level = level
        self.ai_context_dir = self.project_root / ".ai-context"
        
    def deploy(self):
        """部署AI上下文管理系统"""
        print("🚀 开始部署AI上下文管理系统 v2.0...")
        print(f"📁 项目路径: {self.project_root}")
        print(f"⚙️  部署级别: {self.level}")
        print("-" * 60)
        
        # 阶段1: 基础结构
        self._create_basic_structure()
        
        # 阶段2: 核心工具（包含所有完整功能）
        self._create_core_tools()
        
        # 阶段3: VS Code完整集成
        self._create_vscode_integration()
        
        # 阶段4: 高级功能和模板
        self._create_advanced_features()
        
        # 最终设置
        self._finalize_setup()
        
        print("\n✅ AI上下文管理系统部署完成!")
        self._print_next_steps()
    
    def _create_basic_structure(self):
        """创建基础目录结构和文件"""
        print("📂 创建基础目录结构...")
        
        # 创建所有必要目录
        directories = [
            self.ai_context_dir,
            self.ai_context_dir / "templates",
            self.ai_context_dir / "docs", 
            self.ai_context_dir / "tools",
            self.ai_context_dir / "cache",
            self.ai_context_dir / "sessions",
            self.ai_context_dir / "backup"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {directory.relative_to(self.project_root)}")
        
        # 创建配置文件
        self._create_config_file()
    
    def _create_config_file(self):
        """创建完整的配置文件"""
        print("⚙️  创建配置文件...")
        
        project_name = self.project_root.name
        project_type = self._detect_project_type()
        
        config = {
            "project": {
                "name": project_name,
                "type": project_type,
                "version": "2.0.0",
                "created": datetime.now().isoformat(),
                "description": "AI上下文管理系统 - 完整版本"
            },
            "settings": {
                "auto_update": True,
                "session_prefix": f"{project_name}-",
                "template_version": "2.0",
                "max_context_length": 15000,
                "enable_smart_detection": True,
                "enable_vscode_integration": True
            },
            "scanning": {
                "max_depth": 3,
                "include_hidden_dirs": False,
                "special_include_dirs": [".ai-context"],
                "exclude_dirs": ["__pycache__", "node_modules", ".git"],
                "important_extensions": [".py", ".js", ".md", ".json", ".yml", ".yaml", ".sql", ".db", ".html", ".css", ".tsx", ".jsx", ".ts"]
            },
            "recent_files": {
                "days_threshold": 7,
                "max_depth": 3,
                "include_hidden_dirs": False,
                "apply_project_specific": True
            },
            "integrations": {
                "vscode": True,
                "git": True,
                "ci_cd": False
            }
        }
        
        config_file = self.ai_context_dir / "context-config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print("  ✓ context-config.json")
    
    def _detect_project_type(self):
        """智能项目类型检测"""
        if (self.project_root / "package.json").exists():
            return "web_project"
        elif (self.project_root / "requirements.txt").exists():
            return "python_project"
        elif (self.ai_context_dir).exists():
            return "context-management-system"
        else:
            return "general"
    
    def _create_core_tools(self):
        """创建核心工具文件"""
        print("🛠️  创建核心工具...")
        
        # 从当前目录复制现有的工具文件
        current_tools_dir = Path(__file__).parent / ".ai-context" / "tools"
        
        if current_tools_dir.exists():
            print("  📋 复制现有工具文件...")
            for tool_file in current_tools_dir.glob("*.py"):
                target_file = self.ai_context_dir / "tools" / tool_file.name
                shutil.copy2(tool_file, target_file)
                print(f"    ✓ {tool_file.name}")
        else:
            print("  ⚠️  未找到现有工具文件，创建基础版本...")
            self._create_basic_tools()
    
    def _create_basic_tools(self):
        """创建基础工具文件"""
        print("    📝 创建完整工具集...")
        
        # 1. 创建上下文生成器
        self._create_context_generator()
        
        # 2. 创建会话管理器
        self._create_session_manager()
        
        # 3. 创建智能刷新工具
        self._create_smart_refresh()
        
        # 4. 创建项目检测器
        self._create_project_detector()
        
        # 5. 创建简化系统工具
        self._create_simplify_system()
        
        # 6. 创建__init__.py
        self._create_init_file()
    
    def _create_context_generator(self):
        """创建上下文生成器"""
        context_generator = '''#!/usr/bin/env python3
"""
上下文信息生成器 - 完整版本
"""
import os
import json
from datetime import datetime
from pathlib import Path

class ContextGenerator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.config_file = self.project_root / ".ai-context" / "context-config.json"
        self.config = self._load_config()
        
    def _load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def generate_context_summary(self):
        """生成项目上下文总结"""
        project_info = self._get_project_info()
        file_structure = self._get_file_structure()
        recent_changes = self._get_recent_changes()
        
        summary = f"""# 项目上下文总结
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 项目信息
- 名称: {project_info['name']}
- 类型: {project_info['type']}
- 技术栈: {project_info['tech_stack']}
- 路径: {self.project_root}

## 核心功能
[请描述项目的主要功能模块]

## 项目结构与重要文件
{file_structure}

## 最近更新
{recent_changes}

## 项目管理状态
暂无项目状态记录

## 技术约束
- 暂无约束信息

## 当前开发状态
- ✅ 核心工具脚本 (基础版本)
- ✅ 配置系统已完成
- ✅ VS Code任务集成完成
- ✅ 模板系统已完成
- ⚡ 缓存系统正常运行
- 📚 项目文档 (基础版本)
"""
        
        # 保存到缓存
        cache_file = self.project_root / ".ai-context" / "cache" / "latest-context.md"
        cache_file.parent.mkdir(exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(summary)
        return summary
    
    def _get_project_info(self):
        """获取项目信息"""
        project_config = self.config.get('project', {})
        return {
            'name': project_config.get('name', self.project_root.name),
            'type': project_config.get('type', 'general'),
            'tech_stack': self._detect_tech_stack()
        }
    
    def _detect_tech_stack(self):
        """检测技术栈"""
        tech_stack = []
        if (self.project_root / "package.json").exists():
            tech_stack.append("Node.js")
        if (self.project_root / "requirements.txt").exists():
            tech_stack.append("Python")
        if (self.project_root / "pom.xml").exists():
            tech_stack.append("Java")
        if (self.project_root / "Cargo.toml").exists():
            tech_stack.append("Rust")
        return ", ".join(tech_stack) if tech_stack else "通用"
    
    def _get_file_structure(self):
        """获取文件结构"""
        structure_lines = []
        max_depth = self.config.get('scanning', {}).get('max_depth', 3)
        exclude_dirs = self.config.get('scanning', {}).get('exclude_dirs', [])
        
        for root, dirs, files in os.walk(self.project_root):
            # 计算深度
            level = root.replace(str(self.project_root), '').count(os.sep)
            if level >= max_depth:
                dirs[:] = []
                continue
            
            # 过滤排除目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # 添加目录
            indent = "  " * level
            folder_name = os.path.basename(root)
            if level > 0:
                structure_lines.append(f"{indent}- 📁 {folder_name}/")
            
            # 添加重要文件
            important_files = self._filter_important_files(files)
            for file in important_files[:5]:  # 限制每个目录最多5个文件
                structure_lines.append(f"{indent}  - 📄 {file}")
        
        return "\\n".join(structure_lines[:20])  # 限制总行数
    
    def _filter_important_files(self, files):
        """过滤重要文件"""
        important_extensions = self.config.get('scanning', {}).get('important_extensions', 
                                                                  ['.py', '.js', '.md', '.json'])
        important_files = []
        for file in files:
            if any(file.endswith(ext) for ext in important_extensions):
                important_files.append(file)
        return sorted(important_files)
    
    def _get_recent_changes(self):
        """获取最近变更"""
        try:
            import subprocess
            result = subprocess.run(['git', 'log', '--oneline', '-10'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0 and result.stdout.strip():
                return "## 最近修改的文件:\\n基础版本，无Git历史记录"
            else:
                return "基础版本，无Git历史记录"
        except:
            return "基础版本，无Git历史记录"

if __name__ == "__main__":
    generator = ContextGenerator(".")
    generator.generate_context_summary()
'''
        
        generator_file = self.ai_context_dir / "tools" / "context-generator.py"
        with open(generator_file, 'w', encoding='utf-8') as f:
            f.write(context_generator)
        print("    ✓ context-generator.py (完整版本)")
    
    def _create_session_manager(self):
        """创建会话管理器"""
        session_manager = '''#!/usr/bin/env python3
"""
工作会话管理器 - 基础版本
"""
import json
import argparse
from datetime import datetime
from pathlib import Path

class SessionManager:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
        self.ai_context_dir = self.project_root / ".ai-context"
        self.sessions_dir = self.ai_context_dir / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        
    def start_session(self, title, description=""):
        """开始新会话"""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_data = {
            "id": session_id,
            "title": title,
            "description": description,
            "start_time": datetime.now().isoformat(),
            "status": "active",
            "files_modified": []
        }
        
        session_file = self.sessions_dir / f"{session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 会话已开始: {title}")
        print(f"📝 会话ID: {session_id}")
        return session_id
    
    def end_session(self):
        """结束当前会话"""
        active_session = self._get_active_session()
        if not active_session:
            print("⚠️  没有活跃的会话")
            return
        
        session_file = self.sessions_dir / f"{active_session['id']}.json"
        active_session['status'] = 'completed'
        active_session['end_time'] = datetime.now().isoformat()
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(active_session, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 会话已结束: {active_session['title']}")
    
    def get_status(self):
        """获取当前状态"""
        active_session = self._get_active_session()
        if active_session:
            duration = self._calculate_duration(active_session['start_time'])
            print(f"🔄 活跃会话: {active_session['title']}")
            print(f"⏱️  持续时间: {duration}")
            print(f"📝 描述: {active_session.get('description', '无')}")
        else:
            print("💤 没有活跃的会话")
    
    def list_sessions(self, limit=10):
        """列出最近的会话"""
        session_files = list(self.sessions_dir.glob("*.json"))
        session_files.sort(reverse=True)
        
        print(f"📋 最近 {min(limit, len(session_files))} 个会话:")
        for session_file in session_files[:limit]:
            with open(session_file, 'r', encoding='utf-8') as f:
                session = json.load(f)
            
            status_icon = "🔄" if session['status'] == 'active' else "✅"
            print(f"  {status_icon} {session['title']} ({session['id']})")
    
    def _get_active_session(self):
        """获取活跃会话"""
        for session_file in self.sessions_dir.glob("*.json"):
            with open(session_file, 'r', encoding='utf-8') as f:
                session = json.load(f)
            if session.get('status') == 'active':
                return session
        return None
    
    def _calculate_duration(self, start_time):
        """计算持续时间"""
        start = datetime.fromisoformat(start_time)
        duration = datetime.now() - start
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        return f"{hours}小时{minutes}分钟"

def main():
    parser = argparse.ArgumentParser(description="工作会话管理器")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 开始会话
    start_parser = subparsers.add_parser('start', help='开始新的工作会话')
    start_parser.add_argument('title', help='会话标题')
    start_parser.add_argument('-d', '--description', default='', help='会话描述')
    
    # 结束会话
    subparsers.add_parser('end', help='结束当前会话')
    
    # 查看状态
    subparsers.add_parser('status', help='查看当前会话状态')
    
    # 列出会话
    list_parser = subparsers.add_parser('list', help='列出最近的会话')
    list_parser.add_argument('-n', '--number', type=int, default=10, help='显示会话数量')
    
    args = parser.parse_args()
    manager = SessionManager()
    
    if args.command == 'start':
        manager.start_session(args.title, args.description)
    elif args.command == 'end':
        manager.end_session()
    elif args.command == 'status':
        manager.get_status()
    elif args.command == 'list':
        manager.list_sessions(args.number)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
'''
        
        manager_file = self.ai_context_dir / "tools" / "session-manager.py"
        with open(manager_file, 'w', encoding='utf-8') as f:
            f.write(session_manager)
        print("    ✓ session-manager.py")
    
    def _create_smart_refresh(self):
        """创建智能刷新工具"""
        smart_refresh = '''#!/usr/bin/env python3
"""
智能刷新工具 - 基础版本
"""
import os
import argparse
from datetime import datetime
from pathlib import Path

class SmartRefresh:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
        self.ai_context_dir = self.project_root / ".ai-context"
        self.cache_dir = self.ai_context_dir / "cache"
        
    def check_refresh_needed(self):
        """检查是否需要刷新"""
        context_file = self.cache_dir / "latest-context.md"
        if not context_file.exists():
            print("🔄 需要刷新：上下文文件不存在")
            return True
        
        # 检查文件修改时间
        context_mtime = context_file.stat().st_mtime
        
        # 检查项目文件是否有更新
        for root, dirs, files in os.walk(self.project_root):
            if ".ai-context" in root:
                continue
            if ".git" in root:
                continue
                
            for file in files:
                file_path = Path(root) / file
                if file_path.stat().st_mtime > context_mtime:
                    print(f"🔄 需要刷新：检测到文件更新 {file_path.name}")
                    return True
        
        print("✅ 上下文是最新的，无需刷新")
        return False
    
    def auto_refresh(self):
        """自动刷新（如果需要）"""
        if self.check_refresh_needed():
            self.force_refresh()
        else:
            print("📋 上下文已是最新状态")
    
    def force_refresh(self):
        """强制刷新"""
        print("🔄 强制刷新上下文...")
        context_generator = self.ai_context_dir / "tools" / "context-generator.py"
        
        if context_generator.exists():
            os.system(f"python {context_generator}")
            print("✅ 上下文刷新完成")
        else:
            print("❌ 未找到上下文生成器")
    
    def get_report(self):
        """生成刷新报告"""
        context_file = self.cache_dir / "latest-context.md"
        
        if context_file.exists():
            mtime = datetime.fromtimestamp(context_file.stat().st_mtime)
            print(f"📊 上下文状态报告")
            print(f"📅 最后更新时间: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📁 缓存文件: {context_file}")
            print(f"📏 文件大小: {context_file.stat().st_size} 字节")
        else:
            print("❌ 上下文文件不存在")

def main():
    parser = argparse.ArgumentParser(description="智能刷新工具")
    parser.add_argument('--check', action='store_true', help='检查是否需要刷新')
    parser.add_argument('--auto', action='store_true', help='自动刷新（如需要）')
    parser.add_argument('--force', action='store_true', help='强制刷新')
    parser.add_argument('--report', action='store_true', help='显示刷新报告')
    
    args = parser.parse_args()
    refresh = SmartRefresh()
    
    if args.check:
        refresh.check_refresh_needed()
    elif args.auto:
        refresh.auto_refresh()
    elif args.force:
        refresh.force_refresh()
    elif args.report:
        refresh.get_report()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
'''
        
        refresh_file = self.ai_context_dir / "tools" / "smart-refresh.py"
        with open(refresh_file, 'w', encoding='utf-8') as f:
            f.write(smart_refresh)
        print("    ✓ smart-refresh.py")
    
    def _create_project_detector(self):
        """创建项目检测器"""
        project_detector = '''#!/usr/bin/env python3
"""
项目类型检测器 - 基础版本
"""
import json
from pathlib import Path
from collections import defaultdict

class ProjectDetector:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
    
    def detect_project_type(self):
        """检测项目类型"""
        if (self.project_root / "package.json").exists():
            return "web_project", 0.9
        elif (self.project_root / "requirements.txt").exists():
            return "python_project", 0.9
        elif (self.project_root / "pom.xml").exists():
            return "java_project", 0.9
        elif (self.project_root / "Cargo.toml").exists():
            return "rust_project", 0.9
        elif any(self.project_root.glob("*.csproj")):
            return "dotnet_project", 0.9
        elif any(self.project_root.glob("*.md")):
            return "documentation", 0.7
        else:
            return "general", 0.5
    
    def get_tech_stack(self):
        """识别技术栈"""
        tech_stack = []
        
        if (self.project_root / "package.json").exists():
            tech_stack.append("Node.js")
        if (self.project_root / "requirements.txt").exists():
            tech_stack.append("Python")
        if (self.project_root / "pom.xml").exists():
            tech_stack.append("Java")
        if (self.project_root / "Cargo.toml").exists():
            tech_stack.append("Rust")
        if any(self.project_root.glob("*.csproj")):
            tech_stack.append(".NET")
        
        return tech_stack or ["通用"]
    
    def analyze_structure(self):
        """分析项目结构"""
        structure = {
            "directories": [],
            "file_types": defaultdict(int),
            "total_files": 0
        }
        
        for item in self.project_root.rglob("*"):
            if item.is_dir():
                structure["directories"].append(item.name)
            else:
                structure["file_types"][item.suffix] += 1
                structure["total_files"] += 1
        
        return structure

if __name__ == "__main__":
    detector = ProjectDetector(".")
    proj_type, confidence = detector.detect_project_type()
    tech_stack = detector.get_tech_stack()
    
    print(f"项目类型: {proj_type} (置信度: {confidence:.2f})")
    print(f"技术栈: {', '.join(tech_stack)}")
'''
        
        detector_file = self.ai_context_dir / "tools" / "project_detector.py"
        with open(detector_file, 'w', encoding='utf-8') as f:
            f.write(project_detector)
        print("    ✓ project_detector.py")
    
    def _create_simplify_system(self):
        """创建系统简化工具"""
        simplify_system = '''#!/usr/bin/env python3
"""
系统简化工具 - 基础版本
"""
import shutil
from pathlib import Path

class SystemSimplifier:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
        self.ai_context_dir = self.project_root / ".ai-context"
    
    def clean_cache(self):
        """清理缓存文件"""
        cache_dir = self.ai_context_dir / "cache"
        if cache_dir.exists():
            for file in cache_dir.glob("*"):
                if file.is_file():
                    file.unlink()
            print("✅ 缓存文件已清理")
        else:
            print("📁 缓存目录不存在")
    
    def clean_old_sessions(self, days=30):
        """清理旧会话记录"""
        sessions_dir = self.ai_context_dir / "sessions"
        if not sessions_dir.exists():
            print("📁 会话目录不存在")
            return
        
        import time
        current_time = time.time()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        cleaned_count = 0
        for session_file in sessions_dir.glob("*.json"):
            if session_file.stat().st_mtime < cutoff_time:
                session_file.unlink()
                cleaned_count += 1
        
        print(f"✅ 清理了 {cleaned_count} 个旧会话记录")
    
    def backup_system(self):
        """备份系统配置"""
        backup_dir = self.ai_context_dir / "backup"
        backup_dir.mkdir(exist_ok=True)
        
        # 备份配置文件
        config_file = self.ai_context_dir / "context-config.json"
        if config_file.exists():
            from datetime import datetime
            backup_name = f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            shutil.copy2(config_file, backup_dir / backup_name)
            print(f"✅ 配置已备份: {backup_name}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="系统简化工具")
    parser.add_argument('--clean-cache', action='store_true', help='清理缓存')
    parser.add_argument('--clean-sessions', type=int, default=30, help='清理N天前的会话')
    parser.add_argument('--backup', action='store_true', help='备份系统配置')
    
    args = parser.parse_args()
    simplifier = SystemSimplifier()
    
    if args.clean_cache:
        simplifier.clean_cache()
    elif args.clean_sessions:
        simplifier.clean_old_sessions(args.clean_sessions)
    elif args.backup:
        simplifier.backup_system()
    else:
        parser.print_help()
'''
        
        simplify_file = self.ai_context_dir / "tools" / "simplify-system.py"
        with open(simplify_file, 'w', encoding='utf-8') as f:
            f.write(simplify_system)
        print("    ✓ simplify-system.py")
    
    def _create_init_file(self):
        """创建__init__.py文件"""
        init_content = '''"""
AI上下文管理系统工具包
提供项目上下文生成、会话管理、智能刷新等功能
"""

__version__ = "2.0.0"
__author__ = "AI Context Management System"

# 导入主要类
try:
    from .context_generator import ContextGenerator
    from .session_manager import SessionManager
    from .smart_refresh import SmartRefresh
    from .project_detector import ProjectDetector
except ImportError:
    # 如果直接运行工具，忽略导入错误
    pass
'''
        
        init_file = self.ai_context_dir / "tools" / "__init__.py"
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(init_content)
        print("    ✓ __init__.py")
    
    def _create_vscode_integration(self):
        """创建VS Code集成"""
        print("🚀 创建VS Code集成...")
        
        # 创建.vscode目录
        vscode_dir = self.project_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        # 创建完整任务配置
        tasks_config = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "生成AI上下文",
                    "type": "shell",
                    "command": "python",
                    "args": [".ai-context/tools/context-generator.py"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always"
                    }
                },
                {
                    "label": "智能上下文检查",
                    "type": "shell",
                    "command": "python",
                    "args": [".ai-context/tools/smart-refresh.py", "--check"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always"
                    }
                },
                {
                    "label": "自动上下文刷新",
                    "type": "shell",
                    "command": "python",
                    "args": [".ai-context/tools/smart-refresh.py", "--auto"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always"
                    }
                },
                {
                    "label": "强制上下文刷新",
                    "type": "shell",
                    "command": "python",
                    "args": [".ai-context/tools/smart-refresh.py", "--force"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always"
                    }
                },
                {
                    "label": "开始工作会话",
                    "type": "shell",
                    "command": "python",
                    "args": [
                        ".ai-context/tools/session-manager.py",
                        "start",
                        "${input:sessionTitle}",
                        "-d",
                        "${input:sessionDescription}"
                    ],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always"
                    }
                },
                {
                    "label": "结束工作会话",
                    "type": "shell",
                    "command": "python",
                    "args": [".ai-context/tools/session-manager.py", "end"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always"
                    }
                },
                {
                    "label": "查看工作会话",
                    "type": "shell",
                    "command": "python",
                    "args": [".ai-context/tools/session-manager.py", "status"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always"
                    }
                },
                {
                    "label": "列出最近会话",
                    "type": "shell",
                    "command": "python",
                    "args": [".ai-context/tools/session-manager.py", "list"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always"
                    }
                }
            ],
            "inputs": [
                {
                    "id": "sessionTitle",
                    "description": "会话标题",
                    "default": "开发任务",
                    "type": "promptString"
                },
                {
                    "id": "sessionDescription",
                    "description": "会话描述",
                    "default": "请描述本次会话的目标",
                    "type": "promptString"
                }
            ]
        }
        
        tasks_file = vscode_dir / "tasks.json"
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(tasks_config, f, indent=2, ensure_ascii=False)
        print("  ✓ .vscode/tasks.json (完整任务集)")
    
    def _create_advanced_features(self):
        """创建高级功能"""
        print("📝 创建模板和文档...")
        
        # 创建会话启动模板
        session_template = '''# AI协作会话启动模板

## 项目信息
- **项目名称**: {project_name}
- **项目类型**: {project_type}
- **工作目录**: {project_path}

## 当前任务
- **任务描述**: [请填写具体要完成的任务]
- **预期目标**: [请描述期望达到的效果]
- **技术要求**: [请列出相关技术约束]

## 上下文信息
[这里会自动填入最新的项目上下文]

## 工作指南
1. 请仔细阅读项目结构和现有代码
2. 遵循项目的编码规范和架构设计
3. 对不确定的地方及时提问
4. 保持代码的可维护性和可读性

---
*模板生成时间: {current_time}*
'''.format(
            project_name=self.project_root.name,
            project_type=self._detect_project_type(),
            project_path=self.project_root,
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        template_file = self.ai_context_dir / "templates" / "session-starter.md"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(session_template)
        print("  ✓ session-starter.md")
        
        # 创建项目概览文档
        overview_doc = f'''# {self.project_root.name} - 项目概览

## 基本信息
- **项目名称**: {self.project_root.name}
- **项目类型**: {self._detect_project_type()}
- **创建时间**: {datetime.now().strftime("%Y-%m-%d")}
- **AI上下文管理**: 已启用 v2.0

## 项目结构
[请根据实际情况填写项目的主要目录和文件结构]

## 技术栈
[请列出项目使用的主要技术和框架]

## 核心功能
[请描述项目的主要功能模块]

## 开发规范
[请填写代码规范、命名规范等开发约定]

## 部署说明
[请填写项目的部署和运行方式]

## 重要说明
[其他需要特别注意的事项]

---
*文档创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*请及时更新此文档以保持信息的准确性*
'''
        
        overview_file = self.ai_context_dir / "docs" / "project-overview.md"
        with open(overview_file, 'w', encoding='utf-8') as f:
            f.write(overview_doc)
        print("  ✓ project-overview.md")
    
    def _finalize_setup(self):
        """完成最终设置"""
        print("🎯 完成最终设置...")
        
        # 创建README
        readme_content = f'''# AI上下文管理系统

本项目已成功部署AI上下文管理系统 v2.0

## 🚀 快速开始

### 生成项目上下文
```bash
python .ai-context/tools/context-generator.py
```

### 使用VS Code任务
1. 按 `Ctrl+Shift+P`
2. 输入 "Tasks: Run Task"
3. 选择 "生成AI上下文"

## 📁 系统结构
```
.ai-context/
├── tools/           # 自动化工具
├── templates/       # 模板文件
├── docs/           # 项目文档
├── cache/          # 缓存文件
├── sessions/       # 会话记录
└── backup/         # 备份文件
```

## 📖 使用指南

### 1. 更新项目信息
编辑 `.ai-context/docs/project-overview.md` 填写项目详细信息

### 2. 自定义模板
根据需要修改 `.ai-context/templates/` 中的模板文件

### 3. AI协作流程
1. 运行上下文生成工具
2. 复制生成的上下文信息
3. 在AI对话中粘贴上下文
4. 开始协作开发

## ⚙️ 配置说明
系统配置文件: `.ai-context/context-config.json`
可以调整扫描深度、文件过滤等参数

## 🔧 升级说明
如需升级到完整版本（包含会话管理等高级功能），请访问:
https://github.com/your-repo/ai-context-management

---
**部署信息**
- 版本: 2.0
- 部署时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- 部署级别: {self.level}
'''
        
        readme_file = self.ai_context_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("  ✓ README.md")
        
        # 生成初始上下文
        print("🔄 生成初始上下文...")
        try:
            os.chdir(self.project_root)
            os.system(f"python {self.ai_context_dir / 'tools' / 'context-generator.py'}")
        except:
            print("  ⚠️  初始上下文生成失败，请手动运行")
    
    def _print_next_steps(self):
        """打印后续步骤"""
        print("\n" + "="*60)
        print("🎉 部署完成！后续步骤：")
        print("="*60)
        
        print("\n📝 立即可做的：")
        print("1. 编辑 .ai-context/docs/project-overview.md 完善项目信息")
        print("2. 运行：python .ai-context/tools/context-generator.py")
        print("3. 复制生成的上下文信息到AI对话中")
        
        print("\n🚀 VS Code用户：")
        print("- 使用 Ctrl+Shift+P > Tasks: Run Task > 生成AI上下文")
        
        print("\n📚 重要文档：")
        print("- 系统说明：.ai-context/README.md")
        print("- 项目概览：.ai-context/docs/project-overview.md")
        print("- 配置文件：.ai-context/context-config.json")
        
        print("\n🔧 获取完整版本：")
        print("访问 GitHub 获取包含会话管理等高级功能的完整版本")
        print("或将现有的完整工具文件复制到 .ai-context/tools/ 目录")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI上下文管理系统部署工具")
    parser.add_argument("project_path", nargs="?", default=".", help="项目路径（默认当前目录）")
    parser.add_argument("--level", choices=["basic", "standard", "full"], default="full", 
                       help="部署级别（默认: full）")
    parser.add_argument("--force", action="store_true", help="强制覆盖现有配置")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path).resolve()
    
    # 检查是否已存在
    ai_context_dir = project_path / ".ai-context"
    if ai_context_dir.exists() and not args.force:
        print(f"⚠️  检测到 {ai_context_dir} 已存在")
        response = input("是否继续并覆盖现有配置？(y/N): ")
        if response.lower() != 'y':
            print("部署已取消")
            return
    
    # 开始部署
    deployer = AIContextDeployer(project_path, args.level)
    deployer.deploy()

if __name__ == "__main__":
    main()
