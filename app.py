"""
UAS - Sistem Informasi Geografis (W182500032)
Soal No. 1: Peta Interaktif Aksesibilitas Taman Bermain Layak Anak &
Tingkat Kerentanan ISPA/Stunting di Provinsi Banten

Tool: Low-Code Python -> Streamlit + Folium
Catatan: Seluruh data pada folder data/ adalah data SINTETIS (dummy)
yang dibuat dengan generate_data.py, digunakan untuk mensimulasikan
data resmi Dinas Kesehatan & DP3AKB Provinsi Banten.
"""

import json
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Peta Anak Sehat Banten", layout="wide")

DATA_DIR = "data"

def load_geojson(name):
    with open(f"{DATA_DIR}/{name}") as f:
        return json.load(f)

taman = load_geojson("taman_bermain.geojson")
buffer_taman = load_geojson("buffer_taman.geojson")
zona_polusi = load_geojson("zona_polusi.geojson")
blank_spot = load_geojson("blank_spot.geojson")
populasi = load_geojson("populasi_rentan.geojson")

# Judul & ringkasan eksekutif
st.title("🧒 Peta Aksesibilitas Taman Bermain & Kerentanan Kesehatan Anak Banten")
n_blankspot = len(blank_spot["features"])
total_kasus = sum(f["properties"]["jumlah_kasus_ispa_stunting"] for f in blank_spot["features"])
st.markdown(
    f"**Ringkasan Eksekutif:** Ditemukan **{n_blankspot} RW/Desa** di kawasan industri "
    f"Tangerang, Banten yang merupakan *blank spot* taman bermain, dengan total sekitar "
    f"**{total_kasus} anak balita** tercatat rentan/terpapar kasus ISPA maupun stunting. "
    f"Wilayah ini perlu menjadi prioritas pembangunan *playground* baru yang berjarak aman "
    f"dari zona paparan polusi industri. *(Data pada peta ini bersifat simulasi/dummy untuk keperluan tugas akademik.)*"
)

# Peta dasar, dipusatkan di kawasan kajian
m = folium.Map(location=[-6.17, 106.65], zoom_start=12, tiles="CartoDB positron")

# 1. Zona Paparan Polusi (Oranye transparan)
fg_polusi = folium.FeatureGroup(name="🟧 Zona Paparan Polusi Industri/Jalan Utama")
for feat in zona_polusi["features"]:
    p = feat["properties"]
    folium.GeoJson(
        feat,
        style_function=lambda x: {"fillColor": "orange", "color": "orange",
                                   "fillOpacity": 0.35, "weight": 1},
        tooltip=f"Sumber: {p['sumber_paparan']} (radius {p['radius_meter']}m)"
    ).add_to(fg_polusi)
fg_polusi.add_to(m)

# 2. Buffer 500m Taman Bermain (Hijau transparan)
fg_buffer = folium.FeatureGroup(name="🟩 Buffer 500m Taman Bermain (Zona Aman Jalan Kaki)")
for feat in buffer_taman["features"]:
    folium.GeoJson(
        feat,
        style_function=lambda x: {"fillColor": "green", "color": "green",
                                   "fillOpacity": 0.15, "weight": 1},
        tooltip=feat["properties"]["nama_taman"]
    ).add_to(fg_buffer)
fg_buffer.add_to(m)

# 3. Blank Spot Taman Bermain (Merah)
fg_blank = folium.FeatureGroup(name="🟥 Blank Spot Taman Bermain (Prioritas)")
for feat in blank_spot["features"]:
    p = feat["properties"]
    popup_html = (f"<b>{p['nama_desa']}</b><br>"
                  f"Jumlah Balita: {p['jumlah_balita']}<br>"
                  f"Jumlah Anak Rentan: {p['jumlah_kasus_ispa_stunting']}<br>"
                  f"Kasus ISPA/Stunting: {p['jumlah_kasus_ispa_stunting']}<br>"
                  f"Status: {p['status_wilayah']}")
    tooltip_html = (f"<b>Desa/RW:</b> {p['nama_desa']}<br>"
                    f"<b>Balita:</b> {p['jumlah_balita']}<br>"
                    f"<b>Kasus ISPA/Stunting:</b> {p['jumlah_kasus_ispa_stunting']}<br>"
                    f"<b>Status:</b> {p['status_wilayah']}")
    folium.GeoJson(
        feat,
        style_function=lambda x: {"fillColor": "red", "color": "darkred",
                                   "fillOpacity": 0.5, "weight": 1},
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=folium.Tooltip(tooltip_html)
    ).add_to(fg_blank)
fg_blank.add_to(m)

# 4. Populasi Anak Rentan Kesehatan (gradasi Kuning -> Merah)
def warna_gradasi(jumlah_kasus):
    if jumlah_kasus < 30:
        return "#ffff66"      # kuning muda
    elif jumlah_kasus < 60:
        return "#ffcc00"      # kuning-oranye
    elif jumlah_kasus < 90:
        return "#ff6600"      # oranye tua
    else:
        return "#cc0000"      # merah

fg_populasi = folium.FeatureGroup(name="🟨 Populasi Anak Rentan Kesehatan (Gradasi)")
for feat in populasi["features"]:
    p = feat["properties"]
    popup_html = (f"<b>{p['nama_desa']}</b><br>"
                  f"Jumlah Balita: {p['jumlah_balita']}<br>"
                  f"Jumlah Anak Rentan: {p['jumlah_kasus_ispa_stunting']}<br>"
                  f"Kasus ISPA/Stunting: {p['jumlah_kasus_ispa_stunting']}<br>"
                  f"Status: {p['status_wilayah']}")
    warna = warna_gradasi(p["jumlah_kasus_ispa_stunting"])
    tooltip_html = (f"<b>Desa/RW:</b> {p['nama_desa']}<br>"
                    f"<b>Balita:</b> {p['jumlah_balita']}<br>"
                    f"<b>Kasus ISPA/Stunting:</b> {p['jumlah_kasus_ispa_stunting']}<br>"
                    f"<b>Status:</b> {p['status_wilayah']}")
    folium.GeoJson(
        feat,
        style_function=lambda x, warna=warna: {"fillColor": warna, "color": "grey",
                                                "fillOpacity": 0.6, "weight": 1},
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=folium.Tooltip(tooltip_html)
    ).add_to(fg_populasi)
fg_populasi.add_to(m)

# 5. Titik Taman Bermain Layak Anak (Hijau)
fg_taman = folium.FeatureGroup(name="🟢 Titik Taman Bermain Layak Anak")
for feat in taman["features"]:
    p = feat["properties"]
    lon, lat = feat["geometry"]["coordinates"]
    popup_html = (f"<b>{p['nama_taman']}</b><br>"
                  f"Ramah Anak: {p['fasilitas_ramah_anak']}<br>"
                  f"Kapasitas Maks: {p['kapasitas_maks_anak']} anak")
    tooltip_html = (f"<b>Taman:</b> {p['nama_taman']}<br>"
                    f"<b>Fasilitas:</b> {p['fasilitas_ramah_anak']}<br>"
                    f"<b>Kapasitas:</b> {p['kapasitas_maks_anak']} Anak")
    folium.CircleMarker(
        location=[lat, lon], radius=7, color="darkgreen",
        fill=True, fill_color="green", fill_opacity=0.9,
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=folium.Tooltip(tooltip_html)
    ).add_to(fg_taman)
fg_taman.add_to(m)

# Layer control (checkbox on/off)
folium.LayerControl(collapsed=False).add_to(m)

# Legenda kustom (HTML overlay)
legend_html = """
<div style="
    position: fixed;
    bottom: 30px;
    left: 30px;
    z-index: 9999;
    background-color: white;
    color: black;
    padding: 10px 14px;
    border-radius: 6px;
    border: 2px solid black;
    font-size: 13px;
    line-height: 1.6;
    font-family: Arial, sans-serif;
">
<b style="color:black;">Legenda</b><br>
<span style="color:green;">&#9679;</span> Taman Bermain Layak Anak<br>
<span style="color:green;">&#9632;</span> Buffer 500m (Zona Aman)<br>
<span style="color:orange;">&#9632;</span> Zona Paparan Polusi<br>
<span style="color:red;">&#9632;</span> Blank Spot Taman Bermain<br>
<span style="
    background:linear-gradient(to right,#ffff66,#cc0000);
    display:inline-block;
    width:40px;
    height:10px;
    border:1px solid black;
"></span>
Kerentanan Anak (Rendah&rarr;Tinggi)
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Render peta di Streamlit
st_folium(m, width=1200, height=650)

st.caption(
    "Sumber data: SINTETIS/dummy untuk keperluan UAS Sistem Informasi Geografis, "
    "Universitas Mercu Buana. Bukan data resmi Dinas Kesehatan/DP3AKB Provinsi Banten."
)
