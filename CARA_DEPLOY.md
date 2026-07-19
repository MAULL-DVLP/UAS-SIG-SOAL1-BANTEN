# Cara Mendapatkan Live URL (Streamlit Community Cloud)

Karena environment ini tidak bisa membuka koneksi ke GitHub/Streamlit Cloud,
langkah publikasi berikut perlu Anda lakukan sendiri (gratis, ±5 menit):

## 1. Coba dulu di komputer sendiri (opsional)
```bash
pip install -r requirements.txt
streamlit run app.py
```
Buka browser ke `http://localhost:8501` untuk melihat peta interaktifnya.

## 2. Upload ke GitHub
1. Buat repository baru di GitHub, misal `webgis-banten-uas`.
2. Upload seluruh isi folder ini: `app.py`, `requirements.txt`, dan folder `data/`
   (berisi 5 file .geojson).

## 3. Deploy ke Streamlit Community Cloud
1. Buka https://share.streamlit.io/ lalu login dengan akun GitHub.
2. Klik **New app** → pilih repository `webgis-banten-uas`.
3. Main file path: `app.py`
4. Klik **Deploy**. Tunggu 1-2 menit sampai build selesai.
5. Anda akan mendapat **Live URL** publik, contoh:
   `https://webgis-banten-uas.streamlit.app`

## 4. Ambil Screenshot untuk deliverable
- Screenshot 1: tampilan penuh peta beserta legenda & layer control.
- Screenshot 2: klik salah satu poligon "Blank Spot" / "Populasi Rentan"
  hingga muncul pop-up info, lalu screenshot.

## Alternatif cepat tanpa GitHub
File `map_preview.html` yang disertakan sudah berisi peta lengkap (statis,
tanpa perlu server Streamlit). Anda bisa membukanya langsung di browser
untuk keperluan screenshot, meskipun untuk deliverable "Live URL" tetap
disarankan deploy ke Streamlit Cloud sesuai langkah di atas.
