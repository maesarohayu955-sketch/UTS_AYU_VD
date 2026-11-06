# 🎬 NETFLIX CONTENT ANALYTICS: Exploring Movies and TV Shows Around the World
### Dashboard Analisis Data & Visualisasi Interaktif Berbasis Python & Streamlit
**Proyek Ujian Tengah Semester (UTS) — Mata Kuliah Visualisasi Data**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-E50914?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dataset](https://img.shields.io/badge/Dataset-Kaggle%20Netflix-blue?logo=kaggle)](https://www.kaggle.com/datasets/shivamb/netflix-shows)

---

## 📌 1. Identitas Mahasiswa & Akademik

| Informasi | Keterangan |
| :--- | :--- |
| **Nama Lengkap** | **Ayu Maesaroh** |
| **Nomor Induk Mahasiswa (NIM)** | **241041010** |
| **Program Studi** | **Manajemen Informatika** |
| **Mata Kuliah** | Visualisasi Data (UTS) |
| **Dosen Pengampu** | **Muryan Awaludin, S.Kom, M.Kom** |
| **Tautan Live Dashboard** | `[Isi Tautan Streamlit Community Cloud Setelah Deploy]` |
| **Repositori GitHub** | `[Isi Tautan Repositori GitHub Anda]` |

---

## 📖 2. Deskripsi Proyek

**Netflix Content Analytics** adalah aplikasi dashboard analitik interaktif berbasis web yang dibangun untuk mengeksplorasi secara mendalam katalog film (*Movies*) dan serial televisi (*TV Shows*) yang tersedia di platform Netflix secara global hingga tahun 2021. 

Aplikasi ini dirancang dengan standar antarmuka profesional bertaraf industri, mengadopsi identitas visual khas Netflix: **Pitch Black (`#000000`)**, aksen **Netflix Red (`#E50914`)**, dan tipografi modern yang responsif. Seluruh visualisasi dibuat dinamis dan interaktif menggunakan **Plotly**, memungkinkan pengguna melakukan eksplorasi multi-sudut pandang mulai dari tren pertumbuhan tahunan, dominasi geografis produksi, taksonomi genre, hingga segmentasi klasifikasi usia penonton.

> [!NOTE]  
> **Karakteristik Data:** Seluruh data yang dianalisis dalam proyek ini merupakan metadata katalog (*titles, genres, release year, countries, ratings, durations*), **bukan data jumlah penonton (*viewership*) atau statistik *streaming jam tonton***. Oleh karena itu, kesimpulan ditarik murni berdasarkan penawaran katalog (*supply/inventory analysis*).

---

## 🎯 3. Fitur Utama Dashboard

Dashboard terbagi ke dalam **6 Menu Halaman Fungsional** yang dapat diakses melalui sidebar:

1. **📊 1. Overview**
   - **4 KPI Cards Otomatis:** Total Konten (8,807 judul), Total Movies (6,131 judul), Total TV Shows (2,676 judul), dan Total Negara Terlibat (122 negara).
   - **Donut Chart:** Rasio perbandingan volume Movie vs TV Show.
   - **Line Chart Interaktif:** Tren evolusi konten berdasarkan tahun rilis historis (1980 - 2021).
   - **Horizontal Bar Charts:** Top 10 negara produsen terbanyak dan Top 10 genre paling dominan.
   - **Key Analytical Storytelling Cards:** Ringkasan temuan strategis dari dataset.

2. **🎬 2. Content Analysis**
   - **Distribusi Format per Tahun Rilis:** Stacked bar chart interaktif dengan slider rentang tahun dinamis.
   - **Tren Penambahan Konten (*date_added*):** Area chart penambahan konten baru ke server Netflix per tahun, memperlihatkan lonjakan ekspansi platform.
   - **Karakteristik Durasi Film:** Histogram sebaran menit durasi film beserta garis penanda *mean* (99.6 menit) dan *median* (98 menit).
   - **Karakteristik Musim Serial TV:** Distribusi jumlah musim (*seasons*), menyoroti dominasi serial 1-musim (*limited series*).

3. **🏷️ 3. Genre Analysis**
   - **Top 10 Genre Netflix:** Perhitungan frekuensi genre murni setelah proses *data exploding* pada kolom multi-genre (*listed_in*).
   - **Komparasi Genre Movie vs TV Show:** Membedah perbedaan karakteristik tema film lepas dan serial bersambung.
   - **Heatmap Hubungan Genre vs Tahun Rilis:** Visualisasi intensitas rilis genre populer selama 10 tahun terakhir (2012 - 2021).

4. **🌍 4. Country Analysis**
   - **World Choropleth Map Interaktif:** Peta dunia tematik gelap dengan skala intensitas merah Netflix yang memetakan konsentrasi produksi konten di 122 negara.
   - **Pemisahan Entri Multi-Negara:** Parsing koma (*comma-splitting*) untuk memastikan akurasi data produksi kolaborasi antarnegara.
   - **Komposisi Movie vs TV Show per Negara:** Komparasi orientasi produksi negara (misal dominasi film di India vs dominasi serial di Jepang & Korea Selatan).
   - **Spotlight Cards:** Kartu analisis khusus untuk sentra produksi Amerika Utara, Asia Selatan, dan Asia Timur.

5. **🎯 5. Rating Analysis**
   - **Distribusi Klasifikasi Usia:** Bar chart frekuensi rating (TV-MA, TV-14, TV-PG, R, PG-13, dll).
   - **Donut Chart Segmentasi Audiens:** Pengelompokan rating ke dalam segmen Dewasa (*Mature*), Remaja (*Teens*), Bimbingan Orang Tua (*Parental Guidance*), dan Anak-anak (*Kids/Family*).
   - **Komparasi Rating per Format Konten:** Membandingkan orientasi rating antara Movie dan TV Show.
   - **Panduan Tabel Klasifikasi:** Definisi resmi dan batasan konten untuk masing-masing rating.

6. **🔍 6. Data Explorer**
   - **Pencarian Real-Time:** Filter kata kunci instan berdasarkan judul, nama sutradara, nama pemeran, atau sinopsis.
   - **Filter Multi-Kriteria:** Format konten, rentang tahun rilis, klasifikasi rating, genre, dan negara produksi.
   - **Indikator Metrik Dinamis:** Menghitung jumlah dan persentase data yang lolos penyaringan secara *real-time*.
   - **Tombol Download CSV:** Ekspor dataset hasil filter ke dalam berkas CSV siap pakai.
   - **Title Inspector:** Penampil rincian detail film/serial (sinopsis, sutradara, pemeran, durasi, rating) dalam format kartu visual elegan.

---

## 💡 4. Minimal 5 Key Analytical Insights (Berbasis Data Aktual)

Berdasarkan hasil kalkulasi algoritma data pada berkas `analysis/data_analysis.py`, diperoleh temuan faktual berikut:

### 1. Dominasi Signifikan Format Movie
* **Statistik Data:** **6,131 Film (69.6%)** berbanding **2,676 Serial TV (30.4%)**.
* **Insight:** Sekitar 7 dari setiap 10 judul di katalog Netflix adalah film lepas (*Movie*). Hal ini membuktikan bahwa strategi awal kurasi Netflix berfokus pada volume film layar lebar yang memiliki komitmen waktu tonton sekali tuntas (*single-session consumption*) bagi pengguna.

### 2. Puncak Rilis & Agresi Akuisisi Platform
* **Statistik Data:** Puncak tahun produksi/rilis: **2018 (1,147 judul)**. Puncak penambahan ke katalog (*date_added*): **2019 (2,016 judul baru)**.
* **Insight:** Terjadi lonjakan eksponensial penambahan konten ke platform streaming antara tahun 2017 hingga 2019, sebelum akhirnya mengalami penurunan laju akibat pergeseran strategi ke *original high-budget productions* serta disrupsi pandemi global pada industri perfilman pada tahun 2020–2021.

### 3. Amerika Serikat Sebagai Kiblat Utama & Kekuatan Poros Asia
* **Statistik Data:** **United States (3,690 judul, ~41.9% dari seluruh katalog)**, disusul **India (1,046 judul)** dan **United Kingdom (806 judul)** dari total **122 negara**.
* **Insight:** Amerika Serikat tetap memimpin pangsa katalog secara dominan. Namun, India menjadi kekuatan terbesar kedua dengan spesialisasi film Bollywood (88% berupa film), sementara kawasan Asia Timur (Jepang dengan 318 judul dan Korea Selatan dengan 231 judul) memiliki rasio *TV Show* tertinggi melalui anime dan K-Drama.

### 4. Internasionalisasi Konten Menjadi Genre Terbesar
* **Statistik Data:** Genre terpopuler adalah **'International Movies' (2,752 kemunculan)**, diikuti oleh **'Dramas' (2,427 kemunculan)** dan **'Comedies' (1,674 kemunculan)**.
* **Insight:** Penempatan *International Movies* di urutan pertama menegaskan transformasi strategi Netflix dari penyedia konten domestik Amerika menjadi kurator bioskop dunia, yang mendistribusikan karya sineas lintas bahasa dan budaya ke audiens global.

### 5. Fokus Utama pada Segmen Audiens Dewasa (*TV-MA*)
* **Statistik Data:** **TV-MA menduduki 3,207 judul (36.4%)**, diikuti oleh **TV-14 sebanyak 2,160 judul (24.5%)**.
* **Insight:** Lebih dari 60% katalog Netflix ditujukan khusus untuk penonton usia remaja akhir dan dewasa. Hal ini memberikan kebebasan kreatif bagi para kreator untuk mengeksplorasi tema narasi yang lebih kompleks, gelap, dan realistis tanpa pembatasan ketat seperti televisi siaran publik.

### 6. Karakteristik Durasi: Standardisasi Bioskop & Fenomena 1-Musim
* **Statistik Data:** Rata-rata durasi film: **99.6 menit** (median 98 menit). Serial TV yang hanya memiliki 1 Season: **67.0%**.
* **Insight:** Mayoritas film Netflix dirancang dalam durasi klasik 1.5 hingga 2 jam. Di sisi lain, 2 dari 3 serial TV di Netflix berhenti pada *Season 1*, yang mencerminkan tingginya tren *miniseries / limited series* serta kebijakan seleksi ketat Netflix dalam memperpanjang serial ke musim berikutnya berdasarkan performa retensi penonton.

---

## 🛠️ 5. Teknologi & Pustaka yang Digunakan

* **Bahasa Pemrograman:** [Python 3.10+](https://www.python.org/)
* **Framework Web & Dashboard:** [Streamlit](https://streamlit.io/)
* **Manipulasi & Analisis Data:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Visualisasi Interaktif:** [Plotly Express](https://plotly.com/python/plotly-express/) & [Plotly Graph Objects](https://plotly.com/python/graph-objects/)
* **Styling & User Experience:** Custom CSS3 (Pitch Black Netflix UI Theme)

---

## 📂 6. Struktur Direktori Proyek

```text
netflix-content-analytics/
│
├── app.py                      # Skrip utama aplikasi web Streamlit
├── requirements.txt            # Daftar pustaka dependensi Python
├── README.md                   # Dokumentasi lengkap proyek & panduan deployment
│
├── data/
│   ├── netflix_titles.csv      # Dataset mentah dari Kaggle
│   └── netflix_cleaned.csv     # Dataset hasil pembersihan & rekayasa fitur
│
├── assets/
│   └── style.css               # Berkas CSS kustom (Tema Hitam Pekat & Merah Netflix)
│
└── analysis/
    └── data_analysis.py        # Modul data cleaning, sanitasi, dan ekstraksi insight
```

---

## 🧹 7. Metodologi Data Cleaning & Preprocessing

Proses sanitasi data diimplementasikan secara otomatis dalam `analysis/data_analysis.py` dengan tahapan berikut:

1. **Koreksi Anomali Baris (Misplaced Duration):**
   Pada dataset Kaggle, terdapat anomali pada baris judul komedi spesial Louis C.K. (`show_id`: s5542, s5795, s5813) dimana nilai durasi (misal `'74 min'`) tertukar masuk ke kolom `rating`, menyebabkan kolom `duration` menjadi `NaN`. Skrip mendeteksi pola ini, memindahkan nilai durasi ke kolom yang tepat, dan mengisi rating dengan `'NR'` (*Not Rated*).
2. **Penanganan Missing Values:**
   - Kolom `director`, `cast`, dan `country` yang bernilai `NaN` diisi dengan label `'Unknown'` / `'Unknown Country'` agar tidak menghilangkan baris data secara sembarangan.
   - Kolom `rating` diisi dengan `'Not Rated'`.
   - Normalisasi rating: mengubah label ambigu `'UR'` menjadi `'NR'`.
3. **Standarisasi & Ekstraksi Temporal (*date_added*):**
   - Mengonversi format teks tanggal (contoh: `"September 25, 2021"`) menjadi objek `datetime`.
   - Mengimputasi ~10 baris dengan nilai tanggal kosong menggunakan tanggal 1 Januari dari `release_year`.
   - Mengekstraksi fitur turunan: `year_added`, `month_added`, `month_name_added`, dan `year_month_added`.
4. **Pembersihan Kolom Durasi:**
   - Mengekstraksi angka integer dari kolom durasi ke dalam `duration_int`.
   - Menetapkan unit durasi ke dalam `duration_unit` (`'Minutes'` untuk Movie, `'Season'`/`'Seasons'` untuk TV Show).
5. **Penanganan Nilai Multi-Kategori (*Multi-Valued Splitting*):**
   - Kolom `country` dan `listed_in` (genre) memuat beberapa nilai yang dipisahkan tanda koma. Dibuat fungsi helper `get_exploded_countries()` dan `get_exploded_genres()` menggunakan teknik `.explode()` agar setiap entitas negara dan genre terhitung secara independen dan akurat.

---

## 💻 8. Panduan Menjalankan Aplikasi Secara Lokal

### Prasyarat
- Komputer telah terpasang **Python 3.10** atau versi lebih baru.
- Editor teks / IDE seperti **Visual Studio Code (VS Code)** atau terminal/command prompt.

### Langkah demi Langkah:

1. **Buka Terminal / Command Prompt** dan navigasikan ke folder proyek:
   ```bash
   cd path/to/netflix-content-analytics
   ```

2. **(Opsional namun Direkomendasikan) Buat Virtual Environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Seluruh Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Proses Data Cleaning & Analisis (Opsional, sudah otomatis dilakukan jika belum ada):**
   ```bash
   python analysis/data_analysis.py
   ```

5. **Jalankan Aplikasi Streamlit:**
   ```bash
   streamlit run app.py
   ```

6. **Buka Browser:**  
   Streamlit akan secara otomatis membuka jendela browser di:
   ```text
   Local URL: http://localhost:8501
   ```

---

## 🚀 9. Panduan Publikasi ke GitHub & Streamlit Community Cloud

### Bagian A: Unggah ke GitHub

1. **Inisialisasi Git pada Folder Proyek:**
   Buka terminal di folder `netflix-content-analytics`:
   ```bash
   git init
   ```

2. **Buat Berkas `.gitignore`:**
   Pastikan folder `venv` tidak ikut terunggah:
   ```bash
   echo "venv/" > .gitignore
   echo "__pycache__/" >> .gitignore
   echo ".vscode/" >> .gitignore
   ```

3. **Tambahkan dan Commit Berkas:**
   ```bash
   git add .
   git commit -m "feat: Initial commit Netflix Content Analytics Dashboard for UTS"
   ```

4. **Hubungkan ke Repositori GitHub Anda:**
   - Buka [GitHub](https://github.com), buat repositori baru dengan nama `netflix-content-analytics` (pilih Public).
   - Salin perintah push yang diberikan GitHub, contoh:
   ```bash
   git branch -M main
   git remote add origin https://github.com/[username-anda]/netflix-content-analytics.git
   git push -u origin main
   ```

---

### Bagian B: Deploy ke Streamlit Community Cloud (Gratis)

1. Buka situs [Streamlit Community Cloud](https://share.streamlit.io/) dan login menggunakan akun GitHub Anda.
2. Klik tombol **"New app"** di pojok kanan atas.
3. Pada form konfigurasi:
   - **Repository:** Pilih repositori Anda (`[username-anda]/netflix-content-analytics`).
   - **Branch:** Pilih `main`.
   - **Main file path:** Ketik `app.py`.
4. Klik **"Deploy!"**.
5. Tunggu proses build selesai (~1-2 menit). Aplikasi Anda akan memiliki tautan publik aktif (contoh: `https://[nama-anda]-netflix-analytics.streamlit.app`).
6. Salin tautan publik tersebut dan cantumkan ke dalam laporan tugas serta bagian tabel identitas di atas!

---

## 🖼️ 10. Preview Tampilan Dashboard

*Tampilan visual dashboard konsisten bernuansa gelap bioskop khas Netflix:*

```text
+---------------------------------------------------------------------------------------+
|  NETFLIX  |  NETFLIX CONTENT ANALYTICS                                                |
|  -------- |  Exploring Movies and TV Shows Around the World                           |
|  OVERVIEW |                                                                           |
|  CONTENT  |  +---------------+ +---------------+ +---------------+ +---------------+  |
|  GENRE    |  | TOTAL KONTEN  | | TOTAL MOVIES  | | TOTAL TV SHOW | | TOTAL NEGARA  |  |
|  COUNTRY  |  |    8,807      | | 6,131 (69.6%) | | 2,676 (30.4%) | |  122 NEGARA   |  |
|  RATING   |  +---------------+ +---------------+ +---------------+ +---------------+  |
|  EXPLORER |                                                                           |
|           |  [ Donut Chart: Format ]      [ Line Chart: Pertumbuhan Rilis Tahunan ]   |
|           |  [ Bar: Top 10 Negara ]       [ Bar: Top 10 Genre Paling Populer ]        |
+---------------------------------------------------------------------------------------+
```

---

## 📄 11. Lisensi & Sumber Data

* **Sumber Dataset:** Kaggle — *Netflix Movies and TV Shows Dataset* oleh Shivam Bansal ([Link Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows)).
* **Lisensi Penggunaan:** Proyek ini dibuat untuk keperluan akademik Ujian Tengah Semester (UTS) mata kuliah Visualisasi Data dan dilisensikan di bawah [MIT License](LICENSE).
