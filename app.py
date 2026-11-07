import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="Aplikasi Lengkap", page_icon="🎮", layout="centered")

# =========================================================
# NAVIGATION BAR / PILIHAN MENU
# =========================================================
st.sidebar.title("📌 Navigation Menu")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Tampilan Gambar & Mini Game", "Kritik & Pesan"]
)

# =========================================================
# HALAMAN 1: TAMPILAN GAMBAR & MINI GAME
# =========================================================
if menu == "Tampilan Gambar & Mini Game":
    st.title("🖼️ Tampilan Gambar Utama")
    
    # Menampilkan Gambar Utama
    st.image("https://picsum.photos/800/400", use_container_width=True, caption="Gambar Utama")
    
    st.write("---")
    
    # Mini Game Tebak Angka
    st.subheader("🎮 Mini Game: Tebak Angka (1 - 100)")
    st.write("Coba tebak angka rahasia sebelum mengisi formulir!")

    if "target_number" not in st.session_state:
        st.session_state.target_number = random.randint(1, 100)
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    if "game_over" not in st.session_state:
        st.session_state.game_over = False

    col1, col2 = st.columns([3, 1])
    with col1:
        tebakan = st.number_input("Masukkan tebakanmu:", min_value=1, max_value=100, value=50, step=1, disabled=st.session_state.game_over)
    with col2:
        st.write("")
        st.write("")
        tebak_btn = st.button("Tebak! 🎯", disabled=st.session_state.game_over)
        
    if tebak_btn and not st.session_state.game_over:
        st.session_state.attempts += 1
        if tebakan < st.session_state.target_number:
            st.warning(f"💡 Angka tebakanmu ({tebakan}) terlalu *KECIL*!")
        elif tebakan > st.session_state.target_number:
            st.warning(f"💡 Angka tebakanmu ({tebakan}) terlalu *BESAR*!")
        else:
            st.balloons()
            st.success(f"🎉 *SELAMAT!* Angka rahasianya adalah *{st.session_state.target_number}* (Total percobaan: {st.session_state.attempts})")
            st.session_state.game_over = True
            
    if st.button("🔄 Main Lagi"):
        st.session_state.target_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.rerun()

# =========================================================
# HALAMAN 2: GAMBAR ATAS + FORMULIR (NAMA, NO HP, PESAN)
# =========================================================
elif menu == "Kritik & Pesan":
    st.title("📝 Halaman Kritik & Pesan")
    
    # 1. Gambar Bagian Atas Sesuai Sketsa
    st.image("https://picsum.photos/800/250", use_container_width=True, caption="Banner Formulir")
    
    st.write("---")
    
    # 2. Formulir Kritik & Pesan (Nama, No HP, Pesan)
    st.subheader("📬 Form Masukan Pengguna")
    
    # Inisialisasi koneksi Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)

    with st.form("form_kritik_pesan"):
        nama = st.text_input("Nama")
        no_hp = st.text_input("No HP / WhatsApp")
        pesan = st.text_area("Pesan / Kritik & Saran")
        
        submitted = st.form_submit_button("Kirim Pesan 🚀")
        
        if submitted:
            if not nama.strip():
                st.error("Nama wajib diisi!")
            elif not no_hp.strip():
                st.error("No HP wajib diisi!")
            elif not pesan.strip():
                st.error("Pesan tidak boleh kosong!")
            else:
                waktu_kirim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Baca data lama dari Google Sheets
                try:
                    existing_data = conn.read(worksheet="Sheet1", ttl=0)
                except Exception:
                    existing_data = pd.DataFrame()

                # Buat baris data baru (Waktu, Nama, No HP, Pesan)
                data_baru = pd.DataFrame([{
                    "Waktu": waktu_kirim,
                    "Nama": nama,
                    "No HP": no_hp,
                    "Pesan": pesan
                }])
                
                # Simpan ke Google Sheets
                updated_df = pd.concat([existing_data, data_baru], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_df)
                
                st.success("✅ Terima kasih! Data Anda berhasil masuk ke Google Sheets.")