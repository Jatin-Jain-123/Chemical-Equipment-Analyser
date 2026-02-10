# Chemical-Equipment-Analyser
# Chemical Equipment Parameter Visualizer

Hybrid Web + Desktop Application for CSV-based data analytics and visualization

---

## 📌 Project Overview

The **Chemical Equipment Parameter Visualizer** is a hybrid application that runs as both:

* a **Web Application (React + Chart.js)**, and
* a **Desktop Application (PyQt5 + Matplotlib)**,

powered by a **shared Django REST backend**.

The application allows authenticated users to upload CSV files containing chemical equipment data, performs analytics using Pandas, stores recent datasets, visualizes results, and generates downloadable PDF reports.

This project was built as part of an **Intern Screening Task** to demonstrate full‑stack development, API design, data processing, and UI consistency across platforms.

---

## 🧱 Architecture

```
React (Web) ─────┐
                 │
PyQt (Desktop) ──┼──▶ Django REST API ──▶ SQLite
                 │           │
                 │           ├── Pandas (CSV analytics)
                 │           └── ReportLab (PDF generation)
```

### Key Principles

* One **shared backend** for both web and desktop
* Frontends communicate **only via REST APIs**
* Backend enforces business rules (last 5 datasets, auth, analytics)

---

## ⚙️ Tech Stack

| Layer            | Technology                    |
| ---------------- | ----------------------------- |
| Backend          | Django, Django REST Framework |
| Auth             | Token-based authentication    |
| Data Processing  | Pandas                        |
| Database         | SQLite                        |
| Web Frontend     | React, Chart.js               |
| Desktop Frontend | PyQt5, Matplotlib             |
| PDF Reports      | ReportLab                     |
| Version Control  | Git & GitHub                  |

---

## ✨ Features

### Core Features

* CSV file upload (Web + Desktop)
* Automatic data analytics:

  * total equipment count
  * average flowrate, pressure, temperature
  * equipment type distribution
* Data visualization:

  * Chart.js (Web)
  * Matplotlib (Desktop)
* Token-based authentication
* Dataset history management (last 5 uploads only)
* PDF report generation and download

### UX Features

* Auto-updating dataset list in React
* Secure API access using tokens
* Shared backend logic across platforms

---

## 📁 Project Structure

```
project-root/
├── backend/
│   ├── backend/          # Django project settings
│   ├── uploads/          # CSV, analytics, PDF, APIs
│   ├── media/            # Uploaded CSVs & PDFs
│   └── manage.py
├── web/                  # React frontend
├── desktop/              # PyQt desktop app
└── README.md
```

---

## 🚀 Setup Instructions

### 1️⃣ Backend Setup (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend runs at:

```
http://127.0.0.1:8000/
```

---

### 2️⃣ Web Frontend Setup (React)

```bash
cd web
npm install
npm start
```

Web app runs at:

```
http://localhost:3000/
```

---

### 3️⃣ Desktop App Setup (PyQt)

```bash
cd desktop
pip install PyQt5 requests matplotlib
python main.py
```

---

## 🔐 Authentication Flow

1. User logs in via Web or Desktop UI
2. Django returns an auth token
3. Token is included in API headers:

```
Authorization: Token <token>
```

4. Protected endpoints:

* `/api/upload/`
* `/api/datasets/`
* `/api/datasets/<id>/pdf/`

---

## 📊 CSV Format

Required CSV headers:

```
Equipment Name,Type,Flowrate,Pressure,Temperature
```

Example row:

```
Pump A,Pump,12.5,4.2,90
```

---

## 📄 PDF Reports

Each dataset can generate a PDF containing:

* upload timestamp
* total equipment count
* averages
* equipment type distribution

PDFs can be downloaded from:

* React Web UI
* PyQt Desktop UI

---

## 🧪 API Endpoints

| Method | Endpoint                  | Description          |
| ------ | ------------------------- | -------------------- |
| POST   | `/api/login/`             | Login & get token    |
| POST   | `/api/upload/`            | Upload CSV           |
| GET    | `/api/datasets/`          | List last 5 datasets |
| GET    | `/api/datasets/<id>/pdf/` | Download PDF report  |

---

## 🎥 Demo

A short demo video (2–3 minutes) shows:

* login
* CSV upload
* charts
* PDF download
* web + desktop usage

---

## 🧠 Learning Outcomes

This project demonstrates:

* full‑stack architecture
* REST API design
* frontend–backend integration
* data analytics with Pandas
* secure token-based authentication
* cross-platform UI development

---

## 📌 Notes

* SQLite is used for simplicity and demo purposes
* Backend automatically deletes oldest datasets beyond 5
* Project emphasizes clarity, correctness, and real-world patterns

---

## 👤 Author

Built as an **Intern Screening Task project** to demonstrate practical full‑stack development skills.

---

## ✅ Status

✔ Complete
✔ Fully functional
✔ Ready for submission
