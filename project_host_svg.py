import streamlit as st
import os
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_option_menu import option_menu
import re


st.set_page_config(layout="wide")
selected = option_menu(
    menu_title="Menu",
    options=["Visualisasi Data Pending (Cashless)", "Detail Pending (Cashless)"],
    menu_icon="columns-gap",
        icons=[        
        "gear-fill",          
        "journal-text"       
    ],
    default_index=0,
    orientation="vertical"
)

if selected == "Visualisasi Data Pending (Cashless)":

    svg_files = {"Grafik Line Chart Aging":"grafik claim monitoring (1).svg",
        "Grafik Pie Chart Provider Pending > 3 Claim Pending":"grafik claim monitoring (2).svg",
        "Grafik Pending Aging Tertinggi":"grafik claim monitoring (3).svg",
        "Grafik Top 10 Pending":"grafik claim monitoring (4).svg"}
    
    
    def render_svg(file_path):
        # Mengecek apakah file ada
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                svg_content = f.read()
                svg_content = re.sub(r'(<svg[^>]*?)\s+width="[^"]*"', r"\1", svg_content, count=1)
                svg_content = re.sub(r'(<svg[^>]*?)\s+height="[^"]*"', r"\1", svg_content, count=1)
                svg_content = svg_content.replace("<svg ", '<svg style="width: 100%; height: auto; display: block;" ', 1)
            st.markdown(svg_content, unsafe_allow_html=True)
        else:
            st.error(f"File tidak ditemukan: {file_path}")
    
    st.title("Grafik Claim Monitoring")
    
    # Membuat dropdown menu
    pilihan_baru = st.selectbox("Pilih Visualisasi:", list(svg_files.keys()))
    if pilihan_baru == "Grafik Line Chart Aging":
        st.subheader("Aging Claim on Payor")
    elif pilihan_baru == "Grafik Pie Chart Provider Pending > 3 Claim Pending":
        st.subheader("Percentage Pending on Provider")
    else:
        st.warning("Silahkan cek detail untuk info lebih lanjut")
        
    
    pilihan_asli = svg_files[pilihan_baru]
    # Render SVG yang dipilih
    render_svg(pilihan_asli)
if selected == "Detail Pending (Cashless)":
    import io, os
    import pandas as pd
    from cryptography.fernet import Fernet
    daftar_file_enc = sorted([f for f in os.listdir(".") if f.endswith(".enc")])

    if not daftar_file_enc:
        st.warning("Tidak ada file Pending ditemukan")
    else:
        file_terpilih = st.selectbox("Pilih file Data Pending (.enc)", options=daftar_file_enc)

        @st.cache_date
        def muat_file_enc(nama_file):
            key = st.secrets["KUNCI_EXCEL"][nama_file]
            cipher = Fernet(key)
            with open(nama_file, "rb") as f:
                decrypted_data = cipher.decrypt(f.read())
            return pd.read_excel(io.BytesIO(decrypted_data))
            
        try:
            df = muat_data_enc(file_terpilih)
            st.success(f"Berhasil memuat: **{file_terpilih}** ({len(df)} baris)")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Gagal membuka file {file_terpilih}. Pastikan key sesuai. Detail: {e}")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filter= True, floatingFilter= True, resizable = True)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
    gridOptions = gb.build()
    AgGrid(df,gridOptions = gridOptions, fit_columns_on_grid_load = False, height = 650, use_container_width=True)
