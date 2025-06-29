# VS Code插件开发指南 - AI上下文管理系统

## 1. VS Code插件技术架构

### 1.1 核心概念

VS Code插件（Extensions）是基于**Node.js**和**TypeScript**的模块化应用，运行在VS Code的扩展宿主进程中。

#### 关键组件
- **Extension Host Process**：独立的Node.js进程，运行插件代码
- **VS Code API**：提供与编辑器交互的接口
- **Extension Manifest**：`package.json`文件，定义插件元数据和能力
- **Activation Events**：触发插件激活的事件

### 1.2 架构层次

```
┌─────────────────────────────────────┐
│          VS Code 主进程              │
│  ┌─────────────────────────────────┐ │
│  │      渲染进程 (Electron)        │ │
│  │  ┌─────────────────────────────┐│ │
│  │  │    编辑器 UI               ││ │
│  │  │    侧边栏、面板             ││ │
│  │  │    命令面板                ││ │
│  │  └─────────────────────────────┘│ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
            │ IPC 通信
┌─────────────────────────────────────┐
│      Extension Host Process        │
│  ┌─────────────────────────────────┐ │
│  │    你的插件代码 (TypeScript)    │ │
│  │    ├── activation.ts          │ │
│  │    ├── commands.ts            │ │
│  │    ├── providers/             │ │
│  │    └── utils/                 │ │
│  └─────────────────────────────────┘ │
│  ┌─────────────────────────────────┐ │
│  │       VS Code API             │ │
│  │    vscode.window              │ │
│  │    vscode.workspace           │ │
│  │    vscode.commands            │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 1.3 文件结构

标准VS Code插件项目结构：
```
ai-context-extension/
├── src/                        # TypeScript源码
│   ├── extension.ts            # 插件入口点
│   ├── commands/               # 命令实现
│   ├── providers/              # 内容提供者
│   ├── views/                  # 自定义视图
│   └── utils/                  # 工具函数
├── package.json                # 插件清单
├── tsconfig.json              # TypeScript配置
├── webpack.config.js          # 打包配置
├── .vscodeignore              # 发布时忽略的文件
├── CHANGELOG.md               # 变更日志
├── README.md                  # 说明文档
└── out/                       # 编译输出（Git忽略）
```

### 1.4 关键API类别

#### 窗口和编辑器API
```typescript
import * as vscode from 'vscode';

// 显示信息
vscode.window.showInformationMessage('Hello');

// 获取活动编辑器
const editor = vscode.window.activeTextEditor;

// 创建输出通道
const output = vscode.window.createOutputChannel('AI Context');
```

#### 工作区API
```typescript
// 获取工作区文件夹
const workspaceFolders = vscode.workspace.workspaceFolders;

// 文件系统操作
const uri = vscode.Uri.file('/path/to/file');
const content = await vscode.workspace.fs.readFile(uri);

// 监听文件变化
vscode.workspace.onDidChangeTextDocument(event => {
    // 处理文件变化
});
```

#### 命令和贡献点
```typescript
// 注册命令
vscode.commands.registerCommand('ai-context.generate', () => {
    // 命令实现
});

// 状态栏
const statusBar = vscode.window.createStatusBarItem();
statusBar.text = "$(sync~spin) Generating...";
```

## 2. 当前项目升级步骤

### 2.1 项目结构转换

#### 阶段1：创建插件基础结构
1. **初始化插件项目**
   ```bash
   npm install -g yo generator-code
   yo code  # 选择"New Extension (TypeScript)"
   ```

2. **迁移现有Python代码逻辑**
   - 将Python的项目检测逻辑转换为TypeScript
   - 保留核心算法，适配Node.js文件系统API
   - 重构为VS Code API兼容的模块

#### 阶段2：实现核心功能
1. **文件扫描和分析**
   ```typescript
   // 替换Python的pathlib
   import * as vscode from 'vscode';
   import * as path from 'path';
   
   async function scanWorkspace(): Promise<FileInfo[]> {
       const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
       // 实现扫描逻辑
   }
   ```

2. **上下文生成**
   ```typescript
   // 替换Python的文件操作
   async function generateContext(): Promise<string> {
       // 使用VS Code API生成上下文
   }
   ```

#### 阶段3：UI集成
1. **命令面板集成**
2. **侧边栏视图**
3. **状态栏指示器**
4. **快捷键绑定**

### 2.2 技术栈映射

| Python项目 | VS Code插件 | 说明 |
|------------|-------------|------|
| `pathlib.Path` | `vscode.Uri` + `path` | 文件路径处理 |
| `json.load()` | `JSON.parse()` | JSON处理 |
| `subprocess.run()` | `child_process.exec()` | 执行外部命令 |
| `datetime` | `Date` | 时间处理 |
| 文件读写 | `vscode.workspace.fs` | 文件系统操作 |
| 命令行参数 | `vscode.commands` | 命令系统 |

## 3. 功能规划

### 3.1 核心功能模块

#### 📁 文件管理模块
- **功能**：智能扫描工作区文件
- **实现**：`src/core/fileScanner.ts`
- **UI**：侧边栏文件树视图

#### 🔄 上下文生成模块
- **功能**：自动生成项目上下文
- **实现**：`src/core/contextGenerator.ts`
- **UI**：命令面板 + 进度条

#### ⚙️ 配置管理模块
- **功能**：用户配置和项目设置
- **实现**：`src/config/settingsManager.ts`
- **UI**：设置页面

#### 📝 模板系统模块
- **功能**：可定制的输出模板
- **实现**：`src/templates/templateEngine.ts`
- **UI**：模板编辑器

#### 🔗 集成模块
- **功能**：与Git、任务系统集成
- **实现**：`src/integrations/`
- **UI**：状态栏 + 通知

### 3.2 用户界面设计

#### 侧边栏视图
```
AI Context Manager
├── 📊 Project Overview
├── 📁 Important Files (12)
│   ├── 📄 package.json
│   ├── 📄 tsconfig.json
│   └── 📄 README.md
├── 🔄 Recent Changes (3)
│   ├── ✏️  src/extension.ts (2h ago)
│   └── ➕ src/commands/generate.ts (5h ago)
└── ⚙️ Settings
    ├── 🎯 Auto-generate triggers
    ├── 📝 Output templates
    └── 🔗 Integrations
```

#### 命令面板命令
- `AI Context: Generate Project Context`
- `AI Context: Refresh Cache`
- `AI Context: Open Settings`
- `AI Context: Export Context`
- `AI Context: Create Template`

#### 状态栏
```
$(sync~spin) Generating context... | AI Context: Ready ✓
```

### 3.3 功能优先级

#### 🔥 Phase 1 - MVP (最小可行产品)
1. ✅ 基础项目扫描
2. ✅ 简单上下文生成
3. ✅ 命令面板集成
4. ✅ 基础配置

#### 🚀 Phase 2 - 增强功能
1. 🔄 侧边栏视图
2. 📝 模板系统
3. ⚡ 智能缓存
4. 🔗 Git集成

#### 🌟 Phase 3 - 高级功能
1. 🤖 AI对话集成
2. 🔄 实时监控
3. 👥 团队协作
4. 📊 使用统计

## 4. 部署和发布流程

### 4.1 开发环境配置

#### 必需工具
```bash
# 1. Node.js (推荐LTS版本)
node --version  # v18.x.x+

# 2. VS Code
code --version

# 3. 插件开发工具
npm install -g yo generator-code vsce

# 4. TypeScript
npm install -g typescript
```

#### 开发工作流
```bash
# 1. 克隆/创建项目
git clone <repository>

# 2. 安装依赖
npm install

# 3. 开发模式
npm run compile-watch  # 监听TypeScript编译

# 4. 调试
F5 # 启动Extension Development Host
```

### 4.2 构建流程

#### package.json 脚本
```json
{
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "compile-watch": "tsc -watch -p ./",
    "pretest": "npm run compile && npm run lint",
    "lint": "eslint src --ext ts",
    "test": "node ./out/test/runTest.js",
    "package": "vsce package",
    "publish": "vsce publish"
  }
}
```

#### 构建配置
```typescript
// tsconfig.json
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

### 4.3 测试策略

#### 单元测试
```typescript
// src/test/suite/extension.test.ts
import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
    test('Context generation', async () => {
        const context = await generateContext();
        assert.ok(context.length > 0);
    });
});
```

#### 集成测试
```bash
# 运行测试
npm run test

# 覆盖率报告
npm run coverage
```

### 4.4 发布流程

#### 版本发布步骤

1. **准备发布**
   ```bash
   # 更新版本号
   npm version patch  # 或 minor/major
   
   # 更新CHANGELOG.md
   git add CHANGELOG.md
   git commit -m "Update changelog for v1.0.1"
   ```

2. **打包插件**
   ```bash
   # 生成 .vsix 文件
   vsce package
   
   # 输出：ai-context-manager-1.0.1.vsix
   ```

3. **本地测试**
   ```bash
   # 安装到本地VS Code
   code --install-extension ai-context-manager-1.0.1.vsix
   ```

4. **发布到市场**
   ```bash
   # 需要先获取Personal Access Token
   vsce login <publisher-name>
   
   # 发布
   vsce publish
   ```

#### 发布渠道

##### 🏪 VS Code Marketplace（官方）
- **优势**：最大用户群，官方认可
- **要求**：严格审核，需要微软账号
- **流程**：
  1. 创建Azure DevOps账号
  2. 获取Personal Access Token
  3. 使用`vsce publish`发布

##### 📦 Open VSX Registry（开源）
- **优势**：开源友好，无审核
- **要求**：GitHub账号
- **流程**：
  ```bash
  npm install -g ovsx
  ovsx publish ai-context-manager-1.0.1.vsix
  ```

##### 🔗 私有分发
- **方式**：直接分发`.vsix`文件
- **适用**：企业内部、测试版本

### 4.5 持续集成

#### GitHub Actions 配置
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
      with:
        node-version: 18
    - run: npm ci
    - run: npm run lint
    - run: npm run test
    - run: npm run package
```

## 5. 迁移策略

### 5.1 渐进式迁移

#### 阶段1：并行开发（推荐）
- 保留现有Python工具
- 创建新的VS Code插件项目
- 逐步实现功能对等
- 用户可以选择使用方式

#### 阶段2：功能增强
- 插件添加Python工具不具备的UI功能
- 保持核心算法一致性
- 提供迁移工具

#### 阶段3：统一替换
- 插件功能完全成熟后
- 提供迁移指南
- 逐步弃用Python工具

### 5.2 兼容性保证

#### 配置文件兼容
```typescript
// 读取现有配置
const legacyConfig = await readLegacyConfig('.ai-context/context-config.json');
const modernConfig = migrateConfig(legacyConfig);
```

#### 输出格式兼容
```typescript
// 保持相同的输出格式
interface ContextOutput {
    projectInfo: ProjectInfo;
    files: FileInfo[];
    structure: ProjectStructure;
    // 与Python版本保持一致
}
```

## 6. 风险评估与缓解

### 6.1 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| TypeScript学习曲线 | 中 | 中 | 1. 渐进式学习<br>2. 参考现有项目<br>3. 社区支持 |
| VS Code API限制 | 低 | 高 | 1. 详细API研究<br>2. 备选方案设计 |
| 性能问题 | 中 | 中 | 1. 异步处理<br>2. 缓存策略<br>3. 渐进式加载 |
| 兼容性问题 | 低 | 中 | 1. 多版本测试<br>2. 向后兼容设计 |

### 6.2 市场风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 用户接受度 | 中 | 高 | 1. MVP快速验证<br>2. 用户反馈收集<br>3. 迭代改进 |
| 竞品冲击 | 低 | 中 | 1. 差异化功能<br>2. 持续创新 |
| 生态系统变化 | 低 | 高 | 1. 关注VS Code路线图<br>2. 灵活架构设计 |

### 6.3 缓解策略

#### 技术缓解
1. **原型验证**：先开发简化版本验证可行性
2. **模块化设计**：核心逻辑与UI分离
3. **测试覆盖**：保证功能正确性

#### 产品缓解
1. **用户调研**：了解真实需求
2. **分阶段发布**：降低单次发布风险
3. **社区建设**：建立用户反馈渠道

## 7. 项目时间线

### 第1周：项目设置和基础架构
- [ ] 创建VS Code插件项目
- [ ] 配置开发环境
- [ ] 设计项目架构
- [ ] 创建基础文件结构

### 第2-3周：核心功能开发
- [ ] 实现文件扫描功能
- [ ] 移植项目检测逻辑
- [ ] 开发上下文生成器
- [ ] 基础命令集成

### 第4周：UI开发
- [ ] 侧边栏视图
- [ ] 命令面板集成
- [ ] 状态栏指示器
- [ ] 基础设置页面

### 第5周：测试和优化
- [ ] 单元测试编写
- [ ] 集成测试
- [ ] 性能优化
- [ ] 用户体验改进

### 第6周：发布准备
- [ ] 文档编写
- [ ] 打包测试
- [ ] 市场发布
- [ ] 用户反馈收集

---

**下一步行动**：
1. 阅读并确认技术方案
2. 开始创建VS Code插件项目基础结构
3. 设置开发环境和工具链
