"""
render_preview.py
Merender peta Folium (logika sama seperti app.py) menjadi file HTML
standalone -- BUKA file ini di browser untuk mengambil screenshot
tampilan penuh + pop-up, sesuai permintaan deliverable soal UAS.
"""

import json
import folium

DATA_DIR = "data"

def load_geojson(name):
    with open(f"{DATA_DIR}/{name}") as f:
        return json.load(f)

taman = load_geojson("taman_bermain.geojson")
buffer_taman = load_geojson("buffer_taman.geojson")
zona_polusi = load_geojson("zona_polusi.geojson")
blank_spot = load_geojson("blank_spot.geojson")
populasi = load_geojson("populasi_rentan.geojson")

m = folium.Map(location=[-6.17, 106.65], zoom_start=12, tiles="CartoDB positron")

fg_polusi = folium.FeatureGroup(name="Zona Paparan Polusi Industri/Jalan Utama")
for feat in zona_polusi["features"]:
    p = feat["properties"]
    folium.GeoJson(
        feat,
        style_function=lambda x: {"fillColor": "orange", "color": "orange",
                                   "fillOpacity": 0.35, "weight": 1},
        tooltip=f"Sumber: {p['sumber_paparan']} (radius {p['radius_meter']}m)"
    ).add_to(fg_polusi)
fg_polusi.add_to(m)

fg_buffer = folium.FeatureGroup(name="Buffer 500m Taman Bermain")
for feat in buffer_taman["features"]:
    folium.GeoJson(
        feat,
        style_function=lambda x: {"fillColor": "green", "color": "green",
                                   "fillOpacity": 0.15, "weight": 1},
        tooltip=feat["properties"]["nama_taman"]
    ).add_to(fg_buffer)
fg_buffer.add_to(m)

fg_blank = folium.FeatureGroup(name="Blank Spot Taman Bermain")
for feat in blank_spot["features"]:
    p = feat["properties"]
    popup_html = (f"<b>{p['nama_desa']}</b><br>"
                  f"Jumlah Balita: {p['jumlah_balita']}<br>"
                  f"Kasus ISPA/Stunting: {p['jumlah_kasus_ispa_stunting']}<br>"
                  f"Status: {p['status_wilayah']}")
    folium.GeoJson(
        feat,
        style_function=lambda x: {"fillColor": "red", "color": "darkred",
                                   "fillOpacity": 0.5, "weight": 1},
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=p["nama_desa"]
    ).add_to(fg_blank)
fg_blank.add_to(m)

def warna_gradasi(jumlah_kasus):
    if jumlah_kasus < 30:
        return "#ffff66"
    elif jumlah_kasus < 60:
        return "#ffcc00"
    elif jumlah_kasus < 90:
        return "#ff6600"
    else:
        return "#cc0000"

fg_populasi = folium.FeatureGroup(name="Populasi Anak Rentan Kesehatan (Gradasi)")
for feat in populasi["features"]:
    p = feat["properties"]
    popup_html = (f"<b>{p['nama_desa']}</b><br>"
                  f"Jumlah Balita: {p['jumlah_balita']}<br>"
                  f"Kasus ISPA/Stunting: {p['jumlah_kasus_ispa_stunting']}<br>"
                  f"Status: {p['status_wilayah']}")
    warna = warna_gradasi(p["jumlah_kasus_ispa_stunting"])
    folium.GeoJson(
        feat,
        style_function=lambda x, warna=warna: {"fillColor": warna, "color": "grey",
                                                "fillOpacity": 0.6, "weight": 1},
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=p["nama_desa"]
    ).add_to(fg_populasi)
fg_populasi.add_to(m)

fg_taman = folium.FeatureGroup(name="Titik Taman Bermain Layak Anak")
for feat in taman["features"]:
    p = feat["properties"]
    lon, lat = feat["geometry"]["coordinates"]
    popup_html = (f"<b>{p['nama_taman']}</b><br>"
                  f"Ramah Anak: {p['fasilitas_ramah_anak']}<br>"
                  f"Kapasitas Maks: {p['kapasitas_maks_anak']} anak")
    folium.CircleMarker(
        location=[lat, lon], radius=7, color="darkgreen",
        fill=True, fill_color="green", fill_opacity=0.9,
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=p["nama_taman"]
    ).add_to(fg_taman)
fg_taman.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

legend_html = """
<div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
     background-color: white; padding: 10px 14px; border-radius: 6px;
     border: 2px solid grey; font-size: 13px; line-height: 1.6;">
<b>Legenda</b><br>
<span style="color:green;">&#9679;</span> Taman Bermain Layak Anak<br>
<span style="color:green;">&#9632;</span> Buffer 500m (Zona Aman)<br>
<span style="color:orange;">&#9632;</span> Zona Paparan Polusi<br>
<span style="color:red;">&#9632;</span> Blank Spot Taman Bermain<br>
<span style="background:linear-gradient(to right,#ffff66,#cc0000);
      display:inline-block; width:40px; height:10px;"></span> Kerentanan Anak (Rendah&rarr;Tinggi)
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

title_html = """
<div style="position: fixed; top: 15px; left: 60px; z-index: 9999;
     background-color: white; padding: 8px 16px; border-radius: 6px;
     border: 2px solid grey; font-size: 16px; font-weight: bold;">
Peta Aksesibilitas Taman Bermain & Kerentanan Kesehatan Anak Banten
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))

m.save("map_preview.html")
print("Peta preview tersimpan: map_preview.html")
