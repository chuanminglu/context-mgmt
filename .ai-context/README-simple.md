# TaskFlow 上下文管理系统

## 🎯 简介

一个**简洁、自动、实用**的项目信息管理工具，让AI协作变得简单高效。

**核心理念**：一个工具、一个文件、一条命令，立即获得完整项目上下文。

## 📁 目录结构

```
.ai-context/
├── tools/
│   └── context-generator.py    # 🔧 核心工具（自动扫描生成上下文）
├── docs/
│   └── project-overview.md     # 📋 项目概览（手动维护的战略文档）
├── cache/
│   └── latest-context.md       # 🌟 最新上下文（AI协作核心文件）
└── README.md                   # 📖 本使用指南
```

## ⚡ 快速使用

### 首次使用
```bash
# 项目根目录运行（仅需一次）
python deploy-ai-context.py
```

### 日常开发
```bash
# 每天开始工作时运行
python .ai-context/tools/context-generator.py

# 或使用 VS Code 任务：
# Ctrl+Shift+P → "Tasks: Run Task" → "生成AI上下文"
```

### AI协作
1. 复制 `.ai-context/cache/latest-context.md` 内容给AI
2. 说明你要完成的任务
3. 开始高效协作 🚀

## 🎯 核心文件说明

| 文件 | 用途 | 更新方式 | 使用场景 |
|------|------|----------|----------|
| **latest-context.md** | AI协作专用 | 自动生成 | 每次AI协作必用 ⭐ |
| **project-overview.md** | 项目战略规划 | 手动维护 | 新人了解、架构设计 |
| **context-generator.py** | 核心生成工具 | 系统工具 | 每天运行一次 |

## 📊 使用场景

### 日常AI协作（95%的情况）
```bash
python .ai-context/tools/context-generator.py
# 使用 latest-context.md ✅
```

### 新人了解项目
```bash
# 1. 先看项目背景
cat .ai-context/docs/project-overview.md

# 2. 再看当前状态  
cat .ai-context/cache/latest-context.md
```

### 换电脑/新会话
```bash
git pull
python .ai-context/tools/context-generator.py
# 继续使用 latest-context.md
```

## 🔄 维护频率

- **context-generator.py**：每天运行 ⏰
- **latest-context.md**：自动更新 🤖
- **project-overview.md**：里程碑更新（周/月）📅

## 💡 设计亮点

### 对比传统方法
❌ **传统**：手动维护多个文档，经常过时  
✅ **现在**：自动扫描生成，始终最新

### 对比复杂系统  
❌ **复杂**：多工具、多配置、学习成本高  
✅ **简洁**：一命令、一文件、立即可用

### AI协作优化
❌ **之前**：每次重新描述项目  
✅ **现在**：一个文件包含完整上下文

## 🎮 实际示例

### 场景1：开发新功能
```bash
# 1. 刷新上下文
python .ai-context/tools/context-generator.py

# 2. AI协作
# 复制 latest-context.md → 粘贴给AI → "我要开发用户认证"
```

### 场景2：完成重要里程碑
```bash
# 1. 更新战略文档
# 手动编辑 project-overview.md（更新完成度、功能状态）

# 2. 刷新技术上下文
python .ai-context/tools/context-generator.py
```

## 🚫 已简化掉的功能

为保持简洁，移除了以下复杂功能：
- ❌ 交互式会话管理
- ❌ 状态更新工具  
- ❌ 多层文档结构
- ❌ 复杂的配置系统

**备份位置**：`.ai-context/backup/`（如需恢复）

## ⚙️ VS Code 集成

可用任务：
- **生成AI上下文** ⭐（推荐日常使用）
- **智能上下文检查**（检查是否需更新）  
- **强制上下文刷新**（强制重新生成）

## 🆘 常见问题

**Q: 怎么知道上下文是否最新？**  
A: 查看 `latest-context.md` 顶部的生成时间

**Q: 什么时候更新 project-overview.md？**  
A: 完成重要功能、架构变更、新人入职前

**Q: 可以自定义生成内容吗？**  
A: 可以修改 `context-generator.py`，但建议保持简洁

**Q: 团队如何使用？**  
A: 5分钟演示：部署→生成→AI协作，立即见效

## 🎯 核心思想

**让上下文管理成为开发助力，而非负担**

简单 → 自动 → 有用 → 高效协作

---

*系统版本：简化版 v2.0 - 专注核心功能，追求极致简洁*
