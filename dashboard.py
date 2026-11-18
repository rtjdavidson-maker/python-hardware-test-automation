"""Generate a self-contained HTML dashboard from simulated hardware diagnostics.

Uses only Python's standard library. No hardware is connected.
"""
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path

from diagnostics import Reading, evaluate, simulate_readings


def make_dashboard(readings: list[Reading]) -> str:
    """Return an HTML document with a readable diagnostic summary."""
    if not readings:
        raise ValueError("At least one device reading is required")

    results = [(reading, *evaluate(reading)) for reading in readings]
    counts = Counter(status for _, status, _ in results)
    passed = counts["PASS"]
    failed = counts["FAIL"]
    total = len(results)
    pass_rate = passed / total * 100
    created = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    rows = []
    for reading, status, details in results:
        cls = "pass" if status == "PASS" else "fail"
        rows.append(
            "<tr>"
            f"<td>{escape(reading.device_id)}</td>"
            f"<td>{reading.voltage_v:.2f} V</td>"
            f"<td>{reading.temperature_c:.1f} °C</td>"
            f"<td>{reading.latency_ms:.1f} ms</td>"
            f'<td><span class="{cls}">{status}</span></td>'
            f"<td>{escape(details)}</td>"
            "</tr>"
        )

    chart_bars = []
    for label, n, cls in [("PASS", passed, "good"), ("FAIL", failed, "bad")]:
        width = n / total * 100
        chart_bars.append(
            '<div class="bar-row">'
            f'<span>{label}</span><div class="track"><div class="fill {cls}" style="width:{width:.2f}%"></div></div>'
            f"<strong>{n}</strong></div>"
        )

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hardware Diagnostics Dashboard</title>
<style>
:root {font-family: system-ui, -apple-system, Segoe UI, sans-serif; color:#e7edf5; background:#101827}
* {box-sizing:border-box}
main {max-width:1100px; margin:36px auto; padding:0 20px}
h1 {margin-bottom:6px; font-size:clamp(1.6rem,4vw,2.3rem)}
.subtitle {color:#abb9ca; margin-top:0}
.cards {display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:16px; margin:24px 0}
.card,.panel {background:#1c293d; border:1px solid #334459; border-radius:14px; padding:20px}
.card small {display:block;color:#b5c1d0}
.card strong {display:block;font-size:2.2rem;margin-top:8px}
.panel {margin:16px 0;overflow-x:auto}
.bar-row {display:grid;grid-template-columns:52px 1fr 30px;gap:12px;align-items:center;margin:18px 0}
.track {height:18px;background:#344458;border-radius:10px;overflow:hidden}
.fill {height:100%;border-radius:10px}
.good {background:#2dc58d}.bad {background:#f47a87}
table {width:100%;border-collapse:collapse;min-width:760px;text-align:left}
th,td {padding:12px;border-bottom:1px solid #35465b;font-size:.91rem}
th {color:#c7d3e2}
.pass {color:#58dfac;font-weight:700}
.fail {color:#ff9ba3;font-weight:700}
footer {color:#9eafc2;font-size:.86rem;margin:22px 0}
</style>
</head>
<body><main>
<h1>Hardware Diagnostics Dashboard</h1>
<p class="subtitle">Simulated devices • Generated """ + escape(created) + """</p>
<section class="cards" aria-label="Summary metrics">
<div class="card"><small>Devices tested</small><strong>""" + str(total) + """</strong></div>
<div class="card"><small>Passed</small><strong>""" + str(passed) + """</strong></div>
<div class="card"><small>Failed</small><strong>""" + str(failed) + """</strong></div>
<div class="card"><small>Pass rate</small><strong>""" + f"{pass_rate:.1f}%" + """</strong></div>
</section>
<section class="panel"><h2>Test results</h2>""" + "".join(chart_bars) + """</section>
<section class="panel"><h2>Device measurements</h2>
<table><thead><tr><th>Device</th><th>Voltage</th><th>Temperature</th><th>Latency</th><th>Status</th><th>Findings</th></tr></thead>
<tbody>""" + "".join(rows) + """</tbody></table></section>
<footer>Educational simulation only. Thresholds: 4.75–5.25 V, 0–70 °C, latency ≤ 100 ms. No physical hardware was tested.</footer>
</main></body></html>"""


def main() -> None:
    readings = simulate_readings()
    destination = Path("reports") / "dashboard.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(make_dashboard(readings), encoding="utf-8")
    print(f"Dashboard saved to {destination.resolve()}")
    print("Open this file in a web browser to view the dashboard.")


if __name__ == "__main__":
    main()
