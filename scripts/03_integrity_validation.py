
import csv
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "ecommerce_transactions.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "reports"

ROWS_PER_FILE = 200_000


def validate_integrity():
    start_time = time.perf_counter()

    output_files = sorted(
        OUTPUT_DIR.glob("transactions_part_*.csv")
    )

    if not INPUT_FILE.exists():
        raise FileNotFoundError(INPUT_FILE)

    if not output_files:
        raise FileNotFoundError("No split CSV files found.")

    input_rows = 0
    output_rows = 0
    matching_rows = 0
    mismatched_rows = 0
    extra_rows = 0
    missing_rows = 0

    print("Starting independent data integrity validation...")

    with open(
        INPUT_FILE, "r", newline="", encoding="utf-8"
    ) as source:

        source_reader = csv.reader(source)
        source_header = next(source_reader, None)

        if source_header is None:
            raise ValueError("Source CSV has no header.")

        for part_number, output_path in enumerate(output_files, 1):

            print(f"Validating {output_path.name}...")

            part_count = 0

            with open(
                output_path, "r", newline="", encoding="utf-8"
            ) as output:

                output_reader = csv.reader(output)
                output_header = next(output_reader, None)

                if output_header != source_header:
                    raise ValueError(
                        f"Header mismatch: {output_path.name}"
                    )

                for output_row in output_reader:
                    part_count += 1
                    output_rows += 1

                    source_row = next(source_reader, None)

                    if source_row is None:
                        extra_rows += 1
                        continue

                    input_rows += 1

                    if output_row == source_row:
                        matching_rows += 1
                    else:
                        mismatched_rows += 1

            if part_count > ROWS_PER_FILE:
                raise ValueError(
                    f"Part exceeds row limit: {output_path.name}"
                )

            print(f"  Rows checked: {part_count:,}")

        # Check whether source has remaining rows
        for _ in source_reader:
            input_rows += 1
            missing_rows += 1

    validation_passed = (
        mismatched_rows == 0
        and extra_rows == 0
        and missing_rows == 0
        and input_rows == output_rows
        and matching_rows == input_rows
    )

    elapsed = time.perf_counter() - start_time

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report_file = REPORT_DIR / "integrity_validation_report.csv"

    report_data = {
        "input_rows": input_rows,
        "output_rows": output_rows,
        "matching_rows": matching_rows,
        "mismatched_rows": mismatched_rows,
        "missing_rows": missing_rows,
        "extra_rows": extra_rows,
        "output_files": len(output_files),
        "execution_seconds": round(elapsed, 2),
        "validation_status": (
            "PASS" if validation_passed else "FAIL"
        ),
    }

    with open(
        report_file, "w", newline="", encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=report_data.keys()
        )

        writer.writeheader()
        writer.writerow(report_data)

    print("\n========== INTEGRITY REPORT ==========")
    for key, value in report_data.items():
        print(f"{key}: {value}")

    print(f"\nReport saved: {report_file}")

    if not validation_passed:
        raise ValueError("Data integrity validation FAILED!")

    print("\nALL DATA INTEGRITY CHECKS PASSED!")


if __name__ == "__main__":
    validate_integrity()
