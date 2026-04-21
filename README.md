# Smart Farming API 🌿  

**Tugas Proyek UTS Pemrograman Web Lanjutan B**  
**Nama:** Muh. Hanif Nurmahdin  
**NIM:** H071241033  

## Deskripsi Proyek
Smart Farming API adalah sistem backend berbasis **FastAPI** yang dirancang untuk manajemen zona pertanian dan monitoring data sensor secara modular. Proyek ini mendemonstrasikan implementasi RESTful API, integrasi ORM (SQLAlchemy), dan keamanan JWT.

## Struktur Arsitektur (Modular)
Proyek ini mengikuti pola arsitektur modular untuk mendukung prinsip *separation of concerns*:
- `models/`: Definisi tabel database (User, PlantZone, SensorLog).
- `schemas/`: Validasi data menggunakan Pydantic.
- `routers/`: Logika endpoint yang dipisahkan berdasarkan domain bisnis.
- `database.py`: Konfigurasi koneksi SQLite.

## Fitur Utama
1. **Autentikasi JWT**: Register dan Login untuk mendapatkan token akses.
2. **Manajemen Zona (CRUD)**: Create, Read, Update, dan Delete zona lahan.
3. **Monitoring Sensor**: Pencatatan log suhu dan kelembapan per zona dengan fitur *Cascade Delete*.

## Cara Menjalankan Proyek
1. Clone repositori ini.
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan server:
   ```bash
   uvicorn main:app --reload
   ```

## Dokumentasi API
Dokumentasi interaktif (Swagger UI) tersedia di: `http://localhost:8000/docs`