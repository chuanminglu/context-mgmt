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
        self.ai_context_dir = self.project_root / ".ai-context"
        
    def generate_context_summary(self):
        """生成简化的上下文总结"""
        detector = ProjectDetector(self.project_root)
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
        summary.extend(self._format_recent_files(recent_files))
        
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
        config_file = self.ai_context_dir / "context-config.json"
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
        return "\n".join(important_files[:25]) if important_files else NO_FILES_MSG
    
    def _scan_directory(self, path, important_files, prefix="", max_depth=2, current_depth=0):
        """递归扫描目录结构"""
        if current_depth >= max_depth:
            return
        
        try:
            items = list(path.iterdir())
            dirs = [item for item in items if item.is_dir() and self._is_important_dir(item)]
            files = [item for item in items if item.is_file() and self._is_important_file(item)]
            
            # 添加重要目录
            for directory in sorted(dirs):
                important_files.append(f"{prefix}- 📁 {directory.name}/")
                self._scan_directory(directory, important_files, prefix + "  ", max_depth, current_depth + 1)
            
            # 添加重要文件
            for file_path in sorted(files):
                important_files.append(f"{prefix}- 📄 {file_path.name}")
                        
        except PermissionError:
            pass
    
    def _is_important_dir(self, directory):
        """判断是否为重要目录"""
        return (not directory.name.startswith('.') and 
                directory.name not in ['__pycache__', 'node_modules', '.git'])
    
    def _is_important_file(self, file_path):
        """判断是否为重要文件"""
        return (not file_path.name.startswith('.') and 
                file_path.suffix in ['.py', '.js', '.md', '.json', '.yml', '.sql', '.db'])
    
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
        """获取最近修改的文件列表"""
        recent_files = []
        cutoff_time = datetime.now().timestamp() - (7 * 24 * 3600)  # 7天内
        
        def check_files(path, max_depth=2, current_depth=0):
            if current_depth >= max_depth:
                return
                
            try:
                for item in path.iterdir():
                    if item.name.startswith('.'):
                        continue
                        
                    if item.is_file() and item.stat().st_mtime > cutoff_time:
                        rel_path = item.relative_to(self.project_root)
                        recent_files.append((str(rel_path), item.stat().st_mtime))
                    elif item.is_dir() and item.name not in ['__pycache__', 'node_modules']:
                        check_files(item, max_depth, current_depth + 1)
            except PermissionError:
                pass
        
        check_files(self.project_root)
        return sorted(recent_files, key=lambda x: x[1], reverse=True)
    
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
        status_info = []
        
        # 检查数据库是否存在
        db_files = list(self.project_root.glob("**/*.db"))
        if db_files:
            status_info.append(f"✅ 数据库已创建 ({len(db_files)} 个数据库文件)")
        else:
            status_info.append("⏳ 数据库未创建")
        
        # 检查后端代码
        backend_files = list((self.project_root / "backend").glob("**/*.py")) if (self.project_root / "backend").exists() else []
        if backend_files:
            status_info.append(f"🔧 后端开发中 ({len(backend_files)} 个Python文件)")
        else:
            status_info.append("⏳ 后端代码未开始")
        
        # 检查前端代码
        frontend_files = []
        if (self.project_root / "frontend").exists():
            frontend_files.extend(list((self.project_root / "frontend").glob("**/*.html")))
            frontend_files.extend(list((self.project_root / "frontend").glob("**/*.js")))
            frontend_files.extend(list((self.project_root / "frontend").glob("**/*.css")))
        
        if frontend_files:
            status_info.append(f"🎨 前端开发中 ({len(frontend_files)} 个前端文件)")
        else:
            status_info.append("⏳ 前端代码未开始")
        
        # 检查测试代码
        test_files = list((self.project_root / "tests").glob("**/*.py")) if (self.project_root / "tests").exists() else []
        if test_files:
            status_info.append(f"🧪 测试代码 ({len(test_files)} 个测试文件)")
        else:
            status_info.append("⏳ 测试代码未编写")
        
        # 检查文档
        doc_files = list(self.project_root.glob("**/*.md"))
        doc_count = len([f for f in doc_files if ".ai-context" not in str(f)])
        if doc_count > 0:
            status_info.append(f"📚 项目文档 ({doc_count} 个文档文件)")
        
        return "\n".join([f"- {info}" for info in status_info]) or "- 项目刚开始"
    
    def _get_project_status(self):
        """读取最新的项目状态信息"""
        status_file = self.project_root / '.ai-context' / 'status' / 'latest-status.md'
        
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

if __name__ == "__main__":
    generator = ContextGenerator(".")
    summary = generator.generate_context_summary()
    print(summary)
