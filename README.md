# Python Hardware Test Automation

A beginner-friendly engineering portfolio project demonstrating **simulated device testing**, automated pass/fail checks, fault identification, and CSV reporting.

> This project uses generated sensor readings. It does **not** connect to physical hardware or claim real-world validation.

## Features

- Simulates device voltage, temperature, and response latency
- Validates measurements against configurable thresholds in `diagnostics.py`
- Identifies out-of-range measurements
- Exports results to `reports/diagnostics.csv`
- Includes automated unit tests and an HTML diagnostics dashboard
- Uses only the Python standard library

## Requirements

Python 3.10 or newer.

## Run

```bash
python diagnostics.py
```

## Diagnostics dashboard

Generate a self-contained HTML dashboard using the Python standard library:

```bash
python dashboard.py
```

Open `reports/dashboard.html` in your browser. The dashboard shows simulated device pass/fail counts, pass rate, measurements, and failure reasons. It does not connect to real hardware.

## Test

```bash
python -m unittest discover -s tests -v
```

## Example output

```text
DEV-001: FAIL - voltage out of range
DEV-002: PASS - all checks passed
...
Saved report to reports/diagnostics.csv
```

## Test criteria

| Measurement | Passing range |
|---|---|
| Voltage | 4.75–5.25 V (inclusive) |
| Temperature | 0–70 °C (inclusive) |
| Response latency | ≤ 100 ms |

## Career relevance

Demonstrates foundational skills used in systems integration, software QA, automated testing, diagnostics, and engineering documentation.

## Next steps

Connect an Arduino or ESP32 over serial, add structured logs, and collect actual sensor data after validating the hardware setup.
