import streamlit as st
import numpy as np

def main():
    # Judul aplikasi
    st.title("Kalkulator Rata-Rata dengan History")

    # Inisialisasi session state untuk history
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Input angka
    input_numbers = st.text_input(
        "Masukkan angka dipisah spasi (contoh: 10 20 30)",
        help="Ketik angka-angka yang dipisah spasi"
    )

    # Tombol hitung
    if st.button("Hitung Rata-Rata"):
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
            st.success(f"Rata-rata: {result}")
            
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

    # Bagian History
    st.header("History Perhitungan")
    
    # Tampilkan history
    if st.session_state.history:
        for i, entry in enumerate(st.session_state.history, 1):
            col1, col2 = st.columns(2)
            with col1:
                st.text(f"Input {i}: {entry['input']}")
            with col2:
                st.text(f"Rata-rata: {entry['result']}")
    else:
        st.info("Belum ada history perhitungan")

    # Tombol hapus history
    if st.button("Hapus History"):
        st.session_state.history = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()
