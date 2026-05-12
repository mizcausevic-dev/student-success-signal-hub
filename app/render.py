from __future__ import annotations

import html
import json
from pathlib import Path

from app.services.success_service import build_service


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def page_shell(title: str, kicker: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_escape(title)}</title>
  <style>
    :root {{
      --bg: #07111d;
      --panel: #0d1a2b;
      --line: #1d3655;
      --text: #eef2ff;
      --muted: #98a7c2;
      --accent: #68b7ff;
      --warning: #ffc86b;
      --danger: #ff8c7f;
      --ok: #7ce0a3;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", Inter, sans-serif;
      background: linear-gradient(180deg, #07111d 0%, #091827 100%);
      color: var(--text);
    }}
    .page {{
      width: 1440px;
      margin: 0 auto;
      padding: 48px 52px 64px;
      background:
        radial-gradient(circle at top right, rgba(104,183,255,0.16), transparent 30%),
        linear-gradient(180deg, rgba(11,25,41,0.95), rgba(6,14,24,0.98));
      min-height: 920px;
    }}
    .frame {{
      border: 1px solid var(--line);
      border-radius: 34px;
      padding: 28px 32px 36px;
      background: rgba(11, 22, 37, 0.88);
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 15px;
      letter-spacing: 0.34em;
      text-transform: uppercase;
      margin-bottom: 18px;
      font-weight: 700;
    }}
    h1 {{
      margin: 0;
      font-size: 66px;
      line-height: 0.98;
      color: #f4f1e3;
      font-family: Georgia, "Times New Roman", serif;
      max-width: 1120px;
    }}
    .lede {{
      margin-top: 18px;
      max-width: 920px;
      color: var(--muted);
      font-size: 18px;
      line-height: 1.6;
    }}
    .pill-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 24px;
    }}
    .pill {{
      border-radius: 999px;
      padding: 10px 16px;
      background: #1a2f4d;
      border: 1px solid #29486e;
      color: #f5f8ff;
      font-size: 15px;
      font-weight: 600;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin-top: 28px;
    }}
    .stat {{
      padding: 22px 22px 18px;
      border-radius: 24px;
      background: #12233a;
      border: 1px solid #25415f;
      min-height: 168px;
    }}
    .label {{
      color: #a8b6cd;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 13px;
      margin-bottom: 14px;
    }}
    .value {{
      color: #f4f1e3;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 48px;
      line-height: 0.95;
      margin-bottom: 12px;
    }}
    .copy {{
      color: #c1cadc;
      font-size: 16px;
      line-height: 1.5;
    }}
    .section {{
      margin-top: 34px;
      border-radius: 28px;
      border: 1px solid #203654;
      background: #0d1524;
      padding: 28px;
    }}
    .section-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}
    .card {{
      border-radius: 22px;
      border: 1px solid #263d5f;
      background: #131e32;
      padding: 22px;
      min-height: 250px;
    }}
    .card .kicker {{
      color: var(--accent);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.18em;
      margin-bottom: 18px;
      font-weight: 700;
    }}
    .card h2 {{
      font-size: 24px;
      line-height: 1.15;
      margin: 0 0 14px;
      color: #f4f1e3;
      font-family: Georgia, "Times New Roman", serif;
    }}
    .card p, .card li, .queue td, .queue th, .note {{
      color: #bdc7d9;
      font-size: 16px;
      line-height: 1.55;
      margin: 0;
    }}
    .card ul {{
      padding-left: 18px;
      margin: 0;
    }}
    .status-urgent {{ color: var(--danger); font-weight: 700; }}
    .status-watch {{ color: var(--warning); font-weight: 700; }}
    .status-stable {{ color: var(--ok); font-weight: 700; }}
    .queue {{
      width: 100%;
      border-collapse: collapse;
    }}
    .queue th, .queue td {{
      text-align: left;
      padding: 14px 12px;
      border-bottom: 1px solid #203654;
      vertical-align: top;
    }}
    .queue th {{
      color: #8fbfff;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 12px;
    }}
    .json {{
      background: #07101b;
      border: 1px solid #284462;
      border-radius: 22px;
      padding: 24px;
      margin-top: 24px;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      color: #d7f7da;
      font-size: 15px;
      line-height: 1.45;
      font-family: Consolas, "SFMono-Regular", monospace;
    }}
  </style>
</head>
<body>
  <div class="page">
    <div class="frame">
      <div class="eyebrow">{_escape(kicker)}</div>
      {body}
    </div>
  </div>
</body>
</html>
"""


def render_overview() -> str:
    service = build_service()
    summary = service.summary()
    students = service.intervention_queue()
    body = f"""
      <h1>Turn attendance, LMS activity, and academic slippage into a real intervention queue.</h1>
      <p class="lede">
        Student Success Signal Hub scores student momentum and risk across attendance,
        assignments, grades, support flags, and login drift so advising teams know who
        needs help first and why.
      </p>
      <div class="pill-row">
        <div class="pill">attendance + LMS signals</div>
        <div class="pill">advisor intervention queue</div>
        <div class="pill">cohort health summary</div>
        <div class="pill">student support proof</div>
      </div>
      <div class="stats">
        <div class="stat"><div class="label">Students scored</div><div class="value">{summary['studentCount']}</div><div class="copy">Students monitored across coursework, engagement, and support signals.</div></div>
        <div class="stat"><div class="label">Avg momentum</div><div class="value">{summary['averageMomentumScore']}</div><div class="copy">Composite signal for academic engagement and on-track activity.</div></div>
        <div class="stat"><div class="label">Urgent cases</div><div class="value">{summary['urgentCount']}</div><div class="copy">Students needing fast advisor or support intervention.</div></div>
        <div class="stat"><div class="label">Financial holds</div><div class="value">{summary['financialHoldCount']}</div><div class="copy">Students whose academic risk should be treated separately from billing friction.</div></div>
      </div>
      <div class="section">
        <div class="section-grid">
          {''.join(
              f'''<div class="card"><div class="kicker">{_escape(student["cohort"])}</div><h2>{_escape(student["name"])}</h2><p>Momentum: {student["momentumScore"]} • Risk: {student["riskScore"]} • Status: <span class="status-{_escape(student["status"])}">{_escape(student["status"])}</span></p><p>{_escape(student["nextAction"])}</p></div>'''
              for student in students
          )}
        </div>
      </div>
    """
    return page_shell("Student Success Signal Hub - Overview", "student success signal hub", body)


def render_queue() -> str:
    students = build_service().intervention_queue()
    rows = "".join(
        f"""
        <tr>
          <td>{_escape(student['name'])}</td>
          <td>{_escape(student['program'])}</td>
          <td>{student['riskScore']}</td>
          <td>{student['momentumScore']}</td>
          <td class="status-{_escape(student['status'])}">{_escape(student['status'])}</td>
          <td>{_escape(student['nextAction'])}</td>
        </tr>
        """
        for student in students
    )
    body = f"""
      <h1>Advisors get a clean queue, not a vague dashboard full of passive red flags.</h1>
      <p class="lede">
        This intervention queue is designed to support action. It sorts students by risk,
        keeps momentum visible, and separates academic, engagement, and support issues well enough for real triage.
      </p>
      <div class="section">
        <table class="queue">
          <thead>
            <tr>
              <th>Student</th>
              <th>Program</th>
              <th>Risk</th>
              <th>Momentum</th>
              <th>Status</th>
              <th>Next action</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    """
    return page_shell("Student Success Signal Hub - Queue", "intervention queue", body)


def render_student_evidence() -> str:
    student = build_service().student("stu-1057")
    body = f"""
      <h1>The score is explainable enough for advising, academic leadership, and retention planning.</h1>
      <p class="lede">
        A student support system is only useful if staff can explain why someone is at risk.
        This view keeps the risk shape transparent and maps it directly to a next action.
      </p>
      <div class="section-grid">
        <div class="card"><div class="kicker">attendance</div><h2>{student['attendanceRate']}%</h2><p>Attendance drop is one of the clearest momentum signals in the current term.</p></div>
        <div class="card"><div class="kicker">assignments</div><h2>{student['assignmentCompletionRate']}%</h2><p>Late or missing work is dragging persistence and grade momentum at the same time.</p></div>
        <div class="card"><div class="kicker">financial friction</div><h2>{'Yes' if student['financialHold'] else 'No'}</h2><p>Financial holds should trigger a different intervention path than pure academic coaching.</p></div>
      </div>
      <div class="json"><pre>{_escape(json.dumps(student, indent=2))}</pre></div>
    """
    return page_shell("Student Success Signal Hub - Evidence", "evidence lane", body)


def render_api_summary() -> str:
    payload = build_service().sample_payload()
    body = f"""
      <h1>A compact API surface that can feed advising tools, dean reports, and intervention workflows.</h1>
      <p class="lede">
        The same scoring layer can power internal portals, advisor worklists, and leadership reporting without duplicating student-risk logic.
      </p>
      <div class="section-grid">
        <div class="card"><div class="kicker">routes</div><h2>Summary, queue, and student detail APIs.</h2><p><code>/api/dashboard/summary</code>, <code>/api/students</code>, <code>/api/students/{'{student_id}'}</code>, and <code>/api/sample</code>.</p></div>
        <div class="card"><div class="kicker">fit</div><h2>Built for advising and retention operations.</h2><p>It works as a signal layer for student success teams, academic affairs, and online program operators.</p></div>
        <div class="card"><div class="kicker">payload</div><h2>Sample intervention payload from the local service.</h2><p>Small enough for demos, structured enough for downstream systems.</p></div>
      </div>
      <div class="json"><pre>{_escape(json.dumps(payload, indent=2))}</pre></div>
    """
    return page_shell("Student Success Signal Hub - API Summary", "api summary", body)


def write_static_proof_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-intervention-queue.html": render_queue(),
        "03-student-evidence.html": render_student_evidence(),
        "04-api-summary.html": render_api_summary(),
    }
    written: list[Path] = []
    for name, contents in pages.items():
        target = output_dir / name
        target.write_text(contents, encoding="utf-8")
        written.append(target)
    return written
