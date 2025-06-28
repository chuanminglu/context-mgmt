# Context Management System

这是一个独立的AI上下文管理系统项目，专门用于开发和测试上下文管理功能。

## 项目目标

- 开发通用的AI上下文管理工具
- 支持VS Code扩展
- 支持MCP集成
- 提供CLI工具

## 功能特性

- ✅ 自动项目扫描和上下文生成
- ✅ 智能刷新机制
- ✅ VS Code任务集成
- ✅ 多种文档输出格式
- 🔄 计划开发：VS Code扩展
- 🔄 计划开发：MCP服务器

## 使用方法

### 生成上下文
```bash
python .ai-context/tools/context-generator.py
```

### 智能检查
```bash
python .ai-context/tools/smart-refresh.py --check
```

### VS Code 任务
- Ctrl+Shift+P → "Tasks: Run Task" → 选择对应任务

## 目录结构

```
.ai-context/
├── tools/          # 核心工具
├── docs/           # 文档
├── cache/          # 缓存文件
├── templates/      # 模板文件
├── backup/         # 备份文件
└── README.md       # 使用指南
```

## 开发计划

1. **完善现有功能**：优化生成算法、增强智能检查
2. **VS Code扩展**：开发用户友好的扩展界面
3. **MCP集成**：实现标准化AI协作协议
4. **CLI工具**：打包为可安装的命令行工具

---

*这是从 TaskFlow 项目中提取的上下文管理功能的独立版本*
