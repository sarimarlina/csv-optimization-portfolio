
import gzip
import hashlib
import shutil
import time
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "reports"

BUFFER_SIZE = 1024 * 1024
COMPRESSION_LEVEL = 6


def calculate_sha256(file_object):
    digest = hashlib.sha256()

    while True:
        chunk = file_object.read(BUFFER_SIZE)

        if not chunk:
            break

        digest.update(chunk)

    return digest.hexdigest()


def compress_and_validate(input_path):
    output_path = input_path.with_suffix(
        input_path.suffix + ".gz"
    )

    if output_path.exists():
        raise FileExistsError(
            f"Compressed file already exists: {output_path.name}"
        )

    start_time = time.perf_counter()

    with open(input_path, "rb") as source:
        original_hash = calculate_sha256(source)

    with open(input_path, "rb") as source:
        with gzip.open(
            output_path,
            "wb",
            compresslevel=COMPRESSION_LEVEL,
        ) as compressed:
            shutil.copyfileobj(
                source,
                compressed,
                length=BUFFER_SIZE,
            )

    with gzip.open(output_path, "rb") as compressed:
        compressed_hash = calculate_sha256(compressed)

    elapsed = time.perf_counter() - start_time

    original_size = input_path.stat().st_size
    compressed_size = output_path.stat().st_size

    saving_percent = (
        (1 - compressed_size / original_size) * 100
    )

    validation = original_hash == compressed_hash

    return {
        "file_name": input_path.name,
        "original_size_mb": round(
            original_size / (1024 * 1024), 2
        ),
        "compressed_size_mb": round(
            compressed_size / (1024 * 1024), 2
        ),
        "space_saved_percent": round(
            saving_percent, 2
        ),
        "execution_seconds": round(elapsed, 2),
        "integrity_status": (
            "PASS" if validation else "FAIL"
        ),
    }


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    input_files = sorted(
        DATA_DIR.glob("transactions_part_*.csv")
    )

    if not input_files:
        raise FileNotFoundError(
            "No CSV split files found."
        )

    results = []

    print("Starting CSV compression benchmark...")
    print(f"Compression level: {COMPRESSION_LEVEL}")

    for input_path in input_files:
        print(f"\nCompressing {input_path.name}...")

        result = compress_and_validate(input_path)
        results.append(result)

        print(
            f"Original: {result['original_size_mb']} MB"
        )
        print(
            f"Compressed: {result['compressed_size_mb']} MB"
        )
        print(
            f"Space saved: {result['space_saved_percent']}%"
        )
        print(
            f"Integrity: {result['integrity_status']}"
        )

        if result["integrity_status"] != "PASS":
            raise ValueError(
                f"Integrity check failed: {input_path.name}"
            )

    total_original = sum(
        r["original_size_mb"] for r in results
    )

    total_compressed = sum(
        r["compressed_size_mb"] for r in results
    )

    total_saved = (
        (1 - total_compressed / total_original) * 100
    )

    report_path = (
        REPORT_DIR / "compression_benchmark.csv"
    )

    with open(
        report_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as report_file:

        writer = csv.DictWriter(
            report_file,
            fieldnames=results[0].keys(),
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n========== COMPRESSION SUMMARY ==========")
    print(f"Files compressed: {len(results)}")
    print(f"Original size: {total_original:.2f} MB")
    print(f"Compressed size: {total_compressed:.2f} MB")
    print(f"Total space saved: {total_saved:.2f}%")
    print("Integrity validation: PASS")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
