# TaskFlow 上下文管理系统

## 🎯 系统概述

TaskFlow 上下文管理系统是一个**简洁、自动、实用**的项目信息管理工具，帮助开发者和AI助手快速了解项目状态，提高协作效率。

### 核心理念
- **简单**：一个工具，一个文件，专注核心功能
- **自动**：扫描代码自动生成上下文，减少手动维护
- **有用**：提供完整、准确的项目信息，支持高效AI协作

## 📁 目录结构

```
.ai-context/
├── tools/                          # 核心工具
│   └── context-generator.py           # 上下文生成器（唯一核心工具）
├── docs/                           # 项目文档
│   ├── project-overview.md            # 项目整体概览（手动维护）
│   ├── context-management-guide.md    # 完整使用指南
│   └── project-overview-usage.md      # 概览文档使用说明
├── cache/                          # 自动生成文件
│   └── latest-context.md              # 最新项目上下文（AI协作核心文件）
├── templates/                      # 系统模板（可选）
│   └── session-starter.md             # AI协作会话模板
├── backup/                         # 复杂功能备份
└── README.md                       # 本文档
```

## 🚀 快速开始

### 1. 首次使用（项目初始化）

```bash
# 在项目根目录运行（只需一次）
python deploy-ai-context.py
```

**初始化后的设置**：
- 手动编辑 `.ai-context/docs/project-overview.md` 填写项目基本信息
- 这是唯一需要手动创建的文档

### 2. 日常开发工作流

#### 每天开始工作时
```bash
# 方法1：命令行运行
python .ai-context/tools/context-generator.py

# 方法2：VS Code任务
# Ctrl+Shift+P → "Tasks: Run Task" → "生成AI上下文"
```

#### AI协作时
1. 查看文件：`.ai-context/cache/latest-context.md`
2. 复制内容给AI助手
3. 说明你要完成的具体任务
4. 开始高效协作

### 3. 新会话/换电脑工作

```bash
# 1. 获取最新代码
git pull

# 2. 刷新项目上下文
python .ai-context/tools/context-generator.py

# 3. 查看当前状态
cat .ai-context/cache/latest-context.md
# Windows: type .ai-context\cache\latest-context.md

# 4. 开始工作
```

## 🎯 核心文件说明

### latest-context.md（🌟 核心文件）
- **用途**：AI协作的完整项目信息
- **内容**：项目结构、代码状态、最近变更、技术约束
- **更新**：自动生成，每次运行 `context-generator.py` 时更新
- **使用**：每次AI协作时使用此文件

### project-overview.md（📋 概览文档）
- **用途**：项目整体规划和架构文档
- **内容**：项目背景、核心功能、技术选型、开发方法论
- **更新**：手动维护，里程碑式更新（周/月级别）
- **使用**：新人了解项目、复杂架构变更时参考

### context-generator.py（🔧 核心工具）
- **用途**：自动扫描项目生成上下文
- **功能**：扫描文件结构、检测技术栈、分析代码状态
- **运行**：每天开始工作时运行一次

## 📊 使用场景对比

| 场景 | 使用方法 | 主要文件 |
|------|----------|----------|
| 日常AI协作 | 直接使用 | `latest-context.md` |
| 新人了解项目 | 先读概览，再看上下文 | `project-overview.md` + `latest-context.md` |
| 复杂架构设计 | 两个文档都参考 | 两个文档 |
| 简单bug修复 | 只需上下文 | `latest-context.md` |
| 项目规划会议 | 更新概览 | `project-overview.md` |

## 🔄 VS Code 集成

### 可用任务
- **生成AI上下文**：刷新项目上下文
- **智能上下文检查**：检查是否需要更新
- **自动上下文刷新**：智能决定是否刷新
- **强制上下文刷新**：强制重新生成

### 使用方法
```
Ctrl+Shift+P → "Tasks: Run Task" → 选择对应任务
```

**推荐**：每天第一次打开项目时运行"生成AI上下文"

## 📅 维护频率建议

| 文件/操作 | 频率 | 触发条件 |
|----------|------|----------|
| 运行 `context-generator.py` | 每天 | 开始工作前 |
| 查看 `latest-context.md` | 按需 | 每次AI协作 |
| 更新 `project-overview.md` | 每周/月 | 完成重要功能、架构变更 |

## 🎮 实际操作示例

### 场景1：开始新的开发任务
```bash
# 1. 刷新上下文
python .ai-context/tools/context-generator.py

# 2. AI协作
# 复制 .ai-context/cache/latest-context.md 给AI
# 说明："我要开发用户认证功能"
```

### 场景2：项目完成重要里程碑
```bash
# 1. 更新项目概览
# 手动编辑 .ai-context/docs/project-overview.md
# 更新完成度、已完成功能等

# 2. 刷新上下文
python .ai-context/tools/context-generator.py
```

### 场景3：新同事加入团队
```
# 1. 先阅读项目概览了解背景
cat .ai-context/docs/project-overview.md

# 2. 查看当前状态
cat .ai-context/cache/latest-context.md

# 3. 开始具体开发
```

## ⚡ 核心优势

### 对比传统方法
- ❌ **传统**：手动维护多个文档，容易过时
- ✅ **现在**：一个工具自动生成，始终最新

### 对比复杂系统
- ❌ **复杂系统**：多个工具，复杂配置，学习成本高
- ✅ **本系统**：一个命令，一个文件，立即可用

### AI协作优化
- ❌ **之前**：每次都要重新描述项目情况
- ✅ **现在**：一个文件包含完整上下文

## 🔧 系统设计原则

### 简化原则
- **单一工具**：只有 `context-generator.py` 一个核心工具
- **单一输出**：主要使用 `latest-context.md` 一个文件
- **最小维护**：大部分信息自动生成

### 实用原则
- **自动检测**：技术栈、文件结构、代码状态
- **智能集成**：合并自动检测和手动文档
- **即用即得**：生成的文件直接用于AI协作

## 🚫 已移除的复杂功能

为保持简洁，已移除以下功能（备份在 `backup/` 目录）：
- ❌ `sessions/` 目录（会话管理过于复杂）
- ❌ `status/` 目录（状态管理重复信息）
- ❌ 交互式工具（增加使用复杂度）
- ❌ 多层文档结构（维护负担重）

## 💡 最佳实践

1. **每天第一件事**：运行上下文生成
2. **AI协作标准流程**：`latest-context.md` + 具体任务描述
3. **重要里程碑**：更新 `project-overview.md`
4. **团队协作**：确保所有人都了解这个简单的工作流程

## 🆘 常见问题

**Q: 如何知道上下文是否是最新的？**
A: 查看 `latest-context.md` 顶部的生成时间

**Q: 什么时候需要更新 project-overview.md？**
A: 完成重要功能、技术选型变更、新人入职前

**Q: 可以自定义生成的上下文内容吗？**
A: 可以编辑 `context-generator.py`，但建议保持简洁

**Q: 如何在团队中推广使用？**
A: 演示 5 分钟：部署→生成→AI协作，立即看到效果

---

## 🎯 核心思想

让上下文管理成为开发的**助力**而非**负担**。

**简单 → 自动 → 有用 → 高效协作**
