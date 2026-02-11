# Chemical-Equipment-Analyser

Hybrid Web + Desktop Application for CSV-based data analytics and visualization

---

## Installation and Run

1. download/ clone this repository
(make sure that Python and pip, Node and npm are installed on your machine)
2. open a terminal, navigate to this repository location and run this command: `pip install -r requirements.txt`
3. create a superuser to log into the system, use the command: `python manage.py createsuperuser` (this will prompt you to choose a username and assign a password to it)
4. navigate to web folder, using: `cd web`
5. run this command: `npm install`
6. navigate back to the repository root location, using: `cd ..`
7. to run the server locally, run these commands: 
    `python manage.py migrate`
    `python manage.py runserver`
8. to run the webpage - create a new terminal instance -> navigate to the web folder(`cd web`) and run: `npm run start` (On Windows - run this command in a CMD instance, Powershell may block script execution)
9. to open a desktop app window - create a new terminal instance -> navigate to the desktop folder(cd desktop) and run: `python main.py`
10. this will create both web and desktop based interfaces for the you to interact with

---

## Project Overview

The **Chemical Equipment Analyser** is a hybrid application that runs as both:

* a **Web Application (React + Chart.js)**, and
* a **Desktop Application (PyQt5 + Matplotlib)**,

powered by a **shared Django backend**.

The application allows authenticated users to upload CSV files containing chemical equipment data, performs analytics using Pandas, stores 5 recent datasets, visualizes results, and generates downloadable PDF reports.

---

## Architecture

```
React (Web) ─────┐
                 │
PyQt (Desktop) ──┼──▶ Django API ──▶ SQLite
                 │           │
                 │           ├── Pandas (CSV analytics)
                 │           └── ReportLab (PDF generation)
```

### Key Principles

* One **shared backend** for both web and desktop
* Frontends communicate **only via REST APIs**
* Backend enforces business rules (last 5 datasets, auth, analytics)

---

## Tech Stack

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

## Features

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

## Project Structure

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

## Authentication Flow

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

## CSV Format

Required CSV headers:

```
Equipment Name,Type,Flowrate,Pressure,Temperature
```

Example row:

```
Pump A,Pump,12.5,4.2,90
```

---

## PDF Reports

Each dataset can generate a PDF containing:

* upload timestamp
* total equipment count
* averages
* equipment type distribution

PDFs can be downloaded from:

* React Web UI
* PyQt Desktop UI

---

## API Endpoints

| Method | Endpoint                  | Description          |
| ------ | ------------------------- | -------------------- |
| POST   | `/api/login/`             | Login & get token    |
| POST   | `/api/upload/`            | Upload CSV           |
| GET    | `/api/datasets/`          | List last 5 datasets |
| GET    | `/api/datasets/<id>/pdf/` | Download PDF report  |
