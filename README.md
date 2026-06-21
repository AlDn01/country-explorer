# Country Explorer CLI

## Project Description

Country Explorer is a Python CLI application that uses the [REST Countries API](https://restcountries.com) to fetch and display real-world country data. It allows users to search for countries, compare them side by side, and explore population statistics by region.

The project demonstrates how REST APIs work in practice — HTTP requests, JSON parsing, error handling, and session-based caching — using Python's `requests` library.

---

## Features

* **Search a country** by name and view:
  * Official name, capital, region, population, area, and currencies
  * Languages spoken
  * Bordering countries (resolved by name, not just country code)
* **Compare two countries** side by side:
  * Population difference
  * Area difference
  * Which country has more official languages
  * Clean, formatted comparison output
* **List the top 5 most populous countries** in a region:
  * Africa, Americas, Asia, Europe, Oceania
* **Graceful error handling** for:
  * Country not found
  * No internet connection
  * Invalid user input
  * API timeout (5-second limit on all requests)

---

## Project Structure

```
country-explorer/
│
├── country_api.py        # API layer — all REST Countries calls (Asem)
├── country_y.py           # CLI application — menu, flow, session cache (Yusuf)
│
├── ui/
│   ├── comparison.py      # Country comparison logic (Allaa)
│   └── formatting.py      # Output formatting (Allaa)
│
└── README.md
```

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/USERNAME/country-explorer.git
cd country-explorer
```

### 2. Install dependencies

```bash
pip install requests
```

### 3. Run the program

```bash
python country_y.py
```

Make sure Python 3 is installed on your system.

---

## Requirements

* Python 3.x
* `requests` library (only external dependency)

---

## System Design

The application is structured into three main layers:

* **API Layer (`country_api.py`):** Wraps all calls to the REST Countries API inside a `CountryExplorer` class, parses JSON responses with `.get()` for safety, and handles connection errors and timeouts.
* **CLI / Application Layer (`country_y.py`):** Handles the menu system, user input, and the in-memory session cache so the same country isn't fetched twice in one run.
* **UI Layer (`ui/comparison.py`, `ui/formatting.py`):** Handles the side-by-side comparison logic and turns raw data into clean, readable terminal output.

---

## Team Contributions

### Yusuf — Application Structure & Session Cache

* Built the CLI menu system and overall application flow
* Implemented the in-memory session cache so repeated lookups don't re-trigger network requests
* Connected the UI layer to the API layer
* Handled navigation between the search, compare, and region-listing features



### Asem — API Integration & Data Layer

* Built the `CountryExplorer` class and all API call methods
* Implemented JSON parsing using `.get()` to safely navigate nested fields
* Implemented error handling for not-found countries, connection errors, and timeouts (5s)
* Migrated the project from REST Countries v3.1 to v5 after the API changed mid-project

**Reflection — what I learned about how the web works:**
Before this project, I had a vague idea that apps "get data from the internet," but I never understood the mechanics behind it. Building the API layer for Country Explorer taught me exactly how that works: your program sends an HTTP GET request to a specific URL, and the server responds with a status code and a JSON body. What surprised me most was how much can go wrong between those two steps — the server might not find what you asked for, your connection might drop, the request might time out, or the API itself might change its entire structure overnight, which is exactly what happened to us when REST Countries deprecated v3.1 mid-project and we had to migrate to v5 on the fly. Debugging that live taught me more about how APIs actually behave in the real world than any tutorial could. I also learned that a simple Python dictionary is enough to build a session cache that prevents your app from making the same network request twice, which showed me that good software is not just about making things work but about making them work efficiently.

### Allaa — Comparison, Formatting & README

* Designed the side-by-side comparison logic (population, area, language count)
* Implemented output formatting for clean, readable terminal output
* Wrote and structured this README
* Verified integration between the API, CLI, and UI layers


---

## Notes

* All data is fetched live from the REST Countries API — nothing is hardcoded
* Country lookups are cached for the duration of a session to avoid duplicate requests
* All requests use a 5-second timeout to prevent the app from hanging on a slow connection

---

## Future Improvements

* Add a GUI or web version (Tkinter / Flask)
* Persist the cache to disk so it survives between runs
* Add more comparison categories (e.g. GDP, time zones, currencies)
* Add unit tests for the API and comparison logic
