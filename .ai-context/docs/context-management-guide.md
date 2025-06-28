# TaskFlow 上下文管理完整指南

## 🎯 核心理念

**简单原则**：上下文管理应该让开发更轻松，而不是更复杂。

## 📁 .ai-context 目录结构说明

```
.ai-context/
├── tools/               # 工具脚本（自动化）
│   ├── context-generator.py    # 自动扫描项目生成上下文
│   ├── smart-refresh.py        # 智能刷新（可选）
│   └── context-manager.py      # 统一管理界面
├── docs/                # 项目文档（手动维护）
│   └── project-overview.md     # 项目整体概览
├── cache/               # 自动生成的缓存
│   └── latest-context.md       # 最新项目上下文（自动生成）
└── templates/           # 模板文件（系统模板）
    ├── session-starter.md      # AI协作会话模板
    └── status-update.md        # 状态更新模板
```

**关键说明**：
- **tools/** = 自动化脚本，偶尔运行
- **docs/** = 手动文档，阶段性更新  
- **cache/** = 自动生成，反映当前状态
- **templates/** = 系统模板，基本不变

## 🚀 使用流程

### 1. 项目刚启动时要做什么？

#### 第一次部署（只做一次）
```bash
# 在项目根目录运行
python deploy-ai-context.py
```
**这会创建**：
- `.ai-context/` 目录结构
- 基本的工具和模板
- 初始的项目概览文档

#### 初始化项目信息（只做一次）  
手动编辑 `.ai-context/docs/project-overview.md`，填写：
- 项目基本信息
- 技术栈选择
- 核心功能规划

### 2. 项目开发中要做什么？

#### 日常开发（建议频率）

**每天开始工作时**：
```bash
# 方法1：使用VS Code任务
Ctrl+Shift+P → "Tasks: Run Task" → "生成AI上下文"

# 方法2：直接运行
python .ai-context/tools/context-generator.py
```
**作用**：更新 `latest-context.md`，反映最新的代码和文件状态

**需要AI协作时**：
1. 直接把 `.ai-context/cache/latest-context.md` 的内容给AI
2. 说明你要做什么任务
3. 开始协作

**完成重要功能时（可选）**：
更新 `.ai-context/docs/project-overview.md` 中的当前状态

### 3. VS Code 任务使用

你已经有这些任务可用：

```json
// 在 VS Code 中按 Ctrl+Shift+P，输入 "Tasks: Run Task"
{
  "生成AI上下文": "自动扫描项目，生成最新上下文",
  "智能上下文检查": "检查是否需要刷新上下文", 
  "自动上下文刷新": "智能决定是否刷新",
  "强制上下文刷新": "强制重新生成上下文"
}
```

**推荐**：每天第一次打开项目时运行 "生成AI上下文"

### 4. 新会话的概念

#### 什么是"新会话"？
- 在新电脑上工作
- 长时间中断后恢复开发  
- 邀请新的开发者/AI助手协作
- 开始新的功能模块开发

#### 新会话时怎么做？

**简单方法**（推荐）：
1. 运行：`python .ai-context/tools/context-generator.py`
2. 查看：`.ai-context/cache/latest-context.md`
3. 把这个文件内容给AI，说明你要做什么

**完整方法**（可选）：
1. 查看 `.ai-context/docs/project-overview.md` 了解项目整体
2. 运行上下文生成获取最新状态
3. 开始协作

## 🎯 实际操作示例

### 场景1：项目第一次使用
```bash
# 1. 部署上下文管理
python deploy-ai-context.py

# 2. 生成初始上下文
python .ai-context/tools/context-generator.py

# 3. 编辑项目概览（可选）
# 手动编辑 .ai-context/docs/project-overview.md
```

### 场景2：日常开发
```bash
# 每天开始工作
python .ai-context/tools/context-generator.py

# 需要AI帮助时，直接使用：
# .ai-context/cache/latest-context.md
```

### 场景3：换电脑工作
```bash
# 1. 拉取代码
git pull

# 2. 刷新上下文
python .ai-context/tools/context-generator.py  

# 3. 查看当前状态
cat .ai-context/cache/latest-context.md

# 4. 开始协作
```

### 场景4：VS Code 中使用
```
1. Ctrl+Shift+P
2. 输入 "Tasks: Run Task"  
3. 选择 "生成AI上下文"
4. 查看生成的 latest-context.md
```

## ✅ 关键文件用途

| 文件 | 用途 | 更新方式 | 使用场景 |
|------|------|----------|----------|
| `latest-context.md` | 给AI的完整项目信息 | 自动生成 | 每次AI协作 |
| `project-overview.md` | 项目整体介绍 | 手动编辑 | 了解项目背景 |
| `context-generator.py` | 上下文生成工具 | 系统工具 | 刷新项目状态 |

## 🚫 简化原则

### 移除复杂功能
- ~~sessions 目录~~（过于复杂）
- ~~status-update.md~~（重复信息）
- ~~smart-refresh.py~~（自动化过度）

### 保留核心功能
- ✅ `latest-context.md` - 核心上下文
- ✅ `project-overview.md` - 项目概览
- ✅ `context-generator.py` - 生成工具
- ✅ VS Code 任务集成

## 🎯 最终建议

### 日常使用只需要：
1. **每天第一次工作**：运行 `生成AI上下文` 任务
2. **需要AI协作**：复制 `latest-context.md` 给AI  
3. **完成里程碑**：更新 `project-overview.md`

### 文件关注优先级：
1. **latest-context.md** - 最重要，每次AI协作必用
2. **project-overview.md** - 次重要，了解项目背景
3. **其他文件** - 工具文件，偶尔关注

---

**核心思想**：让上下文管理成为开发的助力，而不是负担。简单、自动、有用。
