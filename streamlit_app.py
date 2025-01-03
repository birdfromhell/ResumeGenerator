import openai
from fpdf import FPDF
import datetime
import streamlit as st
import zipfile
import os

# Daftar API keys OpenAI
api_keys = [
    'sk-abcdef1234567890abcdef1234567890abcdef12',
    'sk-1234567890abcdef1234567890abcdef12345678',
    'sk-abcdefabcdefabcdefabcdefabcdefabcdef12',
    'sk-7890abcdef7890abcdef7890abcdef7890abcd',
    'sk-1234abcd1234abcd1234abcd1234abcd1234abcd',
    'sk-abcd1234abcd1234abcd1234abcd1234abcd1234',
    'sk-5678efgh5678efgh5678efgh5678efgh5678efgh',
    'sk-efgh5678efgh5678efgh5678efgh5678efgh5678',
    'sk-ijkl1234ijkl1234ijkl1234ijkl1234ijkl1234',
    'sk-mnop5678mnop5678mnop5678mnop5678mnop5678',
    'sk-qrst1234qrst1234qrst1234qrst1234qrst1234',
    'sk-uvwx5678uvwx5678uvwx5678uvwx5678uvwx5678',
    'sk-1234ijkl1234ijkl1234ijkl1234ijkl1234ijkl',
    'sk-5678mnop5678mnop5678mnop5678mnop5678mnop',
    'sk-qrst5678qrst5678qrst5678qrst5678qrst5678',
    'sk-uvwx1234uvwx1234uvwx1234uvwx1234uvwx1234',
    'sk-1234abcd5678efgh1234abcd5678efgh1234abcd',
    'sk-5678ijkl1234mnop5678ijkl1234mnop5678ijkl',
    'sk-abcdqrstefghuvwxabcdqrstefghuvwxabcdqrst',
    'sk-ijklmnop1234qrstijklmnop1234qrstijklmnop',
    'sk-1234uvwx5678abcd1234uvwx5678abcd1234uvwx',
    'sk-efghijkl5678mnopabcd1234efghijkl5678mnop',
    'sk-mnopqrstuvwxabcdmnopqrstuvwxabcdmnopqrst',
    'sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop',
    'sk-abcd1234efgh5678abcd1234efgh5678abcd1234',
    'sk-1234ijklmnop5678ijklmnop1234ijklmnop5678',
    'sk-qrstefghuvwxabcdqrstefghuvwxabcdqrstefgh',
    'sk-uvwxijklmnop1234uvwxijklmnop1234uvwxijkl',
    'sk-abcd5678efgh1234abcd5678efgh1234abcd5678',
    'sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop',
    'sk-1234qrstuvwxabcd1234qrstuvwxabcd1234qrst',
    'sk-efghijklmnop5678efghijklmnop5678efghijkl',
    'sk-mnopabcd1234efghmnopabcd1234efghmnopabcd',
    'sk-ijklqrst5678uvwxijklqrst5678uvwxijklqrst',
    'sk-1234ijkl5678mnop1234ijkl5678mnop1234ijkl',
    'sk-abcdqrstefgh5678abcdqrstefgh5678abcdqrst',
    'sk-ijklmnopuvwx1234ijklmnopuvwx1234ijklmnop',
    'sk-efgh5678abcd1234efgh5678abcd1234efgh5678',
    'sk-mnopqrstijkl5678mnopqrstijkl5678mnopqrst',
    'sk-1234uvwxabcd5678uvwxabcd1234uvwxabcd5678',
    'sk-ijklmnop5678efghijklmnop5678efghijklmnop',
    'sk-abcd1234qrstuvwxabcd1234qrstuvwxabcd1234',
    'sk-1234efgh5678ijkl1234efgh5678ijkl1234efgh',
    'sk-5678mnopqrstuvwx5678mnopqrstuvwx5678mnop',
    'sk-abcdijkl1234uvwxabcdijkl1234uvwxabcdijkl',
    'sk-ijklmnopabcd5678ijklmnopabcd5678ijklmnop',
    'sk-1234efghqrstuvwx1234efghqrstuvwx1234efgh',
    'sk-5678ijklmnopabcd5678ijklmnopabcd5678ijkl',
    'sk-abcd1234efgh5678abcd1234efgh5678abcd1234',
    'sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop'
]

# Fungsi untuk mendapatkan data acak dari OpenAI
def generate_random_cv_data():
    for key in api_keys:
        try:
            openai.api_key = key
            prompt = (
                "Buatkan data acak untuk CV dalam format berikut:\n"
                "Nama: [Nama Lengkap]\n"
                "Alamat: [Alamat Lengkap]\n"
                "Email: [Email]\n"
                "Telepon: [Nomor Telepon]\n"
                "Tanggal Lahir: [Tanggal Lahir]\n"
                "Pendidikan: [Tahun] - [Tahun]: [Gelar] di [Universitas]\n"
                "Pengalaman Kerja: [Jabatan] di [Perusahaan]\n"
                "Keterampilan: [Keterampilan 1], [Keterampilan 2], [Keterampilan 3]\n"
                "Referensi: [Nama Referensi] - [Jabatan] di [Perusahaan]"
            )
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            
            return response['choices'][0]['message']['content']
        
        except Exception as e:
            st.warning(f"API key {key} gagal: {str(e)}")
            continue  # Coba dengan API key berikutnya
    
    st.error("Semua API key gagal. Silakan coba lagi nanti.")
    return None

# Fungsi untuk memparse data CV menjadi dictionary
def parse_cv_data(cv_data):
    lines = cv_data.strip().split('\n')
    cv_dict = {}
    for line in lines:
        key, value = line.split(': ', 1)
        cv_dict[key] = value
    return cv_dict

# Fungsi untuk membuat CV
def create_cv(pdf, cv_dict):
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, cv_dict['Nama'], ln=True, align='C')
    pdf.set_font("Arial", size=12)
    
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
    
    for i in range(2):
        cv_data = generate_random_cv_data()
        if cv_data is None:
            st.error("Gagal mengenerate data CV. Silakan coba lagi.")
            break
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

st.write("Sistem ini menggunakan API OpenAI untuk menghasilkan data CV.")
