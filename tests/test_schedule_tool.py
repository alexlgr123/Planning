import unittest
from datetime import date, timedelta

from schedule_tool import TeamMember, TeamScheduler, display_schedule


def _work_week(start: date):
    return [start + timedelta(days=offset) for offset in range(5)]


class SchedulerTests(unittest.TestCase):
    def test_compiles_workdays_and_assigns_on_call_by_working_hours(self):
        week = _work_week(date(2026, 10, 5))
        scheduler = TeamScheduler(
            members=[
                TeamMember("Alice", {0, 1, 2, 3, 4}, 40),
                TeamMember("Bob", {0, 1, 2, 3, 4}, 20),
            ]
        )

        schedule = scheduler.compile_schedule(week)

        on_calls = [schedule[day]["on_call"] for day in week]
        self.assertGreater(on_calls.count("Alice"), on_calls.count("Bob"))
        self.assertTrue(all(schedule[day]["working_members"] == ["Alice", "Bob"] for day in week))

    def test_supports_custom_constraints_for_on_call_assignments(self):
        week = _work_week(date(2026, 10, 5))
        scheduler = TeamScheduler(
            members=[
                TeamMember("Alice", {0, 1, 2, 3, 4}, 40),
                TeamMember("Bob", {0, 1, 2, 3, 4}, 40),
            ]
        )

        blocked_day = week[2]
        scheduler.add_rule(lambda candidate, day, _: not (candidate == "Alice" and day == blocked_day))

        schedule = scheduler.compile_schedule(week)

        self.assertEqual(schedule[blocked_day]["on_call"], "Bob")

    def test_display_schedule_formats_master_view(self):
        day = date(2026, 10, 5)
        scheduler = TeamScheduler(
            members=[
                TeamMember("Alice", {0, 1, 2, 3, 4}, 40),
            ]
        )

        rendered = display_schedule(scheduler.compile_schedule([day]))

        self.assertIn("Date | Working Members | On Call", rendered)
        self.assertIn("2026-10-05 | Alice | Alice", rendered)


if __name__ == "__main__":
    unittest.main()
