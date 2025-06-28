#!/usr/bin/env python3
"""
上下文管理系统简化脚本
移除过于复杂的功能，保持简洁有用的核心功能
"""

import os
import shutil
from pathlib import Path

def cleanup_context_system():
    """简化上下文管理系统"""
    project_root = Path.cwd()
    ai_context_dir = project_root / '.ai-context'
    
    print("🧹 开始简化上下文管理系统...")
    
    # 备份重要文件
    backup_dir = ai_context_dir / 'backup'
    backup_dir.mkdir(exist_ok=True)
    
    # 移除过于复杂的目录
    dirs_to_remove = ['sessions', 'status', 'config', 'logs']
    
    for dir_name in dirs_to_remove:
        dir_path = ai_context_dir / dir_name
        if dir_path.exists():
            print(f"🗑️  移除目录: {dir_name}")
            # 先备份重要文件
            if dir_name == 'status' and (dir_path / 'latest-status.md').exists():
                shutil.copy2(dir_path / 'latest-status.md', backup_dir / 'latest-status.md')
            shutil.rmtree(dir_path)
    
    # 简化tools目录，移除复杂工具
    tools_dir = ai_context_dir / 'tools'
    complex_tools = ['update-status.py', 'start-session.py', 'context-manager.py']
    
    for tool in complex_tools:
        tool_path = tools_dir / tool
        if tool_path.exists():
            print(f"🗑️  移除复杂工具: {tool}")
            # 备份到backup目录
            shutil.copy2(tool_path, backup_dir / tool)
            tool_path.unlink()
    
    # 简化templates目录
    templates_dir = ai_context_dir / 'templates'
    if templates_dir.exists():
        # 只保留一个简单的会话模板
        for template_file in templates_dir.glob('*'):
            if template_file.name not in ['session-starter.md']:
                template_file.unlink()
    
    # 创建简化的README
    create_simple_readme(ai_context_dir)
    
    print("✅ 系统简化完成！")
    print(f"📁 备份文件保存在: {backup_dir}")
    print("\n📋 简化后的目录结构:")
    print_directory_structure(ai_context_dir)

def create_simple_readme(ai_context_dir):
    """创建简化的README"""
    readme_content = """# TaskFlow 上下文管理系统

## 快速使用

### 日常开发
```bash
# 每天开始工作时运行
python .ai-context/tools/context-generator.py
```

### AI协作
1. 查看文件：`.ai-context/cache/latest-context.md`
2. 复制内容给AI助手
3. 说明你要完成的任务

### VS Code任务
- Ctrl+Shift+P → "Tasks: Run Task" → "生成AI上下文"

## 目录说明
- `tools/` - 核心工具（context-generator.py）
- `docs/` - 项目文档（project-overview.md）  
- `cache/` - 自动生成的上下文文件
- `templates/` - 会话模板（可选）

## 核心原则
简单、自动、有用 - 让上下文管理成为开发助力而非负担。
"""
    
    with open(ai_context_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

def print_directory_structure(path, indent=0):
    """打印目录结构"""
    items = []
    if path.is_dir():
        for item in sorted(path.iterdir()):
            if item.name.startswith('.'):
                continue
            prefix = "  " * indent + ("├── " if indent > 0 else "")
            if item.is_dir():
                items.append(f"{prefix}📁 {item.name}/")
                items.extend(print_directory_structure(item, indent + 1))
            else:
                items.append(f"{prefix}📄 {item.name}")
    
    if indent == 0:
        for item in items[:10]:  # 限制显示条目
            print(item)
        if len(items) > 10:
            print(f"  ... 还有 {len(items) - 10} 个项目")
    
    return items

if __name__ == "__main__":
    try:
        cleanup_context_system()
    except Exception as e:
        print(f"❌ 清理过程出错: {e}")
