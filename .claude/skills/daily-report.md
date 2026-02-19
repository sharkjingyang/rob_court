---
name: daily-report
description: 自动总结当天修改的代码并生成每日报告
---

# 每日报告技能

此技能将自动查找今天修改的 Python 文件，分析其内容，并生成每日报告。

## 执行步骤

### 1. 查找今天修改的 Python 文件
使用 PowerShell 命令查找今天修改的所有 .py 文件：
```powershell
Get-ChildItem -Path . -Recurse -Filter "*.py" -File | Where-Object { $_.LastWriteTime.Date -eq (Get-Date).Date } | Select-Object -ExpandProperty FullName
```

### 2. 分析每个文件
对于每个找到的 Python 文件：
- 读取文件内容
- 提取顶级的函数定义（def 开头的行）
- 提取顶级的类定义（class 开头的行）
- 识别文件的主要用途（通过检查文件开头的注释或 docstring）

### 3. 生成报告
将分析结果写入 `daily_report.md`，格式如下：

```markdown
# 每日报告 - YYYY年MM月DD日

## 修改的文件

### filename.py
- **路径**: relative_path
- **主要功能**: 简要描述文件的主要用途
- **函数**: function1, function2
- **类**: Class1, Class2

---
*报告生成时间: HH:MM:SS*
```

## 输出
- 报告文件: `daily_report.md`（项目根目录）
- 使用 Python 脚本完成文件分析和报告生成
