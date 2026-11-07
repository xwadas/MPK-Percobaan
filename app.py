import os
import solara
import random
import requests
from datetime import datetime, timedelta, timezone

# State Global & Keamanan Environment Variable
WEB_APP_URL = solara.reactive(os.environ.get("WEB_APP_URL", ""))
current_page = solara.reactive("Lobby Utama")
sheet_data = solara.reactive([])

# State Game Code Breaker
cb_secret = solara.reactive("")
cb_attempts = solara.reactive(0)
cb_history = solara.reactive([])
cb_win = solara.reactive(False)
guess_input = solara.reactive("")

# State Form Kritik & Pesan (Anti Double-Submit)
nama_input = solara.reactive("")
no_hp_input = solara.reactive("")
pesan_input = solara.reactive("")
form_submitted_success = solara.reactive(False)
form_error_msg = solara.reactive("")
is_submitting = solara.reactive(False)

def init_game():
    digits = random.sample(range(1, 10), 3)
    cb_secret.value = "".join(map(str, digits))
    cb_attempts.value = 0
    cb_history.value = []
    cb_win.value = False
    guess_input.value = ""

def fetch_sheet_data():
    if not WEB_APP_URL.value:
        return
    try:
        res = requests.get(WEB_APP_URL.value)
        if res.status_code == 200:
            sheet_data.value = res.json()
    except Exception as e:
        print("Gagal mengambil data GSheet:", e)

@solara.component
def Page():
    def auto_load_data():
        if current_page.value == "Lobby Utama":
            fetch_sheet_data()

    solara.use_effect(auto_load_data, [current_page.value])

    solara.Style("""
        @keyframes colorShiftBackground {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes cardSlideIn {
            0% { opacity: 0; transform: translateY(35px) scale(0.97); filter: blur(4px); }
            100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }
        }
        .animated-bg {
            min-height: 100vh;
            background: linear-gradient(-45deg, #000000, #1e3a8a, #ffffff, #d4af37, #0f172a);
            background-size: 400% 400%;
            animation: colorShiftBackground 18s ease infinite;
            padding: 20px 10px;
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }
        .solara-card-custom {
            /* Ganti URL_RAW_GITHUB_LOGO_ANDA dengan link raw gambar logo Anda */
            background: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)), 
                        url('https://github.com/xwadas/MPK-Percobaan/blob/main/WhatsApp_Image_2026-11-07_at_19.14.19-removebg-preview.png?raw=true') !important;
            background-size: cover !important;
            background-position: center !important;
            backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            border-radius: 18px !important;
            padding: 2.2rem !important;
            box-shadow: 0 10px 35px 0 rgba(0, 0, 0, 0.45) !important;
            max-width: 650px !important;
            width: 95% !important;
            margin: 20px auto !important;
            color: #000000 !important;
            animation: cardSlideIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        .solara-card-custom h2, .solara-card-custom p, .solara-card-custom span {
            color: #000000 !important;
            font-weight: 500;
        }
        .info-item-card {
            background: rgba(255, 255, 255, 0.85);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
            border-left: 4px solid #1e3a8a;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        .solara-card-custom button, .btn-full {
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            border-radius: 12px !important;
        }
        .solara-card-custom button:hover, .btn-full:hover {
            transform: translateY(-3px) scale(1.01) !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35) !important;
        }
        .btn-full {
            width: 100% !important;
            margin-top: 8px !important;
            font-weight: 600 !important;
        }
    """)

    with solara.Div(classes=["animated-bg"]):
        if current_page.value == "Lobby Utama":
            with solara.Card(classes=["solara-card-custom"]):
                solara.Markdown("## 🌟 Selamat Datang di MPK SMANKA!")
                solara.Markdown("Jelajahi fitur interaktif aplikasi kami melalui menu di bawah ini:")
                solara.Spacing(2)

                def go_to_game():
                    init_game()
                    current_page.value = "Code Breaker"

                solara.Button("🎮 Mainkan Game Code Breaker", on_click=go_to_game, color="primary", classes=["btn-full"])
                solara.Button("📝 Masuk ke Kritik & Pesan", on_click=lambda: current_page.set("Kritik & Pesan"), color="primary", classes=["btn-full"])

                solara.Spacing(3)
                solara.Markdown("---")
                solara.Markdown("### 📌 Informasi Terkini:")
                solara.Spacing(1)

                if sheet_data.value:
                    for item in sheet_data.value:
                        keys = [k for k in item.keys() if k.lower() != "no"]
                        if keys:
                            title_key = keys[0]
                            title_val = item.get(title_key, "")
                            with solara.Div(classes=["info-item-card"]):
                                solara.Markdown(f"#### 📌 {title_val}")
                                for k in keys[1:]:
                                    val = item.get(k, "")
                                    if str(val).strip():
                                        solara.Markdown(f"*{k}:* {val}")
                else:
                    solara.Info("⏳ Memuat informasi dari server...")

        elif current_page.value == "Code Breaker":
            with solara.Card(classes=["solara-card-custom"]):
                solara.Button("⬅️ Kembali", on_click=lambda: current_page.set("Lobby Utama"), color="dark", outlined=True)
                solara.Spacing(1)
                solara.Markdown("## 🕵️‍♂️ Code Breaker")
                solara.Markdown("Pecahkan 3 digit angka rahasia unik (1-9) menggunakan strategi analisis petunjuk!")
                solara.Spacing(1)

                if not cb_win.value:
                    solara.InputText("Masukkan 3 digit angka unik (Contoh: 123):", value=guess_input)
                    solara.Spacing(1)

                    def handle_guess():
                        val = guess_input.value.strip()
                        if len(val) != 3 or not val.isdigit() or len(set(val)) != 3:
                            return
                        cb_attempts.value += 1
                        secret = cb_secret.value
                        bulls = sum(1 for a, b in zip(val, secret) if a == b)
                        cows = sum(1 for a in val if a in secret) - bulls
                        new_hist = cb_history.value.copy()
                        new_hist.append(f"Tebakan **{val}** ➔ 🎯 Tepat Posisi: **{bulls}** | 🟡 Benar Posisi Salah: **{cows}**")
                        cb_history.value = new_hist
                        if bulls == 3:
                            cb_win.value = True

                    solara.Button("Analisis Tebakan 🔍", on_click=handle_guess, color="success", classes=["btn-full"])

                if cb_history.value:
                    solara.Markdown("### 📋 Riwayat Analisis Logika:")
                    for h in reversed(cb_history.value):
                        solara.Markdown(f"- {h}")

                if cb_win.value:
                    solara.Success(f"🎉 **LUAR BIASA! Kamu Berhasil Memecahkan Kode!** Angka rahasianya adalah **{cb_secret.value}**.")
                    solara.Info(f"Berhasil dipecahkan dalam {cb_attempts.value} kali percobaan analitik.")
                    solara.Spacing(1)
                    solara.Button("🔄 Reset / Kode Baru", on_click=init_game, color="primary", classes=["btn-full"])

        elif current_page.value == "Kritik & Pesan":
            with solara.Card(classes=["solara-card-custom"]):
                solara.Button("⬅️ Kembali", on_click=lambda: current_page.set("Lobby Utama"), color="dark", outlined=True)
                solara.Spacing(1)
                solara.Markdown("## 📝 Halaman Kritik & Pesan")
                solara.Markdown("Silakan isi pesan di bawah ini. Kolom Nama dan No HP bersifat opsional.")
                solara.Spacing(1)

                if form_submitted_success.value:
                    solara.Success("✅ Terima kasih! Data Anda berhasil masuk ke Google Sheets.")
                    solara.Spacing(1)
                    def reset_form():
                        nama_input.value = ""
                        no_hp_input.value = ""
                        pesan_input.value = ""
                        form_submitted_success.value = False
                        is_submitting.value = False
                    solara.Button("🔄 Kirim Pesan Lain", on_click=reset_form, color="primary", classes=["btn-full"])
                    solara.Button("🏠 Kembali ke Lobby", on_click=lambda: current_page.set("Lobby Utama"), color="secondary", classes=["btn-full"])
                else:
                    solara.InputText("Nama Lengkap (Opsional)", value=nama_input)
                    solara.InputText("No HP / WhatsApp (Opsional)", value=no_hp_input)
                    solara.InputTextArea("Pesan / Kritik & Saran (Wajib Diisi)", value=pesan_input)
                    solara.Spacing(1)

                    if form_error_msg.value:
                        solara.Error(form_error_msg.value)

                    def send_kritik_pesan():
                        if is_submitting.value:
                            return
                        if not pesan_input.value.strip():
                            form_error_msg.value = "Pesan wajib diisi!"
                            return
                        is_submitting.value = True
                        form_error_msg.value = ""

                        final_nama = nama_input.value.strip() if nama_input.value.strip() else "Anonim"
                        final_no_hp = no_hp_input.value.strip() if no_hp_input.value.strip() else "-"
                        wib = timezone(timedelta(hours=7))
                        waktu_kirim = datetime.now(wib).strftime("%Y-%m-%d %H:%M:%S")

                        payload = {
                            "tipe": "kritik_pesan",
                            "waktu": waktu_kirim,
                            "nama": final_nama,
                            "no_hp": final_no_hp,
                            "pesan": pesan_input.value.strip()
                        }
                        try:
                            res = requests.post(WEB_APP_URL.value, json=payload)
                            if res.status_code == 200:
                                form_submitted_success.value = True
                            else:
                                form_error_msg.value = "❌ Gagal mengirim data ke server."
                                is_submitting.value = False
                        except Exception as e:
                            form_error_msg.value = f"Terjadi kesalahan koneksi: {e}"
                            is_submitting.value = False

                    btn_label = "⏳ Sedang Mengirim..." if is_submitting.value else "Kirim Pesan 🚀"
                    solara.Button(btn_label, on_click=send_kritik_pesan, color="primary", classes=["btn-full"])
