
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# ==========================================
# CSV OPTIMIZATION PORTFOLIO
# Synthetic E-commerce Dataset Generator
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "raw" / "ecommerce_transactions.csv"

TOTAL_ROWS = 1_000_000
BATCH_SIZE = 50_000
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

products = [
    ("Laptop", "Electronics", 7500000),
    ("Smartphone", "Electronics", 3500000),
    ("Headphones", "Electronics", 450000),
    ("Keyboard", "Accessories", 250000),
    ("Mouse", "Accessories", 150000),
    ("Backpack", "Fashion", 200000),
    ("Shoes", "Fashion", 550000),
    ("T-Shirt", "Fashion", 100000),
    ("Coffee Maker", "Home", 850000),
    ("Blender", "Home", 500000),
]

payment_methods = [
    "Bank Transfer",
    "Credit Card",
    "E-Wallet",
    "Cash on Delivery",
]

cities = [
    "Jakarta",
    "Bandung",
    "Surabaya",
    "Medan",
    "Padang",
    "Yogyakarta",
    "Semarang",
    "Makassar",
    "Palembang",
    "Denpasar",
]

START_DATE = datetime(2025, 1, 1)
DATE_RANGE_DAYS = 365

headers = [
    "transaction_id",
    "customer_id",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "total_amount",
    "payment_method",
    "transaction_date",
    "city",
]


def generate_transaction(index):
    product, category, price = random.choice(products)

    quantity = random.randint(1, 5)
    total_amount = quantity * price

    transaction_date = (
        START_DATE + timedelta(
            days=random.randint(0, DATE_RANGE_DAYS),
            seconds=random.randint(0, 86399),
        )
    )

    return [
        f"TRX{index:09d}",
        f"CUS{random.randint(1, 100000):06d}",
        product,
        category,
        quantity,
        price,
        total_amount,
        random.choice(payment_methods),
        transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
        random.choice(cities),
    ]


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("Starting synthetic dataset generation...")
    print(f"Target rows: {TOTAL_ROWS:,}")
    print(f"Output: {OUTPUT_FILE}")

    with open(
        OUTPUT_FILE,
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)
        writer.writerow(headers)

        for start in range(0, TOTAL_ROWS, BATCH_SIZE):
            end = min(start + BATCH_SIZE, TOTAL_ROWS)

            rows = [
                generate_transaction(index)
                for index in range(start + 1, end + 1)
            ]

            writer.writerows(rows)

            print(
                f"Progress: {end:,}/{TOTAL_ROWS:,} "
                f"({end / TOTAL_ROWS * 100:.1f}%)"
            )

    file_size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)

    print("\nDataset generation completed!")
    print(f"Total records: {TOTAL_ROWS:,}")
    print(f"File size: {file_size_mb:.2f} MB")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
