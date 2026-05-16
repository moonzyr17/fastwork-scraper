#!/usr/bin/env python3
"""
Fastwork Jobboard Scraper - Web Dashboard
Flask app untuk scrape dan visualisasi job listing dari Fastwork Jobboard.
"""

import os
import json
import glob
from datetime import datetime
from flask import Flask, render_template, jsonify
from scraper import scrape_all

app = Flask(__name__)
OUTPUT_DIR = "output"


def get_latest_data() -> dict:
    """Load the most recent scraped JSON file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "fastwork_jobs_*.json")), reverse=True)
    if not files:
        return {"jobs": [], "total": 0, "scraped_at": None}
    with open(files[0], "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(jobs: list) -> str:
    """Save jobs to a timestamped JSON file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUTPUT_DIR, f"fastwork_jobs_{timestamp}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "scraped_at": datetime.now().isoformat(),
            "total": len(jobs),
            "jobs": jobs,
        }, f, ensure_ascii=False, indent=2)
    return path


@app.route("/")
def index():
    data = get_latest_data()
    jobs = data.get("jobs", [])
    scraped_at = data.get("scraped_at")

    # Stats
    categories = {}
    job_types = {}
    for job in jobs:
        cat = job.get("category") or "Lainnya"
        jt = job.get("job_type") or "Tidak diketahui"
        categories[cat] = categories.get(cat, 0) + 1
        job_types[jt] = job_types.get(jt, 0) + 1

    top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:8]
    budgets = [int(j["budget"]) for j in jobs if str(j.get("budget", "")).isdigit() and int(j["budget"]) > 0]
    avg_budget = int(sum(budgets) / len(budgets)) if budgets else 0
    max_budget = max(budgets) if budgets else 0

    return render_template("index.html",
        jobs=jobs,
        total=len(jobs),
        scraped_at=scraped_at,
        top_categories=top_categories,
        job_types=job_types,
        avg_budget=avg_budget,
        max_budget=max_budget,
    )


@app.route("/api/scrape", methods=["POST"])
def api_scrape():
    """Trigger a fresh scrape and return results."""
    try:
        jobs = scrape_all(delay=1.0)
        if not jobs:
            return jsonify({"success": False, "message": "Tidak ada data ditemukan."}), 500
        path = save_json(jobs)
        return jsonify({
            "success": True,
            "total": len(jobs),
            "file": path,
            "scraped_at": datetime.now().isoformat(),
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/jobs")
def api_jobs():
    """Return all jobs as JSON."""
    data = get_latest_data()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
