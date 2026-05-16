# Fastwork Jobboard Scraper

Scraper untuk mengambil semua listing pekerjaan dari [jobboard.fastwork.id](https://jobboard.fastwork.id) dan mengekspornya ke format CSV dan JSON.

## Fitur

- Scrape semua halaman job listing secara otomatis
- Export ke **CSV** dan **JSON**
- Menampilkan progress scraping secara real-time
- Delay antar request untuk menghindari rate limiting
- Penanganan error dan retry otomatis

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

## Instalasi

```bash
git clone https://github.com/moonzyr17/fastwork-scraper.git
cd fastwork-scraper
pip install requests
```

## Penggunaan

```bash
python3 scraper.py
```

Output akan tersimpan di folder `output/` dengan format nama:
```
output/fastwork_jobs_YYYYMMDD_HHMMSS.json
output/fastwork_jobs_YYYYMMDD_HHMMSS.csv
```

## Contoh Output

**JSON:**
```json
{
  "scraped_at": "2026-05-16T17:40:52",
  "total": 275,
  "jobs": [
    {
      "id": "abc123",
      "title": "Saya mencari freelance desain logo",
      "category": "Desain Grafis",
      "job_type": "Freelance",
      "budget": "500000",
      "currency": "IDR",
      "description": "...",
      "posted_at": "2026-05-16T10:00:00",
      "deadline": "2026-05-20",
      "url": "https://jobboard.fastwork.id/jobs/abc123"
    }
  ]
}
```

**CSV:**
```
id,title,category,job_type,budget,currency,description,posted_at,deadline,url
abc123,Saya mencari freelance desain logo,Desain Grafis,Freelance,500000,IDR,...
```

## Requirements

- Python 3.7+
- `requests`

## Catatan

- Scraper menggunakan delay 1 detik antar halaman untuk menghormati server
- Data yang diambil bersifat publik dan tersedia di halaman jobboard
- Gunakan secara bertanggung jawab

## Lisensi

MIT License
