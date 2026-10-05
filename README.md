# 🧠 StudyFocus

**StudyFocus** is a productivity-focused Chrome extension with a backend application that helps users reduce distractions by blocking selected websites during focused study sessions.

The project combines a Chrome Extension with a Django REST backend to manage users, blocked websites, and focus-session history.

---

## ✨ Features

- 🚫 Block distracting websites during Study Mode
- 🎯 Start and manage focused study sessions
- 👤 User registration and authentication
- 🔐 JWT-based authentication
- 🌐 User-specific blocked websites
- 📊 Track focus session history
- ⚙️ Manage blocked websites through the backend
- 🔄 REST API integration between the extension and backend

---

## 🏗️ Architecture

```text
                    StudyFocus
                        │
            ┌───────────┴───────────┐
            │                       │
      Chrome Extension         Django Backend
            │                       │
            │                 REST APIs + JWT
            │                       │
            └───────────┬───────────┘
                        │
                    PostgreSQL
                    / SQLite
```

### Workflow

```text
User
  ↓
Chrome Extension
  ↓
Study Mode ON
  ↓
Blocked Website Detected
  ↓
Redirect to Blocked Page

        ↕

Django REST API
  ↓
Authentication
  ↓
Blocked Websites
  ↓
Focus Sessions
  ↓
Database
```

---

## 🛠️ Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- JWT Authentication

### Database
- PostgreSQL / SQLite

### Frontend / Extension
- JavaScript
- HTML
- CSS
- Chrome Extension Manifest V3

### Browser APIs
- Chrome Declarative Net Request API
- Chrome Extension APIs

### Tools
- Git
- GitHub
- Postman
- VS Code

---

## 📁 Project Structure

```text
StudyFocus
│
├── Chrome Extension
│   ├── manifest.json
│   ├── background/service worker
│   ├── blocked.html
│   ├── popup
│   └── extension assets
│
└── Django Backend
    ├── users
    ├── blocked websites
    ├── focus sessions
    ├── authentication
    └── REST APIs
```

---

## 🔐 Authentication

StudyFocus uses **JWT-based authentication** for securing backend APIs.

The authentication flow includes:

```text
Register
   ↓
Login
   ↓
Access Token
   ↓
Authenticated API Requests
   ↓
Refresh Token
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/palaksharmaIT/study-focus-extension.git
cd study-focus-extension
```

### 2. Backend Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the Django server:

```bash
python manage.py runserver
```

---

### 3. Load the Chrome Extension

Open Chrome and go to:

```text
chrome://extensions/
```

Enable:

**Developer mode**

Click:

**Load unpacked**

Select the Chrome extension folder.

---

## 🌐 Blocked Websites

The extension can be configured to block distracting websites such as:

- YouTube
- Instagram
- Facebook
- Reddit
- Netflix
- X

When Study Mode is active, users are redirected to the StudyFocus blocked page when attempting to access a blocked website.

---

## 🔄 Current Focus

This project is being developed and improved as part of my backend development learning journey.

Future improvements may include:

- More detailed productivity analytics
- Improved session tracking
- Custom blocking schedules
- Better dashboard experience
- Additional productivity features

---

## 👩‍💻 Author

**Palak Sharma**

Python Developer Intern | Backend Development | AI/GenAI

GitHub: https://github.com/palaksharmaIT