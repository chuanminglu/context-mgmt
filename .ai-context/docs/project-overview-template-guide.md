# 项目概览文档模板使用指南

## 文件说明

### 模板文件
- **`project-overview-template.md`** - 通用项目概览模板
  - 包含占位符（如 `{{PROJECT_NAME}}`）
  - 可用于快速创建新项目的概览文档
  - 支持自动化生成工具

### 示例文件
- **`project-overview-example.md`** - TaskFlow项目示例
  - 展示如何使用模板创建具体项目文档
  - 包含完整的项目描述示例
  - 仅作参考，不代表当前项目

### 当前项目文档
- **`project-overview.md`** - 当前AI上下文管理系统的项目概览
  - 描述当前项目的实际情况
  - 会随项目发展持续更新

## 模板变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{PROJECT_NAME}}` | 项目名称 | "TaskFlow 任务管理系统" |
| `{{PROJECT_TYPE}}` | 项目类型 | "Web应用程序" |
| `{{CREATE_DATE}}` | 创建时间 | "2025-06-28" |
| `{{TECH_STACK}}` | 主要技术栈 | "Python Flask + HTML/CSS/JS" |
| `{{DEV_ENVIRONMENT}}` | 开发环境 | "本地开发，生产部署待定" |
| `{{PROJECT_STRUCTURE}}` | 项目结构 | 目录树结构 |
| `{{CORE_FEATURES}}` | 核心功能 | 功能列表 |
| `{{COMPLETION_PERCENTAGE}}` | 完成度 | "20%（原型验证阶段）" |
| `{{DEVELOPMENT_METHOD}}` | 开发方法 | "快速原型 → 需求验证" |
| `{{COMPLETED_TASKS}}` | 已完成任务 | 带✅的任务列表 |
| `{{NEXT_STEPS}}` | 下一步计划 | 编号列表 |
| `{{METHODOLOGY_REFLECTION}}` | 方法论反思 | 开发方法的总结 |
| `{{TECHNICAL_CONSTRAINTS}}` | 技术约束 | 技术限制和要求 |
| `{{NON_FUNCTIONAL_REQUIREMENTS}}` | 非功能性需求 | 性能、可用性等要求 |
| `{{IMPORTANT_DECISIONS}}` | 重要决策记录 | 编号的决策列表 |

## 使用方法

### 手动使用
1. 复制 `project-overview-template.md` 
2. 替换所有 `{{变量}}` 为实际内容
3. 根据项目需要调整章节结构

### 自动化使用
```python
# 示例：自动替换模板变量
import re

def generate_project_overview(template_path, variables):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for key, value in variables.items():
        content = content.replace(f'{{{{{key}}}}}', str(value))
    
    return content

# 使用示例
variables = {
    'PROJECT_NAME': 'My New Project',
    'PROJECT_TYPE': 'Web Application',
    'CREATE_DATE': '2025-06-28',
    # ... 其他变量
}

result = generate_project_overview('project-overview-template.md', variables)
```

## 最佳实践

1. **保持更新**：项目概览应随项目发展持续更新
2. **简洁明了**：避免过于详细的技术细节
3. **结构化**：使用一致的章节结构便于阅读
4. **版本控制**：将概览文档纳入版本控制
5. **团队协作**：确保团队成员都能理解和更新文档

## 扩展建议

可以根据项目特点添加以下章节：
- **部署说明**：生产环境部署相关信息
- **API文档**：核心API接口概览
- **依赖管理**：主要依赖项和版本要求
- **测试策略**：测试方法和覆盖率目标
- **性能指标**：关键性能指标和监控方案

---
*此文档说明如何使用项目概览模板系统*
