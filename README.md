# 🛡️ DataGuard: Automated GDPR Compliance Auditor

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.0+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

**DataGuard** is a full-stack automated auditing tool designed to help website owners verify their compliance with European **GDPR (General Data Protection Regulation)** standards.

---

## 🚀 Key Features

- **Automated SSL Audit:** Verifies if the target website enforces secure HTTPS protocols.
- **Privacy Policy Detection:** Uses DOM parsing to locate mandatory legal documentation.
- **Cookie Consent Heuristics:** Scans for active cookie notices and user consent frameworks.
- **Persistent Scan History:** Saves all audit results to a local SQLite database for historical tracking.
- **Modern Dashboard:** A clean, responsive UI built with Tailwind CSS.

## 🛠️ Technical Architecture

- **Backend:** Python 3.x with **FastAPI** for high-performance asynchronous API routing.
- **Web Scraping:** **BeautifulSoup4** & **Requests** for real-time website analysis.
- **Database:** **SQLite3** for lightweight, persistent data storage.
- **Frontend:** **Vanilla JavaScript** with **Tailwind CSS** for a professional, scalable interface.

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/SohamCode-Main/dataguard-scanner.git](https://github.com/SohamCode-Main/dataguard-scanner.git)
   cd dataguard-scanner