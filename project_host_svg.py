import streamlit as st
import os

svg_files = {"Grafik Line Chart Aging":"grafik claim monitoring (1).svg",
    "Grafik Bar Chart Provider Pending":"grafik claim monitoring (2).svg"}


def render_svg(file_path):
    # Mengecek apakah file ada
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        st.markdown(svg_content, unsafe_allow_html=True)
    else:
        st.error(f"File tidak ditemukan: {file_path}")

st.title("Grafik Claim Monitoring")

# Membuat dropdown menu
pilihan_baru = st.selectbox("Pilih Visualisasi:", list(svg_files.keys()))
pilihan_asli = svg_files[pilihan_baru]
# Render SVG yang dipilih
render_svg(pilihan_asli)
