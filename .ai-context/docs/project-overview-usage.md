# project-overview.md 使用指南

## 🎯 什么是 project-overview.md？

`project-overview.md` 是项目的**战略文档**，记录项目的整体规划、架构决策和长期目标。它与自动生成的 `latest-context.md` 形成互补：

- **latest-context.md**：反映项目**当前状态**（自动生成）
- **project-overview.md**：记录项目**整体规划**（手动维护）

## 📅 什么时候使用？

### 1. **项目初始化时**（必须）
项目刚开始时，编辑此文件定义：
```
- 项目基本信息（名称、类型、技术栈）
- 核心功能规划
- 技术架构选择
- 开发方法论
```

### 2. **重大里程碑时**（推荐）
完成重要阶段后，更新：
```
- 当前完成度
- 已完成的核心功能
- 下一阶段计划
- 架构演进记录
```

### 3. **技术决策时**（可选）
做出重要技术选择时，记录：
```
- 技术选型原因
- 架构约束变更
- 开发方法调整
```

### 4. **团队协作时**（重要）
新成员加入或团队协作时：
```
- 让新人快速理解项目背景
- 统一技术架构理解
- 明确开发规范和约束
```

## 🔄 与 latest-context.md 的关系

### latest-context.md（自动）
- **内容**：代码结构、文件变更、当前状态
- **更新**：每天/每次开发前运行工具自动更新
- **用途**：AI协作、了解代码现状

### project-overview.md（手动）
- **内容**：项目背景、架构规划、长期目标
- **更新**：里程碑式手动更新（周/月级别）
- **用途**：项目规划、团队对齐、架构指导

## 🎯 实际使用场景

### 场景1：项目刚开始（必须使用）
```bash
# 1. 部署上下文系统
python deploy-ai-context.py

# 2. 编辑项目概览
# 手动编辑 .ai-context/docs/project-overview.md
# 定义：项目目标、技术栈、功能规划

# 3. 生成初始上下文
python .ai-context/tools/context-generator.py
```

### 场景2：日常开发（主要用 latest-context.md）
```bash
# 每天开发时主要使用自动生成的上下文
python .ai-context/tools/context-generator.py

# AI协作时使用：
# .ai-context/cache/latest-context.md
```

### 场景3：完成重要功能（更新 project-overview.md）
```
✅ 完成用户认证模块
↓
更新 project-overview.md 中的：
- 当前完成度：20% → 40%
- 已完成功能：添加用户认证
- 下一步计划：开始任务管理开发
```

### 场景4：新人入职（必须参考）
```
新开发者加入团队：
1. 先阅读 project-overview.md 了解项目背景
2. 再查看 latest-context.md 了解当前状态
3. 开始具体开发工作
```

### 场景5：AI协作选择

**简单任务**：直接使用 `latest-context.md`
```
"帮我修复这个bug"
"实现这个小功能"
→ 使用 latest-context.md 即可
```

**复杂任务**：先参考 `project-overview.md`
```
"重构整个认证系统"
"设计新的数据架构"
→ 先查看 project-overview.md 了解整体规划
→ 再用 latest-context.md 了解具体状态
```

## 📊 更新频率建议

| 文件 | 更新频率 | 触发条件 |
|------|----------|----------|
| `latest-context.md` | 每天 | 开始开发前自动生成 |
| `project-overview.md` | 每周/月 | 重要里程碑、架构变更 |

## ✅ 实际操作示例

### TaskFlow 项目当前状态
- **latest-context.md**：显示已完成数据库设计，准备开始后端开发
- **project-overview.md**：记录项目采用"数据库先行"方法，当前处于原型验证阶段

### 如果你现在要开始后端开发：
1. **查看** `project-overview.md` 了解技术约束和架构规划
2. **生成** `latest-context.md` 了解当前代码状态
3. **开始开发** 基于两个文档的指导

## 🎯 核心原则

**project-overview.md** 是项目的**指北针**：
- 不需要频繁更新
- 专注于战略和规划
- 为长期开发提供方向指导

**latest-context.md** 是项目的**实时状态**：
- 每天自动更新
- 反映具体的代码和文件状态
- 为日常开发和AI协作提供精确信息

简单说：**概览看方向，上下文看现状**。
