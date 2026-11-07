
import csv
import time
from pathlib import Path

# ==========================================
# CSV OPTIMIZATION & SPLITTING ENGINE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "ecommerce_transactions.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "reports"

ROWS_PER_FILE = 200_000
ENCODING = "utf-8"


def split_csv():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    existing_parts = list(OUTPUT_DIR.glob("transactions_part_*.csv"))

    if existing_parts:
        raise FileExistsError(
            "Output files already exist. "
            "Move or rename them before running this script again."
        )

    start_time = time.perf_counter()

    total_rows = 0
    part_number = 0
    part_rows = 0
    output_file = None
    writer = None
    report = []

    print("Starting CSV optimization and splitting...")
    print(f"Input: {INPUT_FILE.name}")
    print(f"Rows per output file: {ROWS_PER_FILE:,}")

    try:
        with open(
            INPUT_FILE,
            "r",
            newline="",
            encoding=ENCODING,
        ) as source:

            reader = csv.reader(source)

            header = next(reader, None)

            if not header:
                raise ValueError("Input CSV is empty or has no header.")

            for row in reader:

                if len(row) != len(header):
                    raise ValueError(
                        f"Invalid column count at data row "
                        f"{total_rows + 1}"
                    )

                if output_file is None or part_rows >= ROWS_PER_FILE:

                    if output_file is not None:
                        output_file.close()

                    part_number += 1
                    part_rows = 0

                    output_path = (
                        OUTPUT_DIR /
                        f"transactions_part_{part_number:03d}.csv"
                    )

                    output_file = open(
                        output_path,
                        "w",
                        newline="",
                        encoding=ENCODING,
                    )

                    writer = csv.writer(output_file)
                    writer.writerow(header)

                    print(f"Creating: {output_path.name}")

                writer.writerow(row)

                total_rows += 1
                part_rows += 1

            if output_file is not None:
                output_file.close()
                output_file = None

        # Collect output information
        output_files = sorted(
            OUTPUT_DIR.glob("transactions_part_*.csv")
        )

        output_rows = 0

        for file_path in output_files:
            with open(
                file_path,
                "r",
                newline="",
                encoding=ENCODING,
            ) as file:

                output_reader = csv.reader(file)
                output_header = next(output_reader, None)

                if output_header != header:
                    raise ValueError(
                        f"Header mismatch in {file_path.name}"
                    )

                file_rows = sum(1 for _ in output_reader)

                output_rows += file_rows

                report.append({
                    "file_name": file_path.name,
                    "data_rows": file_rows,
                    "file_size_mb": round(
                        file_path.stat().st_size / (1024 * 1024),
                        2,
                    ),
                    "status": "PASS",
                })

        # Final validation
        validation_passed = (
            total_rows == output_rows
            and total_rows > 0
        )

        if not validation_passed:
            raise ValueError(
                f"Validation failed: input={total_rows}, "
                f"output={output_rows}"
            )

        # Save report
        report_path = REPORT_DIR / "splitting_report.csv"

        with open(
            report_path,
            "w",
            newline="",
            encoding=ENCODING,
        ) as report_file:

            fields = [
                "file_name",
                "data_rows",
                "file_size_mb",
                "status",
            ]

            report_writer = csv.DictWriter(
                report_file,
                fieldnames=fields,
            )

            report_writer.writeheader()
            report_writer.writerows(report)

        elapsed = time.perf_counter() - start_time

        print("\n========== PROCESS SUMMARY ==========")
        print(f"Input records : {total_rows:,}")
        print(f"Output records: {output_rows:,}")
        print(f"Output files  : {len(output_files)}")
        print(f"Validation    : {'PASS' if validation_passed else 'FAIL'}")
        print(f"Execution time: {elapsed:.2f} seconds")
        print(f"Report        : {report_path}")

        print("\nCSV splitting completed successfully!")

    finally:
        if output_file is not None and not output_file.closed:
            output_file.close()


if __name__ == "__main__":
    split_csv()
