# Valorant Match Predictor

Aplikasi yang mengambil riwayat match Valorant lewat HenrikDev API (unofficial),
lalu memprediksi kemungkinan menang berdasarkan statistik permainan.

## Fitur
- Cari statistik match berdasarkan Riot ID
- Model machine learning (Random Forest) untuk prediksi win/loss
- Demo interaktif dengan Streamlit

## Tech Stack
Python, pandas, scikit-learn, Streamlit, HenrikDev API

## Cara Menjalankan
1. `pip install -r requirements.txt`
2. Buat file `.env` berisi `HENRIK_API_KEY=your_key_here`
3. `python src/fetch_data.py` (ganti nama & tag di file)
4. `python src/train_model.py`
5. `streamlit run app.py`

## Limitasi
- Dataset terbatas pada riwayat match yang dapat diakses publik
- Akurasi model sangat dipengaruhi oleh ukuran sampel data (dataset awal proyek ini kecil)
- Hanya mencakup match mode tim (Competitive/Unrated), match Deathmatch di-skip

## Disclaimer
Project ini menggunakan API pihak ketiga tidak resmi (HenrikDev) untuk Valorant,
bukan produk resmi Riot Games.