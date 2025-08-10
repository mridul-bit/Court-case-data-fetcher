# Delhi High Court Case Scraper

This project provides a web-based application to query and fetch case details from the **Delhi High Court** public case search portal for the current year. It features a simple frontend UI form and a backend scraper that programmatically fills the official court website’s form, bypasses the CAPTCHA, and extracts case details including parties, hearing dates, and judgment PDF links.

---

## Prerequisites and Setup

### Backend

- Python 3.8+
- [Playwright](https://playwright.dev/python/) for browser automation
- Django 4.x (or compatible)
- Django REST Framework
- SQLite (default, can be switched to PostgreSQL)
- Node.js and npm (for frontend build)

#### Installing backend dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Playwright browsers
playwright install

Frontend

    React 18+

    Tailwind CSS (optional, for styling)

    Axios (for API calls)

Installing frontend dependencies

cd frontend
npm install

Court Website

We scrape the Delhi High Court case search portal:

    URL: https://delhihighcourt.nic.in/app/

    We dynamically fetch:

        Case types dropdown options

        Filing years dropdown options

        CAPTCHA text shown on the court site

The scraper respects the current year and form inputs as shown on the site.
What We Did — Step by Step

    Built a simple React frontend form with dropdowns for:

        Case Type (populated dynamically from court website via scraper)

        Filing Year (populated dynamically)

        Case Number (user input)

        CAPTCHA text (user input, mandatory)

    Backend scraper using Playwright:

        Navigates to the court website

        Extracts case types and filing years dynamically to serve frontend dropdowns

        Extracts the CAPTCHA text displayed (as plain text on the site)

        Submits the search form with user inputs including CAPTCHA

        Scrapes resulting case details:

            Petitioner and respondent names

            Filing date and next hearing date

            Judgment PDF links (latest)

        Returns structured JSON data to frontend

    Storage:

        Saves each query and its raw HTML response in SQLite

        Stores parsed case details in related tables

    Display:

        Shows parsed details nicely on the frontend

        Allows users to download judgment PDFs if available

    Error Handling:

        Displays clear error messages for invalid case numbers or wrong CAPTCHA

        Automatically reloads CAPTCHA on wrong input

Handling CAPTCHA

    The CAPTCHA on the court site is a simple 4-digit number displayed as text inside a <span> element (not an image).

    We extract this text programmatically and display it in the frontend form.

    The user must manually type the CAPTCHA before submitting.

    If the CAPTCHA is incorrect, the backend returns an error, the frontend reloads the new CAPTCHA text, and asks the user to try again.

    This avoids complex image processing or OCR.

Running the Project
Backend

source venv/bin/activate
python manage.py runserver

Frontend

cd frontend
npm start

Visit http://localhost:3000 in your browser.
Project Structure Highlights

    backend/app/scraper.py — Playwright scraper logic to interact with court website

    backend/app/views.py — API endpoints for frontend interaction

    frontend/src/components/CaseForm.js — User input form with dynamic dropdowns and CAPTCHA display

    frontend/src/App.js — Main React component managing state and API calls

Notes

    The scraper uses headless Chromium via Playwright.

    The project respects the court’s current UI and form structure; selectors are chosen accordingly.

    The design is minimalistic and user-friendly.

    The storage schema is simple but can be extended.
