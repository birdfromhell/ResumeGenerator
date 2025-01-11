import streamlit as st
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import io

def export_history_to_pdf(history):
    """Fungsi untuk export history ke PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Persiapkan data tabel
    table_data = [['No', 'Input', 'Rata-rata']]
    for i, entry in enumerate(history, 1):
        table_data.append([
            str(i), 
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
    
    # Buat PDF
    elements = [table]
    doc.build(elements)
    
    buffer.seek(0)
    return buffer

def main():
    # Konfigurasi halaman
    st.set_page_config(
        page_title="Kalkulator Rata-Rata",
        page_icon="📊",
        layout="centered"
    )

    # Judul dan deskripsi
    st.title("🧮 Kalkulator Rata-Rata Profesional")
    st.markdown("""
    ### Fitur Utama:
    - Hitung rata-rata dengan mudah
    - Simpan history perhitungan
    - Export history ke PDF
    """)

    # Sidebar untuk konfigurasi
    st.sidebar.header("Pengaturan")
    app_title = st.sidebar.text_input(
        "Judul Aplikasi", 
        value="Kalkulator Rata-Rata",
        help="Ubah judul sesuai kebutuhan"
    )

    # Mode tampilan
    view_mode = st.sidebar.radio(
        "Mode Tampilan",
        ["Default", "Kompak", "Detail"]
    )

    # Inisialisasi session state untuk history
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Input angka
    input_numbers = st.text_input(
        f"{app_title} - Masukkan Angka",
        help="Ketik angka-angka yang dipisah spasi"
    )

    # Kolom untuk tombol
    col1, col2 = st.columns(2)

    # Tombol hitung
    with col1:
        if st.button("Hitung Rata-Rata", type="primary"):
            try:
                # Konversi input ke list float
                numbers = [float(x.strip()) for x in input_numbers.split()]
                
                # Validasi input
                if not numbers:
                    st.error("Mohon masukkan setidaknya satu angka")
                    return
                
                # Hitung rata-rata
                result = np.mean(numbers)
                
                # Tampilkan hasil
                st.success(f"Rata-rata: {result:.2f}")
                
                # Tambahkan ke history
                history_entry = {
                    'input': ' '.join(map(str, numbers)),
                    'result': result
                }
                st.session_state.history.insert(0, history_entry)
                
                # Batasi history maksimal 10 entri
                st.session_state.history = st.session_state.history[:10]
            
            except ValueError:
                st.error("Input tidak valid. Mohon masukkan angka yang benar.")

    # Tombol export PDF
    with col2:
        if st.session_state.history:
            pdf_export = st.download_button(
                label="Export History PDF",
                data=export_history_to_pdf(st.session_state.history),
                file_name="history_rata_rata.pdf",
                mime="application/pdf",
                type="secondary"
            )

    # Bagian History dengan mode tampilan
    st.header("History Perhitungan")
    
    # Tampilkan history sesuai mode
    if st.session_state.history:
        if view_mode == "Default":
            for i, entry in enumerate(st.session_state.history, 1):
                st.markdown(f"**Perhitungan {i}:** Input `{entry['input']}` → Rata-rata: `{entry['result']:.2f}`")
        
        elif view_mode == "Kompak":
            data = {
                'No': list(range(1, len(st.session_state.history) + 1)),
                'Input': [entry['input'] for entry in st.session_state.history],
                'Rata-rata': [f"{entry['result']:.2f}" for entry in st.session_state.history]
            }
            st.dataframe(data, hide_index=True)
        
        else:  # Detail
            for i, entry in enumerate(st.session_state.history, 1):
                with st.expander(f"Perhitungan {i}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Input", entry['input'])
                    with col2:
                        st.metric("Rata-rata", f"{entry['result']:.2f}")
    else:
        st.info("Belum ada history perhitungan")

    # Tombol hapus history
    if st.button("Hapus Semua History", type="destructive"):
        st.session_state.history = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()
