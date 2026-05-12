from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.success_service import build_service


class StudentSuccessTests(unittest.TestCase):
    def test_summary_counts(self) -> None:
        summary = build_service().summary()
        self.assertGreaterEqual(summary["studentCount"], 5)
        self.assertGreaterEqual(summary["urgentCount"], 1)

    def test_queue_sorting(self) -> None:
        queue = build_service().intervention_queue()
        self.assertGreaterEqual(queue[0]["riskScore"], queue[-1]["riskScore"])

    def test_student_api_lookup(self) -> None:
        client = TestClient(app)
        response = client.get("/api/students/stu-1057")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Sofia Ramirez")


if __name__ == "__main__":
    unittest.main()
