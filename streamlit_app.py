import requests
from fpdf import FPDF
import datetime
import streamlit as st
import zipfile
import os

# Fungsi untuk mendapatkan data acak dari RapidAPI
def generate_random_cv_data():
    url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Buatkan data acak untuk CV dalam format berikut:\nNama: [Nama Lengkap]\nAlamat: [Alamat Lengkap]\nEmail: [Email]\nTelepon: [Nomor Telepon]\nTanggal Lahir: [Tanggal Lahir]\nPendidikan: [Tahun] - [Tahun]: [Gelar] di [Universitas]\nPengalaman Kerja: [Jabatan] di [Perusahaan]\nKeterampilan: [Keterampilan 1], [Keterampilan 2], [Keterampilan 3]\nReferensi: [Nama Referensi] - [Jabatan] di [Perusahaan]"
            }
        ],
        "model": "gpt-4o",
        "max_tokens": 100,
        "temperature": 0.9
    }
    headers = {
        "x-rapidapi-key": st.secrets["rapidapi_key"],
        "x-rapidapi-host": "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Cek jika ada error pada permintaan
        return response.json()['choices'][0]['message']['content']
    
    except Exception as e:
        st.error(f"Gagal mengambil data dari RapidAPI: {str(e)}")
        return None

# Fungsi untuk memparse data CV menjadi dictionary
def parse_cv_data(cv_data):
    lines = cv_data.strip().split('\n')
    cv_dict = {}
    for line in lines:
        if ': ' in line:  # Pastikan ada ': ' dalam baris
            key, value = line.split(': ', 1)
            cv_dict[key] = value
    return cv_dict

# Fungsi untuk membuat CV
def create_cv(pdf, cv_dict):
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, cv_dict['Nama'], ln=True, align='C')
    pdf.set_font("Arial", size=12)
    
    # Tempat untuk foto
    pdf.image("images.png", x=10, y=20, w=30)  # Ganti dengan path foto jika ada
    
    pdf.ln(35)  # Jarak setelah foto

    for key in ['Alamat', 'Email', 'Telepon', 'Tanggal Lahir']:
        pdf.cell(0, 10, f"{key}: {cv_dict[key]}", ln=True, align='L')
    
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Pendidikan", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, cv_dict['Pendidikan'])
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Pengalaman Kerja", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, cv_dict['Pengalaman Kerja'])
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Keterampilan", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, cv_dict['Keterampilan'], ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Referensi", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, cv_dict['Referensi'], ln=True)

# Streamlit UI
st.title("Generator CV Otomatis")
st.write("Klik tombol di bawah untuk menghasilkan 25 CV.")

if st.button("Generate CV"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf_files = []
    
    for i in range(25):
        cv_data = generate_random_cv_data()
        if cv_data is None:
            st.error("Gagal mengenerate data CV. Silakan coba lagi.")
            break
        
        st.write(cv_data)  # Menampilkan data CV untuk debugging
        cv_dict = parse_cv_data(cv_data)
        file_name = f"cv_output_{i+1}.pdf"
        pdf_files.append(file_name)
        create_cv(pdf, cv_dict)
        
        # Simpan PDF
        pdf.output(file_name)

    # Membuat nama file ZIP dengan timestamp
    zip_file_name = f"cv_output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    # Membuat ZIP
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for pdf_file in pdf_files:
            zipf.write(pdf_file)
            os.remove(pdf_file)  # Hapus file PDF setelah dimasukkan ke ZIP
    
    # Menyediakan file ZIP untuk diunduh
    with open(zip_file_name, "rb") as f:
        st.download_button("Download Semua CV", f, zip_file_name, "application/zip")

st.write("Sistem ini menggunakan API RapidAPI untuk menghasilkan data CV.")
