# Belajar Python Part 18: Autentikasi dengan Flask-Login

Kode pendamping artikel **Belajar Python Part 18**. Aplikasi Flask minimal dengan
register, login, logout, dan proteksi halaman memakai Flask-Login.

## Fitur

- Register dengan validasi (username/email unik, password minimal 8 karakter)
- Password disimpan sebagai hash (Werkzeug)
- Login, "ingat saya", dan logout (POST + CSRF)
- Proteksi halaman dengan `@login_required`
- Redirect `next` yang aman dari open redirect
- Unit test dengan pytest

## Struktur

```text
.
├── run.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── myapp/
│   ├── __init__.py      # application factory
│   ├── extensions.py    # db, login_manager, csrf
│   ├── models.py        # model User + user_loader
│   ├── forms.py         # RegisterForm, LoginForm
│   ├── auth.py          # /register, /login, /logout
│   ├── main.py          # /, /dashboard (terproteksi)
│   └── templates/
└── tests/test_auth.py
```

## Menjalankan

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# opsional tapi disarankan
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"

python run.py
```

Buka http://127.0.0.1:5000

## Menjalankan test

```bash
pip install -r requirements-dev.txt
pytest -v
```

## Catatan keamanan

- Ganti `SECRET_KEY` di produksi dan jangan commit file `.env`.
- Gunakan HTTPS dan set `SESSION_COOKIE_SECURE = True` di produksi.
- Pertimbangkan Flask-Limiter untuk membatasi percobaan login.

## Lisensi

MIT
