# CSV File Optimization & Splitting

A Python-based data processing project designed to split large CSV datasets into smaller, manageable files, validate data integrity, and benchmark gzip compression performance.

This is a self-initiated portfolio project using a synthetic e-commerce transaction dataset.

## Project Overview

Large CSV files can be difficult to manage, transfer, and process. This project demonstrates a memory-efficient approach to handling large CSV datasets using Python's built-in libraries.

The workflow includes:

- Generating a synthetic e-commerce transaction dataset.
- Splitting a large CSV file into smaller files.
- Validating data integrity through row-by-row comparison.
- Compressing output files using GZIP.
- Measuring compression performance and storage savings.
- Verifying compressed files using SHA-256 checksums.

## Dataset Information

| Attribute | Value |
|---|---:|
| Dataset type | Synthetic e-commerce transactions |
| Total records | 1,000,000 |
| Number of columns | 10 |
| Original file size | Approximately 96.03 MB |
| Output files | 5 |
| Records per output file | 200,000 |

## Technologies Used

- Python 3
- CSV module
- GZIP
- Hashlib (SHA-256)
- OS and time modules
- Python standard library

No third-party Python packages are required.

## Project Structure

```text
csv-optimization-portfolio/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   ├── splitting_report.csv
│   ├── integrity_validation_report.csv
│   └── compression_benchmark.csv
│
├── screenshots/
│
├── scripts/
│   ├── 01_generate_dataset.py
│   ├── 02_csv_optimizer.py
│   ├── 03_integrity_validation.py
│   └── 04_compression_benchmark.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Processing Workflow

### 1. Dataset Generation

Generated a synthetic dataset containing 1,000,000 e-commerce transaction records.

### 2. CSV Splitting

Processed the original CSV file and divided it into five smaller files, each containing 200,000 data records.

The script uses sequential row processing rather than loading the entire dataset into memory.

### 3. Data Integrity Validation

Compared the original dataset against the combined split files using row-by-row validation.

### 4. GZIP Compression

Compressed each split CSV file using GZIP compression level 6.

### 5. SHA-256 Verification

Verified that each compressed file could be decompressed into exactly the same file content as its corresponding original split CSV.

## Benchmark Results

### CSV Splitting

| Metric | Result |
|---|---:|
| Input records | 1,000,000 |
| Output records | 1,000,000 |
| Generated files | 5 |
| Execution time | 12.57 seconds |
| Validation | PASS |

### Data Integrity Validation

| Metric | Result |
|---|---:|
| Matching rows | 1,000,000 |
| Mismatched rows | 0 |
| Missing rows | 0 |
| Extra rows | 0 |
| Validation status | PASS |
| Execution time | 9.26 seconds |

### Compression Benchmark

| Metric | Result |
|---|---:|
| Original split files | 96.04 MB |
| Compressed files | 16.55 MB |
| Storage reduction | 82.77% |
| Compressed files verified | 5/5 |
| SHA-256 integrity checks | PASS |

*File sizes and performance measurements are based on the generated benchmark reports. Execution time may vary depending on hardware and storage performance.*

## How to Run

Make sure Python 3 is installed.

Run the scripts in the following order from the project root directory:

```bash
python scripts/01_generate_dataset.py
python scripts/02_csv_optimizer.py
python scripts/03_integrity_validation.py
python scripts/04_compression_benchmark.py
```

The scripts generate the dataset, split files, compressed files, and CSV reports automatically.

## Key Skills Demonstrated

- Large CSV data processing
- Python scripting and automation
- Memory-efficient sequential file processing
- CSV splitting and file management
- Data integrity validation
- GZIP compression benchmarking
- SHA-256 checksum verification
- Performance measurement and reporting

## Project Type

Self-initiated portfolio project using synthetic data. This project does not represent work performed for a client.

## Author

**Sari Marlina**

GitHub: [github.com/sarimarlina](https://github.com/sarimarlina)

Portfolio: [sarimarlina.github.io/sarimarlina-portofolio.io](https://sarimarlina.github.io/sarimarlina-portofolio.io)