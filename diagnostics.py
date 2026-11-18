"""Simulated hardware diagnostics for an engineering portfolio."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import csv
import random
from pathlib import Path


@dataclass
class Reading:
    device_id: str
    voltage_v: float
    temperature_c: float
    latency_ms: float


def evaluate(reading: Reading) -> tuple[str, str]:
    failures = []
    if not 4.75 <= reading.voltage_v <= 5.25:
        failures.append("voltage out of range")
    if not 0 <= reading.temperature_c <= 70:
        failures.append("temperature out of range")
    if reading.latency_ms > 100:
        failures.append("latency too high")
    return ("FAIL", "; ".join(failures)) if failures else ("PASS", "all checks passed")


def simulate_readings(count: int = 10, seed: int = 42) -> list[Reading]:
    rng = random.Random(seed)
    return [
        Reading(
            device_id=f"DEV-{index:03d}",
            voltage_v=round(rng.uniform(4.5, 5.5), 2),
            temperature_c=round(rng.uniform(20, 85), 1),
            latency_ms=round(rng.uniform(10, 130), 1),
        )
        for index in range(1, count + 1)
    ]


def write_report(readings: list[Reading], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=["timestamp_utc", "device_id", "voltage_v", "temperature_c", "latency_ms", "status", "details"])
        writer.writeheader()
        for reading in readings:
            status, details = evaluate(reading)
            writer.writerow({"timestamp_utc": datetime.now(timezone.utc).isoformat(), **asdict(reading), "status": status, "details": details})


def main() -> None:
    readings = simulate_readings()
    for reading in readings:
        status, details = evaluate(reading)
        print(f"{reading.device_id}: {status} - {details}")
    destination = Path("reports") / "diagnostics.csv"
    write_report(readings, destination)
    print(f"\nSaved report to {destination}")


if __name__ == "__main__":
    main()
