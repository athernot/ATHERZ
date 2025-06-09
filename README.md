ATHERZ - Platform E-commerce Modern
ATHERZ adalah aplikasi web e-commerce full-stack yang dibangun menggunakan Python dan Flask. Proyek ini menyediakan pengalaman berbelanja yang lengkap bagi pengguna, mulai dari melihat katalog hingga proses checkout, serta dasbor admin yang komprehensif untuk manajemen toko.

📸 Tampilan Aplikasi
(Di sini adalah tempat yang bagus untuk menambahkan beberapa screenshot dari aplikasi Anda, seperti halaman utama, halaman produk, dan dasbor admin)

Halaman Utama

Dasbor Admin

✨ Fitur Utama
Untuk Pengguna (Pembeli)
Otentikasi Pengguna: Registrasi dan Login yang aman.
Katalog Produk: Menampilkan semua produk dengan fitur filter berdasarkan kategori dan urutkan berdasarkan harga, popularitas, atau produk terbaru.
Pencarian Cepat: Fitur live search untuk menemukan produk secara instan.
Halaman Detail Produk: Tampilan detail produk, ulasan dari pembeli, dan galeri gambar.
Wishlist: Pengguna dapat menyimpan produk yang mereka sukai.
Keranjang Belanja: Menambah, mengubah jumlah, dan menghapus produk dari keranjang menggunakan AJAX tanpa reload halaman.
Proses Checkout: Alur checkout yang mudah dengan pengisian alamat pengiriman.
Profil Pengguna: Melihat riwayat pesanan, mengubah detail profil, dan mengganti password.
Tema Terang & Gelap: Tampilan situs dapat diubah antara mode terang dan gelap.
Untuk Administrator
Dasbor Analitik: Menampilkan ringkasan total penjualan, jumlah pesanan, produk, dan pelanggan.
Manajemen Produk (CRUD): Admin dapat menambah, melihat, mengubah, dan menghapus produk.
Manajemen Pesanan: Melihat semua pesanan yang masuk dan mengubah statusnya (misal: dari 'Pending' menjadi 'Shipped').
Manajemen Pelanggan: Melihat daftar pelanggan dan detail riwayat pesanan mereka.
Laporan Penjualan: Grafik visual untuk penjualan berdasarkan kategori dan daftar produk terlaris.
🛠️ Teknologi yang Digunakan
Backend: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate
Database: SQLite (dapat dengan mudah diganti ke PostgreSQL atau MySQL)
Frontend: HTML5, CSS3, JavaScript, Bootstrap 5
Deployment: Gunicorn
🚀 Instalasi dan Menjalankan Proyek
Ikuti langkah-langkah berikut untuk menjalankan proyek ini di lingkungan lokal Anda.

Clone Repositori

Bash

git clone https://github.com/username/atherz-project.git
cd atherz-project
Buat dan Aktifkan Lingkungan Virtual (Virtual Environment)

Bash

# Untuk Windows
python -m venv venv
venv\Scripts\activate

# Untuk MacOS/Linux
python3 -m venv venv
source venv/bin/activate
Install Semua Kebutuhan (Dependencies)
Pastikan Anda berada di direktori utama proyek, lalu jalankan:

Bash

pip install -r requirements.txt
Buat File .env
Aplikasi ini menggunakan file .env untuk menyimpan kunci rahasia. Buat file bernama .env di direktori utama dan isi dengan:

SECRET_KEY='kunci-rahasia-anda-yang-sangat-sulit-ditebak'
Jalankan Aplikasi

Bash

python app.py
Saat pertama kali dijalankan, aplikasi akan secara otomatis membuat database atherz.db dan mengisinya dengan data awal (produk dan akun admin).

Akses Aplikasi

Buka browser dan kunjungi http://127.0.0.1:5000
Untuk masuk ke dasbor admin, gunakan kredensial berikut:
Email: admin@atherz.com
Password: admin123
