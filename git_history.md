# Git History

## 2026-02-19

### Changes
- booking.py: 新增统一入口文件，支持单用户预订和批量预订模式，使用threading实现并行执行
- config.json: 新增批量预订配置文件，包含用户列表和通用设置
- multi_jinze.py: 重构为调用booking.py，修复了原本调用jinze_rob.py的错误
- CLAUDE.md: 更新文档说明新的使用方式
- .claude/settings.local.json: Added 4 new allowed Bash commands (zip -r, unzip -l, unzip -p, ls)
- .claude/settings.local.json: Added 2 new allowed Bash commands (git commit, git push) [previous]
- .claude/skills/daily-report.md: Deleted skill file [previous]
- project_process.md: Deleted [previous]

### Stats
- 6 files changed, 196 insertions(+), 35 deletions(-)
