import os
from dotenv import load_dotenv

# Muat variabel environment dari file .env
load_dotenv()

# Dapatkan path dasar dari direktori proyek
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Kelas konfigurasi dasar untuk aplikasi Flask.
    Variabel konfigurasi dimuat dari environment variables.
    """
    # Kunci rahasia untuk keamanan sesi dan CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secret-key'

    # Konfigurasi database SQLAlchemy
    # Menggunakan SQLite sebagai default
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'atherz.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Konfigurasi email (jika diperlukan di masa depan)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@atherz.com']
