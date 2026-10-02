from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Set


Rule = Callable[[str, date, Mapping[str, object]], bool]


@dataclass(frozen=True)
class TeamMember:
    name: str
    working_days: Set[int]
    weekly_hours: float

    def works_on(self, day: date) -> bool:
        return day.weekday() in self.working_days


class TeamScheduler:
    def __init__(self, members: Sequence[TeamMember], rules: Optional[Iterable[Rule]] = None):
        if not members:
            raise ValueError("At least one team member is required")

        self.members = list(members)
        self._hours_by_member = {member.name: member.weekly_hours for member in members}
        self._rules: List[Rule] = list(rules or [])

        if len(self._hours_by_member) != len(self.members):
            raise ValueError("Member names must be unique")

        if any(hours <= 0 for hours in self._hours_by_member.values()):
            raise ValueError("Weekly hours must be greater than zero")

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def compile_schedule(self, days: Sequence[date]) -> Dict[date, Dict[str, object]]:
        assignments_count = {member.name: 0 for member in self.members}
        compiled: Dict[date, Dict[str, object]] = {}

        for day in sorted(days):
            available = [member.name for member in self.members if member.works_on(day)]
            context: Dict[str, object] = {
                "available": available,
                "assignments_count": assignments_count,
                "hours_by_member": self._hours_by_member,
            }
            on_call = self._select_on_call(day, available, assignments_count, context)
            if on_call is not None:
                assignments_count[on_call] += 1

            compiled[day] = {
                "working_members": available,
                "on_call": on_call,
            }

        return compiled

    def _select_on_call(
        self,
        day: date,
        available: Sequence[str],
        assignments_count: Mapping[str, int],
        context: Mapping[str, object],
    ) -> Optional[str]:
        allowed = [
            candidate
            for candidate in available
            if all(rule(candidate, day, context) for rule in self._rules)
        ]

        if not allowed:
            return None

        return min(
            allowed,
            key=lambda candidate: (
                assignments_count[candidate] / self._hours_by_member[candidate],
                assignments_count[candidate],
                candidate,
            ),
        )


def display_schedule(schedule: Mapping[date, Mapping[str, object]]) -> str:
    rows = ["Date | Working Members | On Call", "--- | --- | ---"]
    for day in sorted(schedule):
        entry = schedule[day]
        members = ", ".join(entry["working_members"]) if entry["working_members"] else "-"
        on_call = entry["on_call"] if entry["on_call"] else "-"
        rows.append(f"{day.isoformat()} | {members} | {on_call}")
    return "\n".join(rows)
