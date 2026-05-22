# Castle Chess Manager

An offline-first chess tournament management application built with Python and Tkinter.

This application was developed to help chess clubs manage tournaments without requiring an internet connection. It supports player management, Swiss-style tournament rounds, score tracking, standings, JSON data persistence, and PDF report generation.

---

# Features

## Offline Operation

* Fully functional without internet access
* Local JSON-based data storage

## Tournament Management

* Create tournaments
* Add players
* Run tournament rounds
* Record match results

## Swiss Pairing System

* Basic Swiss-style pairing
* Pairings based on current standings

## Player Rankings

* Automatic score updates
* Dynamic standings generation

## Report Generation

* Generate tournament PDF reports
* Includes standings and match results

## Persistent Storage

* Save tournament data as JSON
* Reload and extendable for future enhancements

---

# Technologies Used

* Python 3
* Tkinter (GUI)
* ReportLab (PDF generation)
* JSON (data persistence)

---

# Project Structure

```text id="5ccgj2"
project/
│
├── main.py
├── ui.py
├── models.py
├── pairing.py
├── storage.py
├── report.py
├── requirements.txt
└── data/
```

---

# Installation

## 1. Clone or Download the Project

```bash id="qpf72d"
git clone <repository-url>
cd castle-chess-manager
```

Or extract the ZIP archive if downloaded manually.

---

## 2. Create Virtual Environment (Recommended)

### Windows

```bash id="h4nl4m"
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash id="fexl9c"
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash id="18iyr6"
pip install -r requirements.txt
```

---

# Running the Application

```bash id="svf4w4"
python main.py
```

---

# How to Use

## Create Tournament

1. Click **New Tournament**
2. Enter tournament name

## Add Players

1. Click **Add Player**
2. Enter player names

## Run Tournament Round

1. Click **Next Round**
2. Enter scores for each match

## View Standings

1. Click **Standings**
2. Current rankings will display

## Save Tournament

1. Click **Save**
2. Tournament data is stored as JSON

## Generate Report

1. Click **Generate Report**
2. A PDF report will be created automatically

---

# Generated Files

## Tournament Save File

```text id="ys2ihs"
TournamentName.json
```

## Tournament Report

```text id="j84h4x"
TournamentName_report.pdf
```

---

# Requirements

Contents of `requirements.txt`:

```text id="mn74k6"
reportlab==4.0.9
flake8==7.0.0
flake8-html==0.4.3
```

---

# Code Quality

This project follows:

* Object-Oriented Programming principles
* PEP 8 style guidelines

## Generate flake8 HTML Report

```bash id="t8qnyg"
flake8 . --format=html --htmldir=flake-report
```

Generated report location:

```text id="pb4ngd"
flake-report/index.html
```

---

# Current Limitations

The current version includes a simplified Swiss pairing system.

Future improvements may include:

* Advanced federation-grade Swiss pairing
* Bye management
* Tie-break systems (Buchholz, Sonneborn-Berger)
* Tournament resume/load UI
* Player editing/removal
* Professional dashboard interface
* Windows executable installer
* Chess-themed branding and logo integration

---

# Architecture

The project uses an object-oriented architecture with clear separation of concerns:

* `models.py` → Core entities
* `pairing.py` → Tournament pairing logic
* `storage.py` → Persistence layer
* `report.py` → PDF report generation
* `ui.py` → User interface


# License

This project is intended for educational purposes. An Openclassroom Project

---

# Author
Princewil Mbah

Developed as an offline chess tournament management solution for Castle Chess Club.
