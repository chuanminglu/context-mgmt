# VS Code插件开发 - 快速开始检查清单

## 📋 环境检查清单

### ✅ 必需工具检查

#### 1. Node.js 环境
```bash
# 检查Node.js版本（需要v18.x或更高）
node --version

# 检查npm版本
npm --version

# 如果版本过低，请更新
# Windows: 下载最新LTS版本从 https://nodejs.org/
# 或使用包管理器: winget install OpenJS.NodeJS
```

#### 2. VS Code 开发工具
```bash
# 检查VS Code版本
code --version

# 安装插件开发必需工具
npm install -g yo generator-code vsce typescript

# 验证安装
yo --version
vsce --version
tsc --version
```

#### 3. Git 环境
```bash
# 检查Git版本
git --version

# 配置基本信息（如果尚未配置）
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### ✅ VS Code 插件开发必备知识

#### 1. TypeScript 基础 ⭐⭐⭐
- [ ] 理解基本类型系统
- [ ] 熟悉接口和类
- [ ] 了解异步编程（Promise/async-await）
- [ ] 掌握模块导入导出

#### 2. Node.js 基础 ⭐⭐
- [ ] 文件系统操作（fs模块）
- [ ] 路径处理（path模块）
- [ ] 事件系统（EventEmitter）
- [ ] 流（Streams）基础

#### 3. VS Code API 了解 ⭐⭐⭐
- [ ] 扩展激活机制
- [ ] 命令系统
- [ ] 工作区API
- [ ] 树视图提供者

## 🚀 项目创建步骤

### 步骤1：创建插件项目
```bash
# 进入工作目录
cd c:\Programs\ai-contextmgmt\

# 运行Yeoman生成器
yo code

# 回答以下问题：
# ? What type of extension do you want to create? 
#   → New Extension (TypeScript)
# ? What's the name of your extension? 
#   → AI Context Manager
# ? What's the identifier of your extension? 
#   → ai-context-manager  
# ? What's the description of your extension? 
#   → Intelligent AI context management for development projects
# ? Initialize a git repository? 
#   → Yes
# ? Bundle the source code with webpack? 
#   → Yes
# ? Package manager to use? 
#   → npm
```

### 步骤2：项目初始设置
```bash
# 进入项目目录
cd ai-context-manager

# 安装依赖
npm install

# 测试项目是否正常
npm run compile

# 在VS Code中打开项目
code .
```

### 步骤3：第一次运行测试
```bash
# 按F5启动Extension Development Host
# 或在命令面板中选择 "Debug: Start Debugging"

# 在新窗口中测试示例命令
# Ctrl+Shift+P → "Hello World"
```

## 📝 项目结构理解

### 🔍 关键文件说明

#### `package.json` - 插件清单
```json
{
  "name": "ai-context-manager",           // 插件ID
  "displayName": "AI Context Manager",    // 显示名称
  "description": "...",                   // 描述
  "version": "0.0.1",                    // 版本
  "engines": {
    "vscode": "^1.74.0"                  // VS Code最低版本要求
  },
  "categories": ["Other"],               // 分类
  "activationEvents": [],                // 激活事件
  "main": "./out/extension.js",          // 入口文件
  "contributes": {                       // 贡献点
    "commands": [...],                   // 命令
    "menus": [...],                      // 菜单
    "views": [...]                       // 视图
  }
}
```

#### `src/extension.ts` - 插件入口
```typescript
import * as vscode from 'vscode';

// 插件激活时调用
export function activate(context: vscode.ExtensionContext) {
    console.log('Extension "ai-context-manager" is now active!');
    
    // 注册命令
    let disposable = vscode.commands.registerCommand('ai-context-manager.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from AI Context Manager!');
    });

    context.subscriptions.push(disposable);
}

// 插件停用时调用
export function deactivate() {}
```

#### `tsconfig.json` - TypeScript配置
```json
{
    "compilerOptions": {
        "module": "commonjs",
        "target": "ES2020",
        "outDir": "out",
        "lib": ["ES2020"],
        "sourceMap": true,
        "rootDir": "src",
        "strict": true
    }
}
```

## 🎯 迁移策略选择

### 选项1：渐进式迁移（推荐）⭐⭐⭐
```
优势：
✅ 风险较低，可随时回退
✅ 保持现有工具可用
✅ 逐步验证功能对等性
✅ 用户可选择使用方式

劣势：
❌ 需要维护两套代码
❌ 迁移周期较长
```

### 选项2：一次性替换 ⭐⭐
```
优势：
✅ 快速完成迁移
✅ 统一技术栈
✅ 避免重复维护

劣势：
❌ 风险较高
❌ 可能影响现有用户
❌ 调试周期长
```

### 选项3：混合模式 ⭐⭐⭐
```
优势：
✅ VS Code插件调用Python工具
✅ 快速实现UI集成
✅ 保持核心逻辑稳定

劣势：
❌ 依赖外部Python环境
❌ 部署复杂度增加
```

## 📊 功能优先级规划

### 🔥 第一优先级（MVP）
- [ ] **基础文件扫描**：扫描工作区重要文件
- [ ] **简单上下文生成**：生成基本项目信息
- [ ] **命令面板集成**：`AI Context: Generate`命令
- [ ] **输出显示**：在输出面板显示结果

### ⚡ 第二优先级（增强）
- [ ] **侧边栏视图**：树形显示项目结构
- [ ] **状态栏集成**：显示当前状态
- [ ] **配置系统**：用户可配置选项
- [ ] **缓存机制**：提升性能

### 🌟 第三优先级（高级）
- [ ] **Web视图集成**：富文本显示
- [ ] **Git集成**：显示变更历史
- [ ] **智能刷新**：文件变化自动更新
- [ ] **导出功能**：多格式导出

## 🔧 开发工作流

### 日常开发流程
```bash
# 1. 启动监听编译
npm run watch

# 2. 启动调试（F5）
# 在Extension Development Host中测试

# 3. 代码修改后自动重编译
# 在调试窗口中重启插件：Ctrl+R

# 4. 运行测试
npm test

# 5. 检查代码质量
npm run lint
```

### 调试技巧
```typescript
// 1. 使用console.log输出调试信息
console.log('Debug info:', data);

// 2. 使用VS Code的输出通道
const outputChannel = vscode.window.createOutputChannel('AI Context');
outputChannel.appendLine('Debug message');
outputChannel.show();

// 3. 使用断点调试
// 在Extension Development Host中按F12打开开发者工具
```

## ⚠️ 常见问题和解决方案

### 问题1：编译错误
```
错误：Cannot find module 'vscode'
解决：确保已安装@types/vscode依赖
npm install --save-dev @types/vscode
```

### 问题2：命令不显示
```
错误：注册的命令在命令面板中不显示
解决：检查package.json中的contributes.commands配置
确保command ID匹配
```

### 问题3：插件未激活
```
错误：插件代码未执行
解决：检查activationEvents配置
添加"onStartupFinished"或特定事件
```

### 问题4：TypeScript类型错误
```
错误：类型检查失败
解决：
1. 检查tsconfig.json配置
2. 确保导入正确的类型
3. 使用严格模式逐步修复
```

## 📚 学习资源

### 官方文档
- [VS Code Extension API](https://code.visualstudio.com/api)
- [Extension Guidelines](https://code.visualstudio.com/api/references/extension-guidelines)
- [Publishing Extensions](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)

### 示例项目
- [VS Code Extension Samples](https://github.com/microsoft/vscode-extension-samples)
- [Popular Extensions Source](https://github.com/topics/vscode-extension)

### TypeScript学习
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TypeScript in 5 minutes](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html)

## ✅ 开始前的最终检查

### 环境确认
- [ ] Node.js v18+ 已安装
- [ ] VS Code 最新版本
- [ ] 开发工具已安装 (yo, generator-code, vsce)
- [ ] Git 配置完成

### 技能准备
- [ ] TypeScript 基础语法了解
- [ ] Node.js 文件操作熟悉
- [ ] VS Code 基本使用熟练
- [ ] 已阅读VS Code插件架构文档

### 项目准备
- [ ] 现有Python代码逻辑梳理完成
- [ ] 功能优先级确定
- [ ] 时间计划制定
- [ ] 测试策略确定

---

## 🚀 立即开始

如果以上检查全部完成，你可以立即开始：

1. **运行项目生成器**
   ```bash
   cd c:\Programs\ai-contextmgmt\
   yo code
   ```

2. **创建第一个功能**
   - 从文件扫描功能开始
   - 实现基础的项目检测
   - 添加简单的命令面板命令

3. **设置开发环境**
   - 配置调试启动
   - 设置自动编译监听
   - 准备测试环境

**下一步**：开始创建VS Code插件项目！
