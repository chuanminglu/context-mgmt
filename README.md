# AI上下文管理系统 (Context Management System)

[![版本](https://img.shields.io/badge/版本-v2.0.0-blue.svg)](https://github.com/windlu/ai-contextmgmt-py)
[![Python](https://img.shields.io/badge/Python-3.7+-green.svg)](https://python.org)
[![许可证](https://img.shields.io/badge/许可证-MIT-orange.svg)](LICENSE)

一个强大的AI上下文管理系统，专为AI协作和开发工作流程优化而设计。自动扫描项目结构，生成智能上下文，支持工作会话管理和VS Code深度集成。

## 🎯 核心特性

### ✅ **已完成功能**
- **🔄 自动上下文生成**：智能扫描项目结构和文件内容
- **📋 工作会话管理**：追踪开发会话，关联文件修改历史
- **🚀 VS Code深度集成**：15+个任务，支持参数化和交互式操作
- **⚡ 智能刷新机制**：基于文件变更的增量更新
- **🎨 多种操作模式**：命令行、交互式、VS Code任务三种方式
- **📊 配置化扫描**：支持项目特定的扫描配置
- **🔄 自动化工作流**：开始/结束会话时自动更新上下文
- **📝 多格式输出**：支持简洁和详细两种文档格式

### 🔄 **规划中功能**
- **🧩 VS Code扩展**：图形化界面和增强体验
- **🌐 MCP服务器集成**：支持模型上下文协议
- **📦 CLI工具打包**：独立可安装的命令行工具

## 🚀 快速开始

### 1. 基本使用

```bash
# 生成AI上下文（获取项目当前状态）
python .ai-context/tools/context-generator.py

# 开始工作会话
python .ai-context/tools/session-manager.py start "功能开发" -d "实现用户登录功能"

# 查看当前会话状态
python .ai-context/tools/session-manager.py status

# 结束工作会话（自动更新上下文）
python .ai-context/tools/session-manager.py end
```

### 2. VS Code任务（推荐）

使用 `Ctrl+Shift+P` → `Tasks: Run Task` 选择：

#### 🎯 **上下文管理任务**
- **生成AI上下文**：需要AI协作时使用
- **智能上下文检查**：检查是否需要更新
- **自动上下文刷新**：让系统智能判断
- **强制上下文刷新**：解决缓存问题

#### 📋 **会话管理任务**
- **开始工作会话**：下拉选择常见类型（代码重构、功能开发等）
- **开始工作会话（自定义）**：完全自由输入标题
- **快速开始：代码重构/功能开发/Bug修复**：一键启动常见场景
- **开始工作会话（交互式）**：终端中逐步输入，最灵活
- **结束工作会话**：直接结束当前会话
- **结束工作会话（确认）**：显示会话信息后确认结束
- **更新会话进展**：快速记录工作进度
- **查看工作会话**：列出最近的会话历史

## 🎪 多种操作模式

### 1. **快速命令行模式**
```bash
# 直接指定参数
python .ai-context/tools/session-manager.py start "API重构" -d "优化现有API性能"
```

### 2. **交互式模式**
```bash
# 逐步引导输入
python .ai-context/tools/session-manager.py start -i
```

### 3. **VS Code任务模式**
- **参数化输入**：支持下拉选择和文本输入
- **预设场景**：常见工作类型一键启动
- **图形化操作**：无需记忆命令行参数

## 📁 项目结构

```
.ai-context/
├── tools/              # 🛠️ 核心工具脚本
│   ├── context-generator.py      # 上下文生成器
│   ├── session-manager.py        # 工作会话管理器
│   ├── smart-refresh.py          # 智能刷新工具
│   └── project_detector.py       # 项目类型检测器
├── sessions/           # 📋 工作会话数据
│   └── session-*.json            # 会话记录文件
├── docs/               # 📚 项目文档
│   ├── context-management-guide.md     # 完整使用指南
│   └── project-overview.md             # 项目概览
├── cache/              # 🗂️ 自动生成缓存
│   └── latest-context.md              # 最新上下文（核心输出）
├── templates/          # 📄 系统模板
│   ├── session-starter.md             # AI协作会话模板
│   └── project-overview-template.md   # 项目概览模板
└── context-config.json # ⚙️ 配置文件
```

## 🔧 配置说明

### 基本配置 (`context-config.json`)

```json
{
  "recent_files": {
    "days_threshold": 7,        // 最近修改文件的时间范围（天）
    "max_depth": 3,             // 扫描目录的最大深度
    "include_hidden_dirs": false
  },
  "scanning": {
    "max_depth": 3,
    "exclude_dirs": ["__pycache__", "node_modules", ".git"],
    "important_extensions": [".py", ".js", ".md", ".json"]
  }
}
```

### 项目特定配置

系统自动检测项目类型并应用相应配置：
- `python_project`：Python项目优化
- `web_project`：Web开发项目
- `context-management-system`：本系统特定配置

## 🎯 典型工作流程

### 日常开发流程
```
📅 开始工作
    ↓
🟢 开始工作会话 ← 设定今天要做什么（自动生成上下文）
    ↓
💻 编码开发... ← 正常开发工作
    ↓
📊 生成AI上下文 ← 需要AI协作时（包含会话信息）
    ↓
🤖 与AI协作 ← 使用latest-context.md
    ↓
📝 更新会话进展 ← 记录阶段性成果（可选）
    ↓
🔴 结束工作会话 ← 完成工作（自动更新上下文）
```

### AI协作流程
1. **开始会话**：`开始工作会话` → 输入"用户认证重构"
2. **获取上下文**：系统自动生成包含项目状态的上下文
3. **AI协作**：将 `latest-context.md` 内容提供给AI
4. **继续开发**：根据AI建议进行开发
5. **记录进展**：`更新会话进展` → 输入完成情况
6. **结束会话**：`结束工作会话` → 自动更新最终上下文

## 📊 输出示例

### 生成的上下文文件 (`latest-context.md`)
```markdown
# 项目上下文总结
生成时间: 2025-06-29 12:00:00

## 项目信息
- 名称: my-project
- 类型: python_project  
- 技术栈: Python, FastAPI, SQLAlchemy

## 最近修改的文件:
✅ [会话] 用户认证重构 (11:30-12:00)
   📝 重构用户登录逻辑，添加JWT支持
   - src/auth/login.py (11:45)
   - src/models/user.py (11:30)

📄 其他修改:
- requirements.txt (2025-06-29 10:15)
- README.md (2025-06-29 09:30)
```

## 🔍 高级功能

### 智能文件分组
- **会话关联**：文件修改自动关联到对应工作会话
- **时间窗口**：可配置的最近修改文件时间范围
- **智能过滤**：自动排除临时文件和缓存文件

### 多项目支持
- **项目类型检测**：自动识别Python、Node.js、Web等项目类型
- **配置继承**：基础配置+项目特定配置的合并机制
- **扫描优化**：根据项目类型优化扫描策略

### VS Code深度集成
- **15+个任务**：覆盖上下文管理和会话管理的全流程
- **参数化支持**：下拉选择、文本输入、预设场景
- **交互式模式**：终端中的友好输入体验

## 🤝 开发贡献

### 环境要求
- Python 3.7+
- VS Code（推荐）
- Git

### 本地开发
```bash
# 克隆项目
git clone https://github.com/windlu/ai-contextmgmt-py.git
cd ai-contextmgmt-py/context-mgmt

# 运行测试
python .ai-context/tools/context-generator.py

# 开始会话测试功能
python .ai-context/tools/session-manager.py start "测试功能" -d "验证系统功能"
```

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🔗 相关链接

- **完整文档**：[Context Management Guide](.ai-context/docs/context-management-guide.md)
- **项目概览**：[Project Overview](.ai-context/docs/project-overview.md)  
- **问题反馈**：[GitHub Issues](https://github.com/windlu/ai-contextmgmt-py/issues)

---

**🎉 让AI协作更智能，让开发工作流程更高效！**

*本项目专注于提供最佳的AI上下文管理体验，支持多种工作方式和深度的VS Code集成。*
