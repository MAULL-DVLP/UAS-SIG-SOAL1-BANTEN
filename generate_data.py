"""
generate_data.py
Membuat data spasial DUMMY/SINTETIS untuk Proyek UAS SIG:
"Peta Interaktif Aksesibilitas Taman Bermain Layak Anak & Tingkat
Kerentanan ISPA/Stunting di Provinsi Banten"

Data ini BUKAN data resmi Dinas Kesehatan/DP3AKB Banten, melainkan
data tiruan yang dibuat untuk mensimulasikan struktur & atribut data
riil, karena data asli tidak tersedia untuk mahasiswa.

Output: 5 file GeoJSON di folder ./data
"""

import json
import random
from shapely.geometry import Point, mapping
from shapely.ops import unary_union

random.seed(42)

# ------------------------------------------------------------------
# 1. Area kajian: kawasan industri Tangerang & sekitarnya, Banten
#    (kotak perkiraan, cukup untuk simulasi, bukan batas administrasi resmi)
# ------------------------------------------------------------------
LAT_MIN, LAT_MAX = -6.28, -6.05
LON_MIN, LON_MAX = 106.55, 106.75

NAMA_DESA = [
    "Kadu Agung", "Cikupa Baru", "Pasar Kemis", "Sukamulya", "Balaraja Timur",
    "Curug Wetan", "Jatiuwung", "Periuk Jaya", "Cibodas Sari", "Panunggangan",
    "Batuceper", "Neglasari", "Karawaci Indah", "Cikokol", "Sepatan Timur",
    "Kutabumi", "Mekar Jaya", "Suka Asih", "Talaga Sari", "Gembor"
]

def rand_point():
    lat = random.uniform(LAT_MIN, LAT_MAX)
    lon = random.uniform(LON_MIN, LON_MAX)
    return lat, lon

def buffer_deg(lat, lon, meters):
    """Buffer sederhana dalam derajat (aproksimasi lokal, cukup untuk visual)."""
    deg = meters / 111_000  # 1 derajat lintang approx 111 km
    return Point(lon, lat).buffer(deg)

# ------------------------------------------------------------------
# 2. Titik Taman Bermain Layak Anak
# ------------------------------------------------------------------
taman_features = []
buffer_features = []
N_TAMAN = 14
for i in range(N_TAMAN):
    lat, lon = rand_point()
    nama = f"Taman Bermain {NAMA_DESA[i % len(NAMA_DESA)]}"
    ramah_anak = random.choice([True, True, True, False])  # mayoritas ramah anak
    kapasitas = random.choice([20, 30, 40, 50, 75, 100])

    taman_features.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "nama_taman": nama,
            "fasilitas_ramah_anak": "Ya" if ramah_anak else "Tidak",
            "kapasitas_maks_anak": kapasitas
        }
    })

    buf = buffer_deg(lat, lon, 500)
    buffer_features.append({
        "type": "Feature",
        "geometry": mapping(buf),
        "properties": {"nama_taman": nama, "radius_meter": 500}
    })

with open("data/taman_bermain.geojson", "w") as f:
    json.dump({"type": "FeatureCollection", "features": taman_features}, f)

with open("data/buffer_taman.geojson", "w") as f:
    json.dump({"type": "FeatureCollection", "features": buffer_features}, f)

# ------------------------------------------------------------------
# 3. Zona Paparan Polusi Industri / Jalan Raya Utama
# ------------------------------------------------------------------
polusi_features = []
N_POLUSI = 6
for i in range(N_POLUSI):
    lat, lon = rand_point()
    radius_m = random.choice([700, 900, 1100, 1300])
    zona = buffer_deg(lat, lon, radius_m)
    sumber = random.choice(["Kawasan Industri", "Jalan Raya Utama"])
    polusi_features.append({
        "type": "Feature",
        "geometry": mapping(zona),
        "properties": {"sumber_paparan": sumber, "radius_meter": radius_m}
    })

with open("data/zona_polusi.geojson", "w") as f:
    json.dump({"type": "FeatureCollection", "features": polusi_features}, f)

# ------------------------------------------------------------------
# 4. Blank Spot Taman Bermain (RW/Desa padat penduduk tanpa fasilitas)
# ------------------------------------------------------------------
blankspot_features = []
N_BLANK = 8
used_names = random.sample(NAMA_DESA, N_BLANK)
total_balita_rentan = 0
for nama_desa in used_names:
    lat, lon = rand_point()
    size = random.uniform(0.006, 0.012)
    poly = Point(lon, lat).buffer(size, cap_style=3)  # kotak kasar
    jumlah_balita = random.randint(120, 420)
    jumlah_kasus = random.randint(15, 90)
    total_balita_rentan += jumlah_kasus
    blankspot_features.append({
        "type": "Feature",
        "geometry": mapping(poly),
        "properties": {
            "nama_desa": nama_desa,
            "jumlah_balita": jumlah_balita,
            "jumlah_kasus_ispa_stunting": jumlah_kasus,
            "status_wilayah": "Blank Spot"
        }
    })

with open("data/blank_spot.geojson", "w") as f:
    json.dump({"type": "FeatureCollection", "features": blankspot_features}, f)

# ------------------------------------------------------------------
# 5. Populasi Anak Rentan Kesehatan (gradasi Kuning -> Merah)
# ------------------------------------------------------------------
populasi_features = []
N_POP = 12
used_names2 = random.sample(NAMA_DESA, N_POP)
for nama_desa in used_names2:
    lat, lon = rand_point()
    size = random.uniform(0.005, 0.010)
    poly = Point(lon, lat).buffer(size, cap_style=3)
    jumlah_balita = random.randint(100, 500)
    jumlah_kasus = random.randint(5, 110)
    status = "Terlayani" if random.random() > 0.35 else "Blank Spot"
    populasi_features.append({
        "type": "Feature",
        "geometry": mapping(poly),
        "properties": {
            "nama_desa": nama_desa,
            "jumlah_balita": jumlah_balita,
            "jumlah_kasus_ispa_stunting": jumlah_kasus,
            "status_wilayah": status
        }
    })

with open("data/populasi_rentan.geojson", "w") as f:
    json.dump({"type": "FeatureCollection", "features": populasi_features}, f)

print("Selesai. File tersimpan di folder data/:")
print(" - taman_bermain.geojson   :", N_TAMAN, "titik")
print(" - buffer_taman.geojson    :", N_TAMAN, "poligon buffer 500m")
print(" - zona_polusi.geojson     :", N_POLUSI, "poligon")
print(" - blank_spot.geojson      :", N_BLANK, "poligon, total kasus rentan:", total_balita_rentan)
print(" - populasi_rentan.geojson :", N_POP, "poligon")
