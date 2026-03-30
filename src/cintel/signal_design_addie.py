"""
signal_design_addie.py - Project script.

Author: Addie Gemmell
Date: 2026-03

System Metrics Data

- Data is taken from a system that records operational metrics.
- The data is structured and static for this example.
- Each row represents one observation of system behavior.
- The CSV file includes these columns:
  - requests: number of requests handled
  - errors: number of failed requests
  - total_latency_ms: total response time in milliseconds

Purpose

- Read system metrics from a CSV file.
- Design useful signals from the raw measurements.
- Save the resulting signals as a new CSV artifact.
- Log the pipeline process to assist with debugging and transparency.

Paths (relative to repo root)

    INPUT FILE: data/system_metrics_addie.csv
    OUTPUT FILE: artifacts/signals_addie.csv

Terminal command to run this file from the root project folder

    uv run python -m cintel.signal_design_addie
"""

import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

LOG: logging.Logger = get_logger("P3", level="DEBUG")

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

DATA_FILE: Final[Path] = DATA_DIR / "system_metrics_addie.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "signals_addie.csv"


def main() -> None:
    """Run the pipeline."""
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # STEP 1: Read the CSV
    df: pl.DataFrame = pl.read_csv(DATA_FILE)
    LOG.info(f"Loaded {df.height} system metric records")

    # STEP 2: Design signals
    LOG.info("Designing signals from the raw metrics...")

    is_requests_positive: pl.Expr = pl.col("requests") > 0

    calculated_error_rate: pl.Expr = pl.col("errors") / pl.col("requests")
    error_rate_signal_recipe: pl.Expr = (
        pl.when(is_requests_positive)
        .then(calculated_error_rate)
        .otherwise(0.0)
        .alias("error_rate")
    )

    calculated_avg_latency: pl.Expr = pl.col("total_latency_ms") / pl.col("requests")
    avg_latency_signal_recipe: pl.Expr = (
        pl.when(is_requests_positive)
        .then(calculated_avg_latency)
        .otherwise(0.0)
        .alias("avg_latency_ms")
    )

    throughput_signal_recipe: pl.Expr = pl.col("requests").alias("throughput")

    high_error_flag_signal_recipe: pl.Expr = (
        pl.when(pl.col("requests") > 0)
        .then(pl.col("errors") / pl.col("requests") > 0.05)
        .otherwise(False)
        .alias("high_error_flag")
    )

    df_with_signals: pl.DataFrame = df.with_columns(
        [
            error_rate_signal_recipe,
            avg_latency_signal_recipe,
            throughput_signal_recipe,
            high_error_flag_signal_recipe,
        ]
    )

    LOG.info(
        "Created signal columns: error_rate, avg_latency_ms, throughput, high_error_flag"
    )

    # STEP 3: Select columns to save
    signals_df: pl.DataFrame = df_with_signals.select(
        [
            "requests",
            "errors",
            "total_latency_ms",
            "error_rate",
            "avg_latency_ms",
            "throughput",
            "high_error_flag",
        ]
    )

    LOG.info(f"Enhanced signals table has {signals_df.height} rows")

    # STEP 4: Save artifact
    signals_df.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote signals file: {OUTPUT_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


if __name__ == "__main__":
    main()
