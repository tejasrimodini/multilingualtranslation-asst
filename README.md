# 🌐 Multilingual Translation Bot - Django Application

A powerful multilingual translation web app built with Django that supports **100+ languages**.

---

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Start the Server
```bash
python manage.py runserver
```

Then open: **http://127.0.0.1:8000**

---

## ✨ Features

### ⚡ Single Translation Tab
- Translate text between **100+ languages**
- **Auto-detect** source language
- **Swap** source ↔ target languages
- **Copy** translation to clipboard
- **Text-to-speech** for translated output
- Character counter (up to 5000 chars)
- Keyboard shortcut: **Ctrl+Enter** to translate

### 🌍 Batch Translation Tab
- Translate text into **up to 10 languages simultaneously**
- Quick-select **popular languages** (Spanish, French, German, Japanese, etc.)
- View all translations side by side
- Copy any result with one click

### 📜 History Tab
- Automatically saves all translations
- View source text, translated text, language pair, and timestamp
- **Clear all history** with one click

### 📊 Live Stats (Header)
- Total translations count
- Total characters translated
- Number of languages used

---

## 🗂 Project Structure

```
translation_bot/
├── manage.py
├── requirements.txt
├── README.md
├── translation_bot/         # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── translator/              # Main app
│   ├── models.py            # TranslationHistory model
│   ├── views.py             # API endpoints + page views
│   ├── urls.py              # URL routing
│   └── admin.py             # Django admin config
└── templates/
    └── translator/
        └── index.html       # Full-featured UI
```

---

## 🌐 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Main UI |
| POST | `/translate/` | Single translation |
| POST | `/batch-translate/` | Multi-language translation |
| GET | `/history/` | Get translation history |
| DELETE | `/clear-history/` | Clear all history |

### POST `/translate/` — Example
```json
{
  "text": "Hello, world!",
  "target_language": "fr",
  "source_language": "auto"
}
```

### POST `/batch-translate/` — Example
```json
{
  "text": "Hello, world!",
  "target_languages": ["fr", "de", "ja", "es", "ar"],
  "source_language": "auto"
}
```

---

## 🛠 Tech Stack
- **Backend**: Django 4.2+, SQLite
- **Translation Engine**: Google Translate (unofficial API — no API key required)
- **Frontend**: Vanilla JS, modern CSS (dark theme, animations)
- **Admin**: Django built-in admin at `/admin/`

---

## ⚙️ Optional: Create Superuser for Admin
```bash
python manage.py createsuperuser
```
Then visit: http://127.0.0.1:8000/admin
