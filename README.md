# Country Explorer CLI

## Project Description
Country Explorer is a Python CLI application that uses the REST Countries API to fetch and display real-world country data. It allows users to search countries, compare them, and explore population statistics by region.

The project demonstrates how REST APIs work in practice, including HTTP requests, JSON parsing, error handling, and session caching.

---

## Features

### 1. Search Country
- Official name  
- Capital  
- Region  
- Population  
- Area  
- Currencies  
- Languages  
- Bordering countries (resolved by name)

### 2. Compare Two Countries
- Population difference  
- Area difference  
- Country with more languages  
- Clean formatted comparison output  

### 3. Top 5 Most Populous Countries by Region
Supported regions:
- Africa  
- Americas  
- Asia  
- Europe  
- Oceania  

### 4. Error Handling
- Country not found  
- No internet connection  
- Invalid user input  
- API timeout (5 seconds)  

---

## Technologies Used
- Python 3  
- requests library  
- REST Countries API  

---

## Project Structure
country-explorer/
│
├── country_api.py # API layer (Asem)
├── country_y.py # CLI application (Yusuf + integration)
│
├── ui/
│ ├── comparison.py # Country comparison logic (Allaa)
│ ├── formatting.py # Output formatting (Allaa)
│
└── README.md
---

## How to Install & Run

### 1. Install dependencies
```bash
pip install requests
```

### 2. Run the application
```bash
python country_y.py
```

### 3. Team Contributions

### Yusuf

Application structure, CLI menu, session cache logic, and user interaction handling.

### Asem

API integration, JSON parsing, error handling, and building the core data layer for country retrieval.

Before this project, I had a vague idea that apps "get data from the internet," but I never understood the mechanics behind it. Building the API layer for Country Explorer taught me exactly how that works: your program sends an HTTP GET request to a specific URL, and the server responds with a status code and a JSON body. What surprised me most was how much can go wrong between those two steps, the server might not find what you asked for, your connection might drop, the request might time out, or the API itself might change its entire structure overnight, which is exactly what happened to us when REST Countries deprecated v3.1 mid-project and we had to migrate to v5 on the fly. Debugging that live taught me more about how APIs actually behave in the real world than any tutorial could. I also learned that a simple Python dictionary is enough to build a session cache that prevents your app from making the same network request twice, which showed me that good software is not just about making things work but about making them work efficiently.

### Allaa

Country comparison system and output formatting. Designed the side-by-side comparison logic and ensured the CLI output is clean, readable, and easy to interpret at a glance.