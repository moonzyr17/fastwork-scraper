#!/usr/bin/env python3
"""
Fastwork Jobboard Scraper
Scrapes all job listings from jobboard.fastwork.id and exports to CSV & JSON.
"""

import requests
import json
import csv
import time
import os
from datetime import datetime


API_BASE = "https://jobboard-api.fastwork.id/api/jobs"
OUTPUT_DIR = "output"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
    "Origin": "https://jobboard.fastwork.id",
    "Referer": "https://jobboard.fastwork.id/",
}


def fetch_page(page: int, page_size: int = 20) -> dict:
    """Fetch a single page of job listings from the API."""
    params = {
        "page": page,
        "page_size": page_size,
        "order_by[]": "inserted_at",
        "order_directions[]": "desc",
    }
    response = requests.get(API_BASE, headers=HEADERS, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def parse_jobs(items: list) -> list:
    """Normalize job listing fields."""
    jobs = []
    for job in items:
        category = job.get("category", {})
        jobs.append({
            "id": job.get("id", ""),
            "title": job.get("title", ""),
            "category": category.get("name", "") if isinstance(category, dict) else str(category),
            "job_type": job.get("job_type", ""),
            "budget": job.get("budget", ""),
            "currency": "IDR",
            "description": job.get("description", ""),
            "posted_at": job.get("inserted_at", ""),
            "deadline": job.get("deadline", ""),
            "url": f"https://jobboard.fastwork.id/jobs/{job.get('id', '')}",
        })
    return jobs


def scrape_all(delay: float = 1.0) -> list:
    """Scrape all pages of job listings."""
    all_jobs = []
    page = 1

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Mulai scraping Fastwork Jobboard API...")

    while True:
        try:
            print(f"  → Halaman {page}...", end=" ", flush=True)
            data = fetch_page(page)

            # Handle response structure
            items = data.get("data", [])
            if isinstance(items, dict):
                items = items.get("data", [])

            if not items:
                print("tidak ada data, selesai.")
                break

            jobs = parse_jobs(items)
            all_jobs.extend(jobs)

            # Pagination info
            meta = data.get("meta", {})
            total_pages = meta.get("total_pages", 1)
            total_count = meta.get("total_count", len(all_jobs))

            print(f"{len(jobs)} job (total: {len(all_jobs)} / {total_count})")

            if page >= int(total_pages):
                print(f"  → Semua {total_pages} halaman selesai.")
                break

            page += 1
            time.sleep(delay)

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            break
        except requests.exceptions.ConnectionError:
            print("Koneksi gagal, retry...")
            time.sleep(5)
            continue
        except Exception as e:
            print(f"Error: {e}")
            break

    return all_jobs


def save_json(jobs: list, filepath: str):
    """Save jobs to JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({
            "scraped_at": datetime.now().isoformat(),
            "total": len(jobs),
            "jobs": jobs,
        }, f, ensure_ascii=False, indent=2)
    print(f"  ✓ JSON: {filepath}")


def save_csv(jobs: list, filepath: str):
    """Save jobs to CSV file."""
    if not jobs:
        return
    fieldnames = ["id", "title", "category", "job_type", "budget", "currency",
                  "description", "posted_at", "deadline", "url"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)
    print(f"  ✓ CSV: {filepath}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    jobs = scrape_all(delay=1.0)

    if not jobs:
        print("Tidak ada data yang berhasil di-scrape.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(OUTPUT_DIR, f"fastwork_jobs_{timestamp}.json")
    csv_path = os.path.join(OUTPUT_DIR, f"fastwork_jobs_{timestamp}.csv")

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Menyimpan {len(jobs)} job...")
    save_json(jobs, json_path)
    save_csv(jobs, csv_path)

    print(f"\n✅ Selesai! Total {len(jobs)} job berhasil di-scrape.")
    print(f"   Output tersimpan di: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
