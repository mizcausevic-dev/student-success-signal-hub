# Student Success Signal Hub Architecture

## Intent

This repo turns common student-success signals into a practical intervention
system for advisors and academic support teams.

The scoring model uses:

- attendance
- LMS activity
- assignment completion
- average grade
- advisor notes
- support flags
- financial hold status
- login drift

## Flow

1. `app/data/sample_students.json` provides a realistic student cohort snapshot.
2. `app/services/success_service.py` computes momentum and risk scores.
3. `app/main.py` exposes HTML proof routes and JSON APIs.
4. `app/render.py` builds the repo’s static proof pages.
5. `scripts/render_readme_assets.py` captures PNG screenshots from those proof pages.

## Routes

- `/`
  - overview surface for student-success posture
- `/queue`
  - intervention queue
- `/evidence`
  - student-level explainability view
- `/api-summary`
  - sample payload and route surface
- `/api/dashboard/summary`
  - top-level score summary
- `/api/students`
  - full student queue
- `/api/students/{student_id}`
  - individual student detail
- `/api/sample`
  - compact demo payload

## Why It Matters

Student support systems often fail because:

- they surface too much passive data
- they don’t explain why a student is at risk
- they mix academic risk with operational blockers like financial holds

This repo focuses on actionability and clear intervention sequencing instead.
