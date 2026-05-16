# Fastwork Jobboard Scraper

Scraper + web dashboard untuk mengambil dan memvisualisasikan semua listing pekerjaan dari [jobboard.fastwork.id](https://jobboard.fastwork.id).

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Flask](https://img.shields.io/badge/Flask-3.1-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## Fitur

- Scrape semua halaman job listing secara otomatis
- Web dashboard dengan statistik dan grafik interaktif
- Filter dan pencarian real-time
- Export ke **CSV** dan **JSON**
- Tombol scrape on-demand dari dashboard
- Delay antar request untuk menghindari rate limiting

## Screenshot

Dashboard menampilkan:
- Total job, kategori, rata-rata budget, budget tertinggi
- Bar chart top kategori
- Doughnut chart tipe pekerjaan
- Tabel lengkap dengan search & filter

## Instalasi

```bash
git clone https://github.com/moonzyr17/fastwork-scraper.git
cd fastwork-scraper

# Buat virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# atau .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## Penggunaan

### Scraper saja (CLI)

```bash
python3 scraper.py
```

Output tersimpan di `output/fastwork_jobs_YYYYMMDD_HHMMSS.json` dan `.csv`

### Web Dashboard

```bash
python3 app.py
```

Buka browser ke `http://localhost:5000`

- Klik **Scrape Sekarang** untuk mengambil data terbaru
- Gunakan kolom pencarian untuk filter job
- Filter berdasarkan tipe pekerjaan (Freelance, Full-time, dll)

## Data yang Diambil

| Field | Deskripsi |
|---|---|
| `id` | ID unik job |
| `title` | Judul pekerjaan |
| `category` | Kategori pekerjaan |
| `job_type` | Tipe (Freelance, Full-time, Part-time, dll) |
| `budget` | Budget dalam IDR |
| `description` | Deskripsi pekerjaan |
| `posted_at` | Tanggal diposting |
| `deadline` | Batas waktu pengiriman |
| `url` | Link langsung ke job listing |

## API Endpoints

| Endpoint | Method | Deskripsi |
|---|---|---|
| `/` | GET | Dashboard utama |
| `/api/jobs` | GET | Semua job dalam format JSON |
| `/api/scrape` | POST | Trigger scrape baru |

## Requirements

- Python 3.7+
- Flask
- requests

## Lisensi

MIT License
