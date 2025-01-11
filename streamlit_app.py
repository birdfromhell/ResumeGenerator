import streamlit as st
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io
from datetime import datetime

def export_history_to_pdf(history):
    """Fungsi untuk export history ke PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Elemen PDF
    elements = []

    # Tanggal
    date_style = styles['Normal']
    elements.append(Paragraph(f"Tanggal: {datetime.now().strftime('%d %B %Y')}", date_style))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Persiapkan data tabel
    table_data = [['No', 'Judul', 'Input', 'Rata-rata']]
    for i, entry in enumerate(history, 1):
        table_data.append([
            str(i), 
            entry['title'],
            entry['input'], 
            f"{entry['result']:.2f}"
        ])
    
    # Styling tabel
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    
    # Tambahkan tabel ke elemen
    elements.append(table)
    
    # Buat PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer

def main():
    st.set_page_config(
        page_title="Kalkulator Rata-Rata Fleksibel",
        page_icon="📊",
        layout="centered"
    )

    # Judul utama aplikasi
    st.title("🧮 Kalkulator Rata-Rata Fleksibel")

    # Inisialisasi session state untuk history
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Kolom untuk input
    col1, col2 = st.columns([2, 1])

    # Input judul perhitungan
    with col2:
        calculation_title = st.text_input(
            "Judul Perhitungan", 
            placeholder="Contoh: Nilai Matematika",
            help="Beri judul untuk setiap perhitungan"
        )

    # Input angka
    with col1:
        input_numbers = st.text_input(
            "Masukkan Angka",
            help="Ketik angka-angka yang dipisah spasi"
        )

    # Tombol hitung
    if st.button("Hitung Rata-Rata", type="primary"):
        try:
            # Validasi judul
            if not calculation_title:
                st.error("Mohon masukkan judul perhitungan")
                return

            # Konversi input ke list float
            numbers = [float(x.strip()) for x in input_numbers.split()]
            
            # Validasi input angka
            if not numbers:
                st.error("Mohon masukkan setidaknya satu angka")
                return
            
            # Hitung rata-rata
            result = np.mean(numbers)
            
            # Tampilkan hasil
            st.success(f"Rata-rata untuk {calculation_title}: {result:.2f}")
            
            # Tambahkan ke history
            history_entry = {
                'title': calculation_title,
                'input': ' '.join(map(str, numbers)),
                'result': result
            }
            st.session_state.history.insert(0, history_entry)
            
            # Batasi history maksimal 10 entri
            st.session_state.history = st.session_state.history[:10]
        
        except ValueError:
            st.error("Input tidak valid. Mohon masukkan angka yang benar.")

    # Tombol export PDF
    if st.session_state.history:
        pdf_export = st.download_button(
            label="Export History PDF",
            data=export_history_to_pdf(st.session_state.history),
            file_name="history_rata_rata.pdf",
            mime="application/pdf",
            type="secondary"
        )

    # Bagian History
    st.header("History Perhitungan")
    
    # Tampilkan history
    if st.session_state.history:
        for i, entry in enumerate(st.session_state.history, 1):
            st.markdown(f"""
            **Perhitungan {i}:** 
            - **Judul:** {entry['title']}
            - **Input:** `{entry['input']}`
            - **Rata-rata:** `{entry['result']:.2f}`
            """)
    else:
        st.info("Belum ada history perhitungan")

    # Tombol hapus history (ganti type menjadi "secondary")
    if st.button("Hapus Semua History", type="secondary"):
        st.session_state.history = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()
