#!/usr/bin/env python3
"""
AI上下文管理系统快速部署脚本
一键创建完整的上下文管理系统

使用方法:
python deploy-ai-context.py [项目路径] [--level=basic|standard|full]
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

class AIContextDeployer:
    def __init__(self, project_root, level="basic"):
        self.project_root = Path(project_root).resolve()
        self.level = level
        self.ai_context_dir = self.project_root / ".ai-context"
        
    def deploy(self):
        """部署AI上下文管理系统"""
        print(f"🚀 开始部署AI上下文管理系统...")
        print(f"📁 项目路径: {self.project_root}")
        print(f"⚙️  部署级别: {self.level}")
        print("-" * 60)
        
        # 阶段1: 基础结构
        self._create_basic_structure()
        
        if self.level in ["standard", "full"]:
            # 阶段2: 标准工具
            self._create_standard_tools()
            
        if self.level == "full":
            # 阶段3: 高级集成
            self._create_advanced_integration()
        
        # 最终设置
        self._finalize_setup()
        
        print("\n✅ AI上下文管理系统部署完成!")
        self._print_next_steps()
    
    def _create_basic_structure(self):
        """创建基础目录结构和文件"""
        print("📂 创建基础目录结构...")
        
        # 创建目录
        directories = [
            self.ai_context_dir,
            self.ai_context_dir / "templates",
            self.ai_context_dir / "docs", 
            self.ai_context_dir / "tools",
            self.ai_context_dir / "cache"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {directory.relative_to(self.project_root)}")
        
        # 创建配置文件
        self._create_config_file()
        
        # 创建基础模板
        self._create_basic_templates()
        
        # 创建基础文档
        self._create_basic_docs()
    
    def _create_config_file(self):
        """创建配置文件"""
        print("⚙️  创建配置文件...")
        
        # 检测项目基本信息
        project_name = self.project_root.name
        project_type = self._detect_project_type()
        
        config = {
            "project": {
                "name": project_name,
                "type": project_type,
                "version": "1.0.0",
                "created": datetime.now().isoformat()
            },
            "settings": {
                "auto_update": True,
                "session_prefix": f"{project_name}-",
                "template_version": "1.0",
                "max_context_length": 10000
            },
            "integrations": {
                "vscode": self.level in ["standard", "full"],
                "git": self.level == "full",
                "ci_cd": False
            }
        }
        
        config_file = self.ai_context_dir / "context-config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ context-config.json")
    
    def _detect_project_type(self):
        """简单的项目类型检测"""
        # 检查特征文件
        if (self.project_root / "package.json").exists():
            return "web_project"
        elif (self.project_root / "requirements.txt").exists():
            return "python_project"
        elif (self.project_root / "pom.xml").exists():
            return "java_project"
        elif (self.project_root / "Cargo.toml").exists():
            return "rust_project"
        elif any(self.project_root.glob("*.md")):
            return "documentation"
        else:
            return "general"
    
    def _create_basic_templates(self):
        """创建基础模板"""
        print("📝 创建模板文件...")
        
        # 会话启动模板
        session_template = '''# AI Agent会话启动模板

## 项目基本信息
- **项目名称**：{{project_name}}
- **项目类型**：{{project_type}}
- **技术栈**：{{tech_stack}}
- **项目路径**：{{project_path}}

## 当前会话信息
- **会话主题**：{{session_topic}}
- **会话目标**：{{session_goal}}
- **关注文件**：{{focus_files}}
- **技术约束**：{{constraints}}

## 工作要求
1. 严格遵循项目技术规范和约束
2. 保持代码风格和架构一致性
3. 优先考虑现有解决方案的兼容性
4. 及时提出不清晰的地方

## 成功标准
- {{success_criteria}}

请确认你理解了以上上下文信息，然后开始协助完成任务。
'''
        
        template_file = self.ai_context_dir / "templates" / "session-starter.md"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(session_template)
        print("  ✓ session-starter.md")
        
        # 状态更新模板
        status_template = '''# 项目状态更新模板

## 更新时间
{{update_time}}

## 完成的工作
- [ ] {{completed_task_1}}
- [ ] {{completed_task_2}}

## 进行中的任务
- [ ] {{ongoing_task_1}}
- [ ] {{ongoing_task_2}}

## 待处理问题
1. {{issue_1}}
2. {{issue_2}}

## 下一步计划
- {{next_step_1}}
- {{next_step_2}}

## 重要说明
{{important_notes}}
'''
        
        status_template_file = self.ai_context_dir / "templates" / "status-update.md"
        with open(status_template_file, 'w', encoding='utf-8') as f:
            f.write(status_template)
        print("  ✓ status-update.md")
    
    def _create_basic_docs(self):
        """创建基础文档"""
        print("📚 创建文档文件...")
        
        # 项目概览
        project_overview = f'''# {self.project_root.name} - 项目概览

## 基本信息
- **项目名称**：{self.project_root.name}
- **项目类型**：{self._detect_project_type()}
- **创建时间**：{datetime.now().strftime("%Y-%m-%d")}
- **主要技术栈**：[待填写]
- **开发环境**：[待填写]

## 项目结构
```
{self._get_project_structure()}
```

## 核心组件
- [组件1]：[简要描述]
- [组件2]：[简要描述]
- [组件3]：[简要描述]

## 当前状态
- **完成度**：[百分比]
- **主要功能**：[列出已实现功能]
- **已知问题**：[列出待解决问题]
- **下一步计划**：[近期工作计划]

## 技术约束
- [约束1]
- [约束2]
- [约束3]

## 重要说明
[其他需要特别注意的事项]

---
*此文档由AI上下文管理系统自动生成，请根据实际情况更新内容*
'''
        
        overview_file = self.ai_context_dir / "docs" / "project-overview.md"
        with open(overview_file, 'w', encoding='utf-8') as f:
            f.write(project_overview)
        print("  ✓ project-overview.md")
        
        # 使用指南
        usage_guide = '''# AI上下文管理系统使用指南

## 快速开始

### 1. 手动启动会话
复制并填写 `.ai-context/templates/session-starter.md` 模板

### 2. 更新项目状态
编辑 `.ai-context/docs/project-overview.md` 文件

### 3. 记录会话
在 `.ai-context/cache/` 目录下保存重要对话记录

## 文件说明

### 配置文件
- `context-config.json`: 系统配置
- `project-overview.md`: 项目核心信息

### 模板文件
- `session-starter.md`: 会话启动模板
- `status-update.md`: 状态更新模板

### 缓存目录
- `cache/`: 存放临时文件和会话记录

## 最佳实践

1. **定期更新**：及时更新项目状态和技术信息
2. **模板定制**：根据项目特点调整模板内容
3. **分类管理**：不同类型的会话使用不同的主题标识
4. **备份重要信息**：将关键决策和方案保存到文档中

## 升级到高级功能

如需更多自动化功能，可以：
1. 重新运行部署脚本，选择 `--level=standard` 或 `--level=full`
2. 手动安装 `.ai-context/tools/` 目录下的工具脚本

---
*更多详细信息请参考完整的部署文档*
'''
        
        guide_file = self.ai_context_dir / "docs" / "usage-guide.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(usage_guide)
        print("  ✓ usage-guide.md")
    
    def _get_project_structure(self):
        """获取项目结构"""
        structure_lines = []
        for item in sorted(self.project_root.iterdir()):
            if item.name.startswith('.') and item.name != '.ai-context':
                continue
            if item.is_dir():
                structure_lines.append(f"{item.name}/")
            else:
                structure_lines.append(item.name)
        
        return "\n".join(structure_lines[:10])  # 只显示前10项
    
    def _create_standard_tools(self):
        """创建标准工具"""
        print("🛠️  创建标准工具...")
        
        # 项目检测器
        detector_code = '''#!/usr/bin/env python3
"""
简化版项目类型检测器
"""
import os
import json
from pathlib import Path
from collections import defaultdict

class ProjectDetector:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
    
    def detect_project_type(self):
        """检测项目类型"""
        # 检查特征文件
        if (self.project_root / "package.json").exists():
            return "web_project", 0.9
        elif (self.project_root / "requirements.txt").exists():
            return "python_project", 0.9
        elif (self.project_root / "pom.xml").exists():
            return "java_project", 0.9
        elif (self.project_root / "Cargo.toml").exists():
            return "rust_project", 0.9
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
        
        return tech_stack or ["通用"]

if __name__ == "__main__":
    detector = ProjectDetector(".")
    proj_type, confidence = detector.detect_project_type()
    tech_stack = detector.get_tech_stack()
    
    print(f"项目类型: {proj_type} (置信度: {confidence:.2f})")
    print(f"技术栈: {', '.join(tech_stack)}")
'''
        
        detector_file = self.ai_context_dir / "tools" / "project-detector.py"
        with open(detector_file, 'w', encoding='utf-8') as f:
            f.write(detector_code)
        print("  ✓ project-detector.py")
        
        # 简化版上下文生成器
        generator_code = '''#!/usr/bin/env python3
"""
上下文信息生成器
"""
import os
import json
from datetime import datetime
from pathlib import Path

try:
    from project_detector import ProjectDetector
except ImportError:
    print("警告: 无法导入project_detector，使用简化版本")
    class ProjectDetector:
        def __init__(self, project_root):
            self.project_root = Path(project_root)
        def detect_project_type(self):
            return "general", 0.5
        def get_tech_stack(self):
            return ["通用"]

class ContextGenerator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.ai_context_dir = self.project_root / ".ai-context"
        
    def generate_context_summary(self):
        """生成简化的上下文总结"""
        detector = ProjectDetector(self.project_root)
        proj_type, confidence = detector.detect_project_type()
        tech_stack = detector.get_tech_stack()
        
        summary = f"""# 项目上下文总结
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 项目信息
- 名称: {self.project_root.name}
- 类型: {proj_type}
- 技术栈: {', '.join(tech_stack)}
- 路径: {self.project_root}

## 重要文件
{self._get_important_files()}

## 最近更新
{self._get_recent_changes()}
"""
        
        # 保存到缓存
        cache_file = self.ai_context_dir / "cache" / "latest-context.md"
        cache_file.parent.mkdir(exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return summary
    
    def _get_important_files(self):
        """获取重要文件列表"""
        important_files = []
        patterns = ["*.py", "*.js", "*.md", "*.json", "*.yml"]
        
        for pattern in patterns:
            for file_path in self.project_root.glob(pattern):
                if ".ai-context" not in str(file_path):
                    important_files.append(f"- {file_path.name}")
        
        return "\\n".join(important_files[:10]) or "- 暂无识别到重要文件"
    
    def _get_recent_changes(self):
        """获取最近变更（简化版）"""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                capture_output=True, text=True, cwd=self.project_root
            )
            if result.returncode == 0:
                return result.stdout.strip() or "- 暂无Git历史记录"
        except:
            pass
        return "- 无法获取变更历史"

if __name__ == "__main__":
    generator = ContextGenerator(".")
    summary = generator.generate_context_summary()
    print(summary)
'''
        
        generator_file = self.ai_context_dir / "tools" / "context-generator.py"
        with open(generator_file, 'w', encoding='utf-8') as f:
            f.write(generator_code)
        print("  ✓ context-generator.py")
    
    def _create_advanced_integration(self):
        """创建高级集成"""
        print("🔧 创建高级集成...")
        
        # VS Code设置
        vscode_dir = self.project_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        # 创建VS Code任务
        tasks = {
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
                }
            ]
        }
        
        tasks_file = vscode_dir / "tasks.json"
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2)
        print("  ✓ .vscode/tasks.json")
        
        # Git钩子（如果是Git仓库）
        git_dir = self.project_root / ".git"
        if git_dir.exists():
            hooks_dir = git_dir / "hooks"
            if hooks_dir.exists():
                pre_commit_hook = hooks_dir / "pre-commit"
                hook_content = '''#!/bin/sh
# AI上下文自动更新
echo "更新AI上下文..."
python .ai-context/tools/context-generator.py > /dev/null 2>&1
'''
                with open(pre_commit_hook, 'w') as f:
                    f.write(hook_content)
                pre_commit_hook.chmod(0o755)
                print("  ✓ Git pre-commit hook")
    
    def _finalize_setup(self):
        """完成设置"""
        print("🎯 完成最终设置...")
        
        # 创建README
        readme_content = f'''# AI上下文管理系统

本项目已集成AI上下文管理系统，部署级别：{self.level}

## 快速使用

### 生成项目上下文
```bash
python .ai-context/tools/context-generator.py
```

### 查看使用指南
查看 `.ai-context/docs/usage-guide.md` 获取详细使用说明

## 系统结构
- `.ai-context/`: 上下文管理根目录
- `templates/`: 模板文件
- `docs/`: 项目文档
- `tools/`: 自动化工具
- `cache/`: 缓存文件

## 下一步
1. 编辑 `.ai-context/docs/project-overview.md` 完善项目信息
2. 根据需要调整 `.ai-context/templates/` 中的模板
3. 开始使用AI助手进行开发协作

---
*系统版本: 1.0*
*部署时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
'''
        
        readme_file = self.ai_context_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("  ✓ README.md")
    
    def _print_next_steps(self):
        """打印后续步骤"""
        print("\n" + "="*60)
        print("🎉 部署完成！后续步骤：")
        print("="*60)
        
        print("\n📝 立即可做的：")
        print("1. 编辑 .ai-context/docs/project-overview.md 完善项目信息")
        print("2. 运行：python .ai-context/tools/context-generator.py")
        print("3. 复制生成的上下文信息到AI对话中")
        
        if self.level in ["standard", "full"]:
            print("\n🛠️  可选的高级功能：")
            print("- 自定义 .ai-context/templates/ 中的模板")
            print("- 使用 VS Code 任务面板运行上下文生成")
            
        if self.level == "full":
            print("- Git提交时自动更新上下文")
            
        print("\n📚 文档位置：")
        print("- 使用指南：.ai-context/docs/usage-guide.md")
        print("- 项目概览：.ai-context/docs/project-overview.md")
        print("- 系统说明：.ai-context/README.md")
        
        print("\n🔧 如需升级：")
        print(f"python {__file__} {self.project_root} --level=full")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI上下文管理系统部署工具")
    parser.add_argument("project_path", nargs="?", default=".", help="项目路径（默认当前目录）")
    parser.add_argument("--level", choices=["basic", "standard", "full"], default="basic", 
                       help="部署级别：basic(基础)/standard(标准)/full(完整)")
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
