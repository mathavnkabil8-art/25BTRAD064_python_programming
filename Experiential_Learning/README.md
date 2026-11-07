# 🚌 RouteIQ — Intelligent Commute & Route Optimization System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Tests-Pytest](https://img.shields.io/badge/Tests-PyTest%20(30%20Passed)-brightgreen.svg?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%20%7C%20WebView2-informational.svg?logo=windows&logoColor=white)]()
[![Code Style: Ruff](https://img.shields.io/badge/Code%20Style-Ruff-000000.svg)](https://github.com/astral-sh/ruff)

> An algorithm-driven, multi-modal commute optimization desktop application built with Python. Combines **multi-hop Dijkstra graph pathfinding**, **Google Maps Routes API v2** with real-time traffic awareness, a native **Microsoft Edge WebView2 interactive map**, and an **embedded Matplotlib analytics dashboard** backed by thread-safe **SQLite persistence**.

---

## 📌 Problem Statement & Objectives

Daily commuters often navigate fragmented transit networks with multiple conflicting priorities: minimizing journey time, reducing out-of-pocket travel expenses, and minimizing their carbon footprint. Most standard routing calculators focus strictly on direct roads and single-vehicle choices, failing to evaluate multi-modal combinations or explain the trade-offs between competing options.

**RouteIQ** bridges this gap by:
1. Evaluating multi-modal transit networks across multiple connected hubs.
2. Balancing competing constraints via **Min-Max Normalized Multi-Objective Scoring**.
3. Providing real-time road routing with traffic-delayed ETAs via **Google Maps Routes API v2**.
4. Rendering interactive routes directly on a desktop map via **Microsoft Edge WebView2**.
5. Tracking historical spending, duration averages, and environmental impact via an **embedded analytics dashboard**.

---

## 🌟 Key Features

### 1. Dual-Mode Routing Architecture
- **🟢 Live Google Maps Mode**:
  - Accepts arbitrary street addresses, landmarks, and city locations.
  - Queries Google Maps Routes API v2 (`computeRoutes`) with traffic-aware driving (`TRAFFIC_AWARE`), transit, two-wheeler, and walking calculations.
  - Computes alternative routes, exact route distance, and real-time congestion delays.
- **🟠 Offline Hub Network Mode**:
  - Operates completely offline with zero internet or API key requirements.
  - Traverses the campus/city multi-hop graph using **Dijkstra's Shortest Path Algorithm** with heap priority queues (`heapq`).
  - Evaluates all possible multi-hop transit combinations without integer truncation.
- **Resilient Fallback**:
  - If API keys are missing, invalid, or over quota, RouteIQ clearly labels the mode as `[🟠 Offline / Demo Mode]` and prompts the user to switch seamlessly rather than crashing.

### 2. Multi-Criteria Route Optimization Engine
Evaluates routes across four distinct user perspectives simultaneously:
- **⚡ Fastest Route**: Minimizes total travel duration, factoring in rush-hour road delays.
- **💰 Cheapest Route**: Minimizes total out-of-pocket fare cost across all segments.
- **🌱 Greenest Route**: Minimizes greenhouse gas footprint ($CO_2$ kg) using passenger-km emission models.
- **⚖️ Balanced Route**: Evaluates a weighted multi-objective cost function:
  $$\text{Score} = 0.45 \cdot \hat{T}_{\text{norm}} + 0.35 \cdot \hat{C}_{\text{norm}} + 0.20 \cdot \hat{E}_{\text{norm}}$$

### 3. Route Explanation & Trade-Off Engine
Explains the mathematical trade-offs in plain human language (e.g., *"Choosing Public Bus saves ₹165 and cuts carbon emissions by 65% with only an 8-minute increase in transit time compared to Cab"*).

### 4. Interactive Desktop WebView2 Map
- Renders an interactive map embedded inside a dedicated Microsoft Edge WebView2 native desktop window via `pywebview`.
- Displays real polyline route geometry, traffic layers, start/destination pins, and turn-by-turn route summaries.
- Automatically falls back to the default web browser if WebView2 is unavailable in the environment.

### 5. Advanced Analytics Dashboard with Matplotlib
- Embedded Matplotlib visual charts (`FigureCanvasTkAgg`):
  - **Transport Mode Share**: Donut chart showing commute mode distribution.
  - **Monthly Expenditure Trends**: Bar chart visualizing spending over time.
- High-level KPI summary cards: Total Trips, Total Cash Spent, Average Duration, Top Transport Mode, Estimated Carbon Footprint, and Optimization Time Saved.

### 6. SQLite Persistence & Safe CSV Migration
- Thread-safe SQLite database (`commute_history.db`) with WAL mode and parameterized queries.
- **Zero Data Loss**: Automatically migrates historical records from legacy `commute_history.csv` on application startup without duplicating records or fabricating unknown historical fields.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ (tested on Python 3.13.5) |
| **User Interface** | Tkinter, `ttk.Notebook`, `ttk.Treeview` |
| **Map Rendering** | Microsoft Edge WebView2 (`pywebview`), Google Maps JS API, Leaflet |
| **External APIs** | Google Maps Platform (Routes API v2, Geocoding API) |
| **HTTP Networking** | Requests (with SSL verification and strict timeouts) |
| **Persistence** | SQLite3 (WAL mode, parameterized queries), CSV (UTF-8) |
| **Data Visualization** | Matplotlib (`FigureCanvasTkAgg`) |
| **Automated Testing** | PyTest (with unittest.mock) |
| **Environment & Config** | python-dotenv |

*(Technologies listed are strictly those utilized in the codebase).*

---

## 🏛️ System Architecture

```
RouteIQ/
├── main.py                          # Primary entry point with backward-compatible aliases
├── .env.example                     # Environment template for Google Maps API configuration
├── .gitignore                       # Git exclusion rules (secrets, venv, databases, caches)
├── requirements.txt                 # Production dependencies
├── requirements-dev.txt             # Development and testing dependencies
├── LICENSE                          # MIT License
├── pyproject.toml                   # Standard Python build and tool configuration
├── README.md                        # Project documentation
│
├── config/                          # Centralized configuration management
│   ├── __init__.py
│   └── settings.py                  # Immutable AppConfig, .env loader, fare & emission rates
│
├── src/
│   └── routeiq/
│       ├── __init__.py
│       ├── core/                    # Domain models, constants, and custom exceptions
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── constants.py
│       │   └── exceptions.py
│       ├── routing/                 # Pathfinding, Dijkstra, and API clients
│       │   ├── __init__.py
│       │   ├── offline_router.py
│       │   ├── google_routes.py
│       │   ├── geocoding.py
│       │   ├── route_provider.py
│       │   └── route_optimizer.py
│       ├── optimization/            # Multi-criteria scoring & rationale engine
│       │   ├── __init__.py
│       │   ├── multi_criteria.py
│       │   └── recommendation.py
│       ├── analytics/               # Statistical KPIs and Matplotlib charts
│       │   ├── __init__.py
│       │   ├── commute_analytics.py
│       │   └── visualization.py
│       ├── database/                # SQLite and CSV persistence
│       │   ├── __init__.py
│       │   ├── database.py
│       │   ├── repository.py
│       │   └── migration.py
│       ├── services/                # Application coordination layer
│       │   ├── __init__.py
│       │   └── trip_service.py
│       ├── ui/                      # Modular Tkinter interface
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── route_tab.py
│       │   ├── trip_tab.py
│       │   └── analytics_tab.py
│       ├── maps/                    # WebView2 desktop map renderer
│       │   ├── __init__.py
│       │   └── map_view.py
│       └── utils/                   # Logging with secret masking and input validators
│           ├── __init__.py
│           ├── logging_config.py
│           └── validators.py
│
├── data/                            # Application data directory
│   └── .gitkeep
├── assets/                          # Application graphics and media assets
│   └── .gitkeep
├── docs/                            # In-depth architectural, setup, and security guides
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   └── SECURITY.md
└── tests/                           # PyTest test suite (30 automated tests)
    ├── __init__.py
    ├── test_routing.py
    ├── test_optimization.py
    ├── test_analytics.py
    ├── test_database.py
    ├── test_geocoding.py
    ├── test_validation.py
    └── test_ui_integration.py
```

---

## 🚀 Quickstart & Installation

### Step 1: Clone Repository & Open Directory
```powershell
cd "E:\semester 3\python programming\PythonProject1\PythonProject"
```

### Step 2: Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Step 3: Configure Environment (Optional for Live Mode)
To use live Google Maps routing:
1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Open `.env` and configure your Google Maps API keys:
   ```ini
   GOOGLE_ROUTES_API_KEY=AIzaSyYourRoutesKeyHere
   GOOGLE_GEOCODING_API_KEY=AIzaSyYourGeocodingKeyHere
   GOOGLE_MAPS_JS_API_KEY=AIzaSyYourMapsJSKeyHere
   ```
*(If left blank, RouteIQ automatically runs in **Offline / Demo Mode**).*

### Step 4: Run the Application
```powershell
python main.py
```

### Step 5: Run Automated Tests
```powershell
python -m pytest tests/ -v
```

---

## 🔒 Security & Privacy

- **Zero Hardcoded Keys**: API credentials are loaded dynamically from environment variables.
- **Key Segregation**: Server-side Routes API keys are never written to HTML map files or exposed in frontend JavaScript.
- **Log Masking**: Centralized logging filters automatically replace potential API key strings with `[REDACTED_API_KEY]`.
- **User Privacy**: Private commute histories and local databases are strictly excluded from version control via `.gitignore`.
- For complete security guidelines, see [docs/SECURITY.md](docs/SECURITY.md).

---

## 🔮 Future Enhancements
- [ ] GTFS (General Transit Feed Specification) feed integration for live municipal bus schedules.
- [ ] Machine learning-based travel time prediction using historical weather data.
- [ ] Automated weekly PDF commute summary export.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 👤 Author
Developed as an advanced academic and engineering showcase project.  
**RouteIQ Engineering Team** (2026).
