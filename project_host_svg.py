import streamlit as st
import os
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title="Menu",
    options=["Visualisasi Data Pending (Cashless)", "Patient Pending (Cashless)"],
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
        "Grafik Pie Chart Provider Pending":"grafik claim monitoring (2).svg"}
    
    
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
    if pilihan_baru == "Grafik Line Chart Aging":
        st.subheader("Aging Claim on Payor")
    else:
        st.subheader("Percentage Pending on Provider")
    
    pilihan_asli = svg_files[pilihan_baru]
    # Render SVG yang dipilih
    render_svg(pilihan_asli)
if selected == "Patient Pending (Cashless)":
    df = pd.read_excel("patient_pending.xlsx")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filter= True, floatingFilter= True, resizable = True)
    gridOptions = gb.build()
    AgGrid(df,gridOptions = gridOptions, fit_columns_on_grid_load = True)
