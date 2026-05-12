from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


def _clamp(value: float, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, round(value)))


@dataclass(slots=True)
class StudentSuccessService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return json.loads(self.source_path.read_text(encoding="utf-8"))

    def score_student(self, student: dict[str, Any]) -> dict[str, Any]:
        attendance = student["attendance_rate"] * 100
        assignments = student["assignment_completion_rate"] * 100
        grade = student["average_grade"]
        lms = student["lms_activity_score"]
        notes_penalty = student["advisor_notes"] * 4
        flags_penalty = student["support_flags"] * 8
        login_penalty = student["days_since_last_login"] * 2.1
        financial_penalty = 14 if student["financial_hold"] else 0

        momentum_score = _clamp(attendance * 0.25 + assignments * 0.28 + grade * 0.22 + lms * 0.25)
        risk_score = _clamp(
            100
            - (
                attendance * 0.24
                + assignments * 0.26
                + grade * 0.16
                + lms * 0.18
            )
            + notes_penalty
            + flags_penalty
            + login_penalty
            + financial_penalty
        )

        status = "urgent" if risk_score >= 60 else "watch" if risk_score >= 40 else "stable"
        next_action = (
            "Route to advisor and financial-support outreach within 24 hours."
            if student["financial_hold"]
            else "Assign advisor follow-up and instructor nudges this week."
            if status == "urgent"
            else "Monitor momentum and send a targeted study-support message."
            if status == "watch"
            else "Maintain light-touch encouragement and celebrate progress."
        )

        return {
            "studentId": student["student_id"],
            "name": student["name"],
            "program": student["program"],
            "cohort": student["cohort"],
            "momentumScore": momentum_score,
            "riskScore": risk_score,
            "status": status,
            "attendanceRate": round(student["attendance_rate"] * 100, 1),
            "assignmentCompletionRate": round(student["assignment_completion_rate"] * 100, 1),
            "averageGrade": grade,
            "lmsActivityScore": lms,
            "financialHold": student["financial_hold"],
            "daysSinceLastLogin": student["days_since_last_login"],
            "nextAction": next_action
        }

    def scored_students(self) -> list[dict[str, Any]]:
        data = self.load()
        return sorted(
            [self.score_student(student) for student in data["students"]],
            key=lambda item: (-item["riskScore"], item["name"]),
        )

    def summary(self) -> dict[str, Any]:
        data = self.load()
        scored = self.scored_students()
        avg_momentum = mean(student["momentumScore"] for student in scored)
        avg_risk = mean(student["riskScore"] for student in scored)
        urgent = [student for student in scored if student["status"] == "urgent"]
        watch = [student for student in scored if student["status"] == "watch"]
        holds = [student for student in scored if student["financialHold"]]
        return {
            "institution": data["institution"],
            "term": data["term"],
            "studentCount": len(scored),
            "averageMomentumScore": round(avg_momentum, 1),
            "averageRiskScore": round(avg_risk, 1),
            "urgentCount": len(urgent),
            "watchCount": len(watch),
            "financialHoldCount": len(holds),
            "leadRecommendation": (
                "Prioritize students with both login drift and assignment slippage, then "
                "treat financial holds as a separate intervention lane instead of burying them inside generic risk alerts."
            ),
        }

    def intervention_queue(self) -> list[dict[str, Any]]:
        return self.scored_students()

    def student(self, student_id: str) -> dict[str, Any] | None:
        for student in self.scored_students():
            if student["studentId"] == student_id:
                return student
        return None

    def sample_payload(self) -> dict[str, Any]:
        queue = self.intervention_queue()
        return {
            "dashboard": self.summary(),
            "interventions": [
                {
                    "studentId": student["studentId"],
                    "name": student["name"],
                    "riskScore": student["riskScore"],
                    "status": student["status"],
                    "nextAction": student["nextAction"],
                }
                for student in queue[:3]
            ],
        }


def build_service(root: Path | None = None) -> StudentSuccessService:
    base = root or Path(__file__).resolve().parents[2]
    return StudentSuccessService(base / "app" / "data" / "sample_students.json")
