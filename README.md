# **ATHERZ \- Platform E-commerce Modern**

**ATHERZ** adalah aplikasi web e-commerce *full-stack* yang dibangun menggunakan Python dan Flask. Proyek ini menyediakan pengalaman berbelanja yang lengkap bagi pengguna, mulai dari melihat katalog hingga proses checkout, serta dasbor admin yang komprehensif untuk manajemen toko.

## **📸 Tampilan Aplikasi**

Berikut adalah beberapa contoh tampilan dari aplikasi ATHERZ:

Halaman Utama

Dasbor Admin

## **✨ Fitur Utama**

### **Untuk Pengguna (Pembeli)**

* **Otentikasi Pengguna**: Registrasi dan Login yang aman.  
* **Katalog Produk**: Menampilkan semua produk dengan fitur filter berdasarkan kategori dan urutkan berdasarkan harga, popularitas, atau produk terbaru.  
* **Pencarian Cepat**: Fitur *live search* untuk menemukan produk secara instan.  
* **Halaman Detail Produk**: Tampilan detail produk, ulasan dari pembeli, dan galeri gambar.  
* **Wishlist**: Pengguna dapat menyimpan produk yang mereka sukai.  
* **Keranjang Belanja**: Menambah, mengubah jumlah, dan menghapus produk dari keranjang menggunakan AJAX tanpa *reload* halaman.  
* **Proses Checkout**: Alur checkout yang mudah dengan pengisian alamat pengiriman.  
* **Profil Pengguna**: Melihat riwayat pesanan, mengubah detail profil, dan mengganti password.  
* **Tema Terang & Gelap**: Tampilan situs dapat diubah antara mode terang dan gelap, dengan preferensi yang tersimpan di perangkat pengguna.

### **Untuk Administrator**

* **Dasbor Analitik**: Menampilkan ringkasan total penjualan, jumlah pesanan, produk, dan pelanggan dengan visualisasi grafik.  
* **Manajemen Produk (CRUD)**: Admin dapat menambah, melihat, mengubah, dan menghapus produk.  
* **Manajemen Pesanan**: Melihat semua pesanan yang masuk dan mengubah statusnya (misal: dari 'Pending' menjadi 'Shipped').  
* **Manajemen Pelanggan**: Melihat daftar pelanggan dan detail riwayat pesanan mereka.  
* **Laporan Penjualan**: Grafik visual untuk penjualan berdasarkan kategori dan daftar produk terlaris.

## **🛠️ Teknologi yang Digunakan**

* **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Flask-Bcrypt  
* **Database**: SQLite (dapat dengan mudah dikonfigurasi untuk PostgreSQL atau MySQL)  
* **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5  
* **Deployment**: Gunicorn

## **🚀 Instalasi dan Menjalankan Proyek**

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di lingkungan lokal Anda.

1. **Clone Repositori**  
   git clone https://github.com/username/atherz-project.git  
   cd atherz-project

2. **Buat dan Aktifkan Lingkungan Virtual (Virtual Environment)**  
   \# Untuk Windows  
   python \-m venv venv  
   venv\\Scripts\\activate

   \# Untuk MacOS/Linux  
   python3 \-m venv venv  
   source venv/bin/activate

3. Install Semua Kebutuhan (Dependencies)  
   Pastikan Anda berada di direktori utama proyek, lalu jalankan:  
   pip install \-r requirements.txt

4. Buat File .env  
   Aplikasi ini menggunakan file .env untuk menyimpan kunci rahasia. Buat file baru bernama .env di direktori utama dan isi dengan:  
   SECRET\_KEY='kunci-rahasia-anda-yang-sangat-sulit-ditebak'

5. **Jalankan Aplikasi**  
   python app.py

   Saat pertama kali dijalankan, aplikasi akan secara otomatis membuat database atherz.db dan mengisinya dengan data awal (produk dan akun admin).  
6. **Akses Aplikasi**  
   * Buka browser dan kunjungi http://127.0.0.1:5000  
   * Untuk masuk ke dasbor admin, gunakan kredensial berikut:  
     * **Email**: admin@atherz.com  
     * **Password**: admin123

## **📁 Struktur Folder**

/  
├── static/  
│   ├── css/  
│   │   └── style.css  
│   └── js/  
│       └── main.js  
├── templates/  
│   ├── admin/  
│   ├── components/  
│   ├── errors/  
│   └── (file-file html lainnya)  
├── app.py          \# Logika utama aplikasi Flask  
├── models.py       \# Definisi model database (SQLAlchemy)  
├── forms.py        \# Definisi form (WTForms)  
├── config.py       \# Konfigurasi aplikasi  
└── requirements.txt \# Daftar dependencies

## **📄 Lisensi**

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file LICENSE untuk detailnya.