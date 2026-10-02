# Planning
Tool to help manage the plannings of a team.

## Team schedule and on-call planning

This repository now includes a lightweight scheduler in `schedule_tool.py` that can:

- compile team workdays into a single master schedule,
- assign on-call duties fairly based on each member's weekly working hours,
- accept additional assignment rules (constraints) through `add_rule`.

### Quick example

```python
from datetime import date, timedelta
from schedule_tool import TeamMember, TeamScheduler, display_schedule

members = [
    TeamMember("Alice", {0, 1, 2, 3, 4}, 40),
    TeamMember("Bob", {0, 1, 2, 3, 4}, 20),
]

scheduler = TeamScheduler(members)
week = [date(2026, 10, 5) + timedelta(days=i) for i in range(5)]
master_schedule = scheduler.compile_schedule(week)
print(display_schedule(master_schedule))
```

### Run tests

```bash
python -m unittest discover -s tests -q
```
