#!/usr/bin/env python3
"""
上下文信息生成器
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 常量定义
NO_FEATURES_MSG = "- 暂无功能信息"
NO_CONSTRAINTS_MSG = "- 暂无约束信息"
NO_FILES_MSG = "- 暂无识别到重要文件"
AI_CONTEXT_DIR = ".ai-context"
CONFIG_FILE_NAME = "context-config.json"

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 导入project_detector模块
try:
    from project_detector import ProjectDetector  # type: ignore
except ImportError as e:
    print(f"❌ 错误: 无法导入project_detector模块: {e}")
    print("📍 请确保project_detector.py文件存在于同一目录下")
    print("💡 解决方案:")
    print("   1. 检查 .ai-context/tools/project_detector.py 文件是否存在")
    print("   2. 确保文件内容完整且语法正确")
    print("   3. 如果文件缺失，请重新创建该文件")
    sys.exit(1)

class ContextGenerator:
    def __init__(self, project_root):
        self.project_root = Path(project_root).resolve()  # 确保是绝对路径
        self.ai_context_dir = self.project_root / AI_CONTEXT_DIR
        
        # 读取扫描配置
        self.scanning_config = self._load_scanning_config()
        
    def _load_scanning_config(self):
        """加载扫描配置"""
        default_config = self._get_default_scanning_config()
        
        config_file = self.ai_context_dir / CONFIG_FILE_NAME
        if not config_file.exists():
            return default_config
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return self._merge_scanning_config(default_config, config)
        except (json.JSONDecodeError, FileNotFoundError):
            return default_config
    
    def _get_default_scanning_config(self):
        """获取默认扫描配置"""
        return {
            "max_depth": 3,
            "include_hidden_dirs": False,
            "special_include_dirs": [AI_CONTEXT_DIR],
            "exclude_dirs": ["__pycache__", "node_modules", ".git"],
            "important_extensions": [".py", ".js", ".md", ".json", ".yml", ".yaml", ".sql", ".db", ".html", ".css", ".tsx", ".jsx", ".ts"]
        }
    
    def _merge_scanning_config(self, default_config, config):
        """合并扫描配置"""
        base_scanning_config = config.get('scanning', {})
        
        # 合并默认配置
        for key, value in default_config.items():
            if key not in base_scanning_config:
                base_scanning_config[key] = value
        
        # 应用项目特定配置
        project_type = config.get('project', {}).get('type', 'general')
        project_specific = base_scanning_config.get('project_specific', {})
        
        if project_type in project_specific:
            specific_config = project_specific[project_type]
            for key, value in specific_config.items():
                if key != 'project_specific':  # 避免递归
                    base_scanning_config[key] = value
        
        return base_scanning_config
    
    def generate_context_summary(self):
        """生成简化的上下文总结"""
        detector = ProjectDetector(str(self.project_root))
        proj_type, _ = detector.detect_project_type()  # 使用下划线忽略未使用的变量
        tech_stack = detector.get_tech_stack()
        
        # 读取项目配置信息
        project_info = self._read_project_config()
        
        summary = ["# 项目上下文总结"]
        
        # 基本项目信息
        summary.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append("")
        summary.append("## 项目信息")
        summary.append(f"- 名称: {project_info.get('name', self.project_root.name)}")
        summary.append(f"- 类型: {project_info.get('type', proj_type)}")
        summary.append(f"- 技术栈: {', '.join(project_info.get('tech_stack', tech_stack))}")
        summary.append(f"- 路径: {self.project_root}")
        summary.append("")
        
        # 核心功能
        summary.append("## 核心功能")
        summary.append(self._get_core_features())
        
        # 项目结构与重要文件
        summary.append("## 项目结构与重要文件")
        summary.append(self._get_important_files())
        
        # 最近更新
        summary.append("## 最近更新")
        recent_files = self._get_recently_modified_files()
        summary.extend(self._format_recent_files_with_sessions(recent_files))
        
        # 项目状态（集成手动状态记录）
        summary.append("")
        summary.append("## 项目管理状态")
        project_status = self._get_project_status()
        summary.append(project_status)
        
        # 技术约束
        summary.append("")
        summary.append("## 技术约束")
        summary.append(self._get_technical_constraints())
        
        # 当前开发状态
        summary.append("")
        summary.append("## 当前开发状态")
        summary.append(self._get_development_status())
        
        # 将列表转换为Markdown格式的字符串
        summary_md = "\n".join(summary)
        
        # 保存到缓存
        cache_file = self.ai_context_dir / "cache" / "latest-context.md"
        cache_file.parent.mkdir(exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(summary_md)
        
        return summary_md
    
    def _read_project_config(self):
        """读取项目配置信息"""
        config_file = self.ai_context_dir / CONFIG_FILE_NAME
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('project', {})
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {}
    
    def _get_core_features(self):
        """获取核心功能信息"""
        overview_file = self.ai_context_dir / "docs" / "project-overview.md"
        if not overview_file.exists():
            return NO_FEATURES_MSG
        
        try:
            with open(overview_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return self._extract_section_content(content, "## 核心功能", NO_FEATURES_MSG)
        except FileNotFoundError:
            return NO_FEATURES_MSG
    
    def _extract_section_content(self, content, section_header, default_message):
        """提取指定章节的内容"""
        if section_header not in content:
            return default_message
        
        lines = content.split('\n')
        features = []
        in_section = False
        
        for line in lines:
            if line.startswith(section_header):
                in_section = True
            elif in_section and line.startswith("##"):
                break
            elif in_section and line.strip():
                features.append(line.strip())
        
        return '\n'.join(features[:5]) if features else default_message
    
    def _get_technical_constraints(self):
        """获取技术约束信息"""
        overview_file = self.ai_context_dir / "docs" / "project-overview.md"
        if not overview_file.exists():
            return NO_CONSTRAINTS_MSG
        
        try:
            with open(overview_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return self._extract_section_content(content, "## 技术约束", NO_CONSTRAINTS_MSG)
        except FileNotFoundError:
            return NO_CONSTRAINTS_MSG
    
    def _get_important_files(self):
        """获取重要文件列表"""
        important_files = []
        self._scan_directory(self.project_root, important_files)
        return "\n".join(important_files[:50]) if important_files else NO_FILES_MSG  # 增加到50个文件
    
    def _scan_directory(self, path, important_files, prefix="", current_depth=0):
        """递归扫描目录结构（基于配置）"""
        max_depth = self.scanning_config.get('max_depth', 3)
        if current_depth >= max_depth:
            return
        
        try:
            items = list(path.iterdir())
            dirs = [item for item in items if item.is_dir() and self._is_important_dir(item)]
            files = [item for item in items if item.is_file() and self._is_important_file(item)]
            
            # 添加重要目录
            for directory in sorted(dirs):
                try:
                    important_files.append(f"{prefix}- 📁 {directory.name}/")
                    self._scan_directory(directory, important_files, prefix + "  ", current_depth + 1)
                except UnicodeError:
                    # 如果有编码问题，使用纯文本版本
                    important_files.append(f"{prefix}- [DIR] {directory.name}/")
                    self._scan_directory(directory, important_files, prefix + "  ", current_depth + 1)
            
            # 添加重要文件
            for file_path in sorted(files):
                try:
                    important_files.append(f"{prefix}- 📄 {file_path.name}")
                except UnicodeError:
                    # 如果有编码问题，使用纯文本版本
                    important_files.append(f"{prefix}- [FILE] {file_path.name}")
                        
        except PermissionError:
            pass
        except Exception as e:
            # 添加通用异常处理以诊断问题
            important_files.append(f"{prefix}- [ERROR] 扫描 {path.name} 时出错: {e}")
    
    def _is_important_dir(self, directory):
        """判断是否为重要目录（基于配置）"""
        include_hidden = self.scanning_config.get('include_hidden_dirs', False)
        special_include = self.scanning_config.get('special_include_dirs', [])
        exclude_dirs = self.scanning_config.get('exclude_dirs', [])
        
        # 检查是否在排除列表中
        if directory.name in exclude_dirs:
            return False
        
        # 检查特殊包含目录
        if directory.name in special_include:
            return True
        
        # 检查隐藏目录
        if directory.name.startswith('.'):
            return include_hidden
        
        return True
    
    def _is_important_file(self, file_path):
        """判断是否为重要文件（基于配置）"""
        important_extensions = self.scanning_config.get('important_extensions', [])
        
        # 跳过隐藏文件（除非配置允许）
        if file_path.name.startswith('.'):
            return False
            
        # 检查文件扩展名
        return file_path.suffix.lower() in important_extensions
    
    def _get_recent_changes(self):
        """获取最近变更（改进版）"""
        changes = []
        
        try:
            # 获取最近修改的文件
            recent_files = self._get_recently_modified_files()
            if recent_files:
                changes.extend(self._format_recent_files(recent_files))
            
            # 尝试获取Git历史
            git_history = self._get_git_history()
            if git_history:
                changes.append("\n## Git提交历史:")
                changes.extend(git_history)
            
            if not changes:
                changes.append("- 未发现最近更改")
                
        except Exception as e:
            changes.append(f"- 获取变更信息时出错: {e}")
        
        return "\n".join(changes)
    
    def _get_recently_modified_files(self):
        """获取最近修改的文件列表（基于配置）"""
        recent_config = self._get_recent_files_config()
        days_threshold = recent_config.get('days_threshold', 7)
        max_depth = recent_config.get('max_depth', 3)
        cutoff_time = datetime.now().timestamp() - (days_threshold * 24 * 3600)
        
        recent_files = []
        self._collect_recent_files(self.project_root, recent_files, cutoff_time, max_depth)
        return sorted(recent_files, key=lambda x: x[1], reverse=True)
    
    def _get_recent_files_config(self):
        """获取最近文件配置"""
        recent_config = self.scanning_config
        if 'recent_files' in self.scanning_config:
            config_file = self.ai_context_dir / CONFIG_FILE_NAME
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        full_config = json.load(f)
                        recent_config = full_config.get('recent_files', self.scanning_config)
                except (json.JSONDecodeError, FileNotFoundError, IOError):
                    pass
        return recent_config
    
    def _collect_recent_files(self, path, recent_files, cutoff_time, max_depth, current_depth=0):
        """递归收集最近修改的文件"""
        if current_depth >= max_depth:
            return
            
        try:
            for item in path.iterdir():
                if item.is_dir() and self._is_important_dir(item):
                    self._collect_recent_files(item, recent_files, cutoff_time, max_depth, current_depth + 1)
                elif item.is_file() and self._is_recent_file(item, cutoff_time):
                    rel_path = item.relative_to(self.project_root)
                    recent_files.append((str(rel_path), item.stat().st_mtime))
        except PermissionError:
            pass
    
    def _is_recent_file(self, item, cutoff_time):
        """判断文件是否为最近修改的文件"""
        if item.stat().st_mtime <= cutoff_time:
            return False
        return self._is_important_file(item) or not item.name.startswith('.')
    
    def _format_recent_files(self, recent_files):
        """格式化最近修改的文件列表"""
        changes = ["## 最近修改的文件:"]
        for file_path, mtime in recent_files[:10]:
            mod_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            changes.append(f"- {file_path} ({mod_time})")
        return changes
    
    def _get_git_history(self):
        """获取Git提交历史"""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                capture_output=True, text=True, cwd=self.project_root
            )
            if result.returncode == 0 and result.stdout.strip():
                return [f"- {line}" for line in result.stdout.strip().split('\n')]
        except Exception:
            pass
        return None
    
    def _get_development_status(self):
        """获取当前开发状态"""
        detector = ProjectDetector(str(self.project_root))
        proj_type, _ = detector.detect_project_type()
        
        status_info = []
        
        if proj_type == "context-management-system":
            status_info.extend(self._check_context_system_status())
        else:
            status_info.extend(self._check_traditional_project_status())
        
        # 通用文档检查
        self._check_documentation_status(status_info)
        
        return "\n".join([f"- {info}" for info in status_info]) or "- 项目刚开始"
    
    def _check_context_system_status(self):
        """检查上下文管理系统状态"""
        status_info = []
        
        # 检查核心工具脚本
        status_info.append(self._check_tools_status())
        
        # 检查配置文件
        status_info.append(self._check_config_status())
        
        # 检查VS Code集成
        status_info.append(self._check_vscode_integration())
        
        # 检查模板系统
        status_info.append(self._check_templates_status())
        
        # 检查缓存系统
        status_info.append(self._check_cache_status())
        
        # 检查快速部署脚本
        status_info.append(self._check_deploy_script_status())
        
        return status_info
    
    def _check_tools_status(self):
        """检查工具脚本状态"""
        tools_dir = self.project_root / AI_CONTEXT_DIR / "tools"
        if not tools_dir.exists():
            return "⏳ 核心工具脚本未开始"
        
        tool_files = [f for f in tools_dir.glob("*.py") if f.name != "__init__.py"]
        if tool_files:
            return f"✅ 核心工具脚本 ({len(tool_files)} 个工具)"
        else:
            return "⏳ 核心工具脚本未完成"
    
    def _check_config_status(self):
        """检查配置文件状态"""
        config_file = self.project_root / AI_CONTEXT_DIR / CONFIG_FILE_NAME
        return "✅ 配置系统已完成" if config_file.exists() else "⏳ 配置系统未完成"
    
    def _check_vscode_integration(self):
        """检查VS Code集成状态"""
        vscode_dir = self.project_root / ".vscode"
        if not vscode_dir.exists():
            return "⏳ VS Code集成未开始"
        
        tasks_file = vscode_dir / "tasks.json"
        return "✅ VS Code任务集成完成" if tasks_file.exists() else "⏳ VS Code任务集成未完成"
    
    def _check_templates_status(self):
        """检查模板系统状态"""
        templates_dir = self.project_root / AI_CONTEXT_DIR / "templates"
        if templates_dir.exists() and list(templates_dir.glob("*.md")):
            return "✅ 模板系统已完成"
        else:
            return "⏳ 模板系统未完成"
    
    def _check_cache_status(self):
        """检查缓存系统状态"""
        cache_dir = self.project_root / AI_CONTEXT_DIR / "cache"
        if cache_dir.exists() and list(cache_dir.glob("*.md")):
            return "✅ 缓存系统正常运行"
        else:
            return "⏳ 缓存系统未启用"
    
    def _check_deploy_script_status(self):
        """检查部署脚本状态"""
        deploy_script = self.project_root / "deploy-ai-context.py"
        return "✅ 快速部署脚本完成" if deploy_script.exists() else "⏳ 快速部署脚本未完成"
    
    def _check_traditional_project_status(self):
        """检查传统项目状态"""
        status_info = []
        
        # 检查数据库
        db_files = list(self.project_root.glob("**/*.db"))
        if db_files:
            status_info.append(f"✅ 数据库已创建 ({len(db_files)} 个数据库文件)")
        else:
            status_info.append("⏳ 数据库未创建")
        
        # 检查后端代码
        backend_dir = self.project_root / "backend"
        if backend_dir.exists():
            backend_files = list(backend_dir.glob("**/*.py"))
            if backend_files:
                status_info.append(f"🔧 后端开发中 ({len(backend_files)} 个Python文件)")
            else:
                status_info.append("⏳ 后端代码未开始")
        else:
            status_info.append("⏳ 后端代码未开始")
        
        # 检查前端代码
        frontend_status = self._check_frontend_status()
        status_info.append(frontend_status)
        
        # 检查测试代码
        test_status = self._check_test_status()
        status_info.append(test_status)
        
        return status_info
    
    def _check_frontend_status(self):
        """检查前端代码状态"""
        frontend_dir = self.project_root / "frontend"
        if not frontend_dir.exists():
            return "⏳ 前端代码未开始"
        
        frontend_files = []
        frontend_files.extend(list(frontend_dir.glob("**/*.html")))
        frontend_files.extend(list(frontend_dir.glob("**/*.js")))
        frontend_files.extend(list(frontend_dir.glob("**/*.css")))
        
        if frontend_files:
            return f"🎨 前端开发中 ({len(frontend_files)} 个前端文件)"
        else:
            return "⏳ 前端代码未开始"
    
    def _check_test_status(self):
        """检查测试代码状态"""
        tests_dir = self.project_root / "tests"
        if tests_dir.exists():
            test_files = list(tests_dir.glob("**/*.py"))
            if test_files:
                return f"🧪 测试代码 ({len(test_files)} 个测试文件)"
        return "⏳ 测试代码未编写"
    
    def _check_documentation_status(self, status_info):
        """检查文档状态"""
        doc_files = list(self.project_root.glob("**/*.md"))
        doc_count = len([f for f in doc_files if AI_CONTEXT_DIR not in str(f)])
        if doc_count > 0:
            status_info.append(f"📚 项目文档 ({doc_count} 个文档文件)")
    
    def _get_project_status(self):
        """读取最新的项目状态信息"""
        status_file = self.project_root / AI_CONTEXT_DIR / 'status' / 'latest-status.md'
        
        if not status_file.exists():
            return "暂无项目状态记录"
            
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 提取关键信息
            lines = content.split('\n')
            status_summary = []
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('## 完成的工作'):
                    current_section = 'completed'
                elif line.startswith('## 进行中的任务'):
                    current_section = 'ongoing'
                elif line.startswith('## 待处理问题'):
                    current_section = 'issues'
                elif line.startswith('## 下一步计划'):
                    current_section = 'next'
                elif line.startswith('## 重要说明'):
                    current_section = 'notes'
                elif line.startswith('- [x]') and current_section == 'completed':
                    status_summary.append(f"✅ {line[6:].strip()}")
                elif line.startswith('- [ ]') and current_section == 'ongoing':
                    status_summary.append(f"🔄 {line[6:].strip()}")
                elif line.startswith('1.') and current_section == 'issues':
                    status_summary.append(f"❗ {line[3:].strip()}")
                    
            return '\n'.join(status_summary[:8])  # 限制显示条目
            
        except Exception as e:
            return f"读取项目状态时出错: {e}"
    
    def _get_session_context(self):
        """获取会话上下文信息"""
        try:
            # 导入会话管理器
            session_manager_path = self.ai_context_dir / "tools" / "session-manager.py"
            if not session_manager_path.exists():
                return None
            
            # 动态导入
            import importlib.util
            spec = importlib.util.spec_from_file_location("session_manager", session_manager_path)
            
            if spec is None or spec.loader is None:
                print(f"无法从路径加载模块: {session_manager_path}")
                return None
                
            session_manager_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(session_manager_module)
            
            # 创建会话管理器实例
            manager = session_manager_module.SessionManager(str(self.project_root))
            
            # 获取最近的会话
            recent_sessions = manager.get_recent_sessions(days=7)
            
            return recent_sessions
        except Exception:
            return None
    
    def _format_recent_files_with_sessions(self, recent_files):
        """格式化最近修改的文件列表，包含会话信息"""
        session_context = self._get_session_context()
        
        if not session_context:
            return self._format_recent_files(recent_files)
        
        changes = ["## 最近修改的文件:"]
        sessions_by_time, unassigned_files = self._group_files_by_session(recent_files[:10], session_context)
        
        # 输出按会话分组的文件
        self._append_session_files(changes, sessions_by_time)
        
        # 输出未分配的文件
        self._append_unassigned_files(changes, unassigned_files)
        
        return changes
    
    def _group_files_by_session(self, recent_files, session_context):
        """按会话分组文件"""
        sessions_by_time = {}
        unassigned_files = []
        
        for file_path, mtime in recent_files:
            file_time = datetime.fromtimestamp(mtime)
            session_key = self._find_file_session(file_time, session_context)
            
            if session_key:
                session = next(s for s in session_context if s["session_id"] == session_key)
                if session_key not in sessions_by_time:
                    sessions_by_time[session_key] = {"session": session, "files": []}
                sessions_by_time[session_key]["files"].append((file_path, mtime))
            else:
                unassigned_files.append((file_path, mtime))
        
        return sessions_by_time, unassigned_files
    
    def _find_file_session(self, file_time, session_context):
        """查找文件所属的会话"""
        for session in session_context:
            start_time = datetime.fromisoformat(session["start_time"])
            end_time = datetime.fromisoformat(session["end_time"]) if session.get("end_time") else datetime.now()
            
            if start_time <= file_time <= end_time:
                return session["session_id"]
        return None
    
    def _append_session_files(self, changes, sessions_by_time):
        """添加会话文件到输出"""
        for session_data in sessions_by_time.values():
            session = session_data["session"]
            files = session_data["files"]
            
            time_range = self._format_session_time_range(session)
            status_icon = "🟢" if session["status"] == "active" else "✅"
            changes.append(f"{status_icon} [会话] {session['title']} ({time_range})")
            
            if session.get("description"):
                changes.append(f"   📝 {session['description']}")
            
            for file_path, mtime in sorted(files, key=lambda x: x[1], reverse=True):
                mod_time = datetime.fromtimestamp(mtime).strftime("%H:%M")
                changes.append(f"   - {file_path} ({mod_time})")
            
            changes.append("")
    
    def _format_session_time_range(self, session):
        """格式化会话时间范围"""
        start_time = datetime.fromisoformat(session["start_time"]).strftime("%H:%M")
        if session.get("end_time"):
            end_time = datetime.fromisoformat(session["end_time"]).strftime("%H:%M")
            return f"{start_time}-{end_time}"
        else:
            return f"{start_time}-(进行中)"
    
    def _append_unassigned_files(self, changes, unassigned_files):
        """添加未分配的文件到输出"""
        if unassigned_files:
            changes.append("📄 其他修改:")
            for file_path, mtime in unassigned_files:
                mod_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                changes.append(f"- {file_path} ({mod_time})")

if __name__ == "__main__":
    generator = ContextGenerator(".")
    summary = generator.generate_context_summary()
    
    # 处理 Windows 控制台编码问题
    try:
        print(summary)
    except UnicodeEncodeError:
        # 如果有编码问题，替换所有可能有问题的字符
        safe_summary = summary.replace('📁', '[DIR]').replace('📄', '[FILE]')
        safe_summary = safe_summary.replace('✅', '[OK]').replace('🟢', '[ACTIVE]')
        safe_summary = safe_summary.replace('📝', '[DESC]').replace('⏱️', '[TIME]')
        safe_summary = safe_summary.replace('📋', '[LIST]').replace('🏷️', '[TAG]')
        try:
            print(safe_summary)
        except UnicodeEncodeError:
            # 如果还有问题，输出到文件
            output_file = "context-output.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"上下文已输出到文件: {output_file}")
