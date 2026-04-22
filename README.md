# Careem Bike Availability Tracker (Dubai)

An automated data pipeline that scrapes real-time bike availability data from the Careem Bike API, stores it in Supabase, and generates an interactive map visualization.

## 🚀 Project Overview
This project is designed as a self-updating data product. It monitors bike station statuses across Dubai, allowing for trend analysis and real-time availability viewing via a web-based map.

- **Data Source:** Careem Bike GBFS API.
- **Backend:** Supabase (PostgreSQL) for historical data storage.
- **Automation:** GitHub Actions (CI/CD) running on a cron schedule.
- **Visualization:** Plotly (HTML Map) and GeoJSON for GitHub preview.
- **Deployment:** GitHub Pages.

## 🛠️ Tech Stack
- **Language:** Python 3.10
- **Libraries:** Pandas, Plotly, Requests, GeoPandas, Supabase-py
- **Infrastructure:** GitHub Actions, Supabase
- **Hosting:** GitHub Pages

## 📁 Repository Structure
- `.github/workflows/`: Contains the YAML configuration for the automated scraper and map generator.
- `generate_latest_map.py`: The core engine that processes data and creates the visualizations.
- `latest_bike_availability_map.html`: The live interactive map (Presentation Layer).
- `map.geojson`: Geographic data layer with GitHub Simplestyle styling (Data Layer).
- `requirements.txt`: Python dependencies.

## ⚙️ How It Works
1. **Scrape:** A GitHub Action triggers every hour, running the Python scripts.
2. **Process:** The script fetches current station status from Careem and joins it with static station metadata from Supabase.
3. **Generate:** - An interactive HTML map is created with bubble sizes representing bike density.
    - A `.geojson` file is updated with marker colors based on availability.
4. **Commit & Deploy:** The Action commits the new files back to the `main` branch. GitHub Pages then automatically refreshes the live URL.

## 📊 Live Map
You can view the real-time availability map here:
[https://ayshaasif.github.io/Careem-Bike-Sharing-Analysis/latest_bike_availability_map.html](https://ayshaasif.github.io/Careem-Bike-Sharing-Analysis/latest_bike_availability_map.html)

## 🛠 Setup & Installation
If you wish to run this locally:
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set up your `.env` file with `SUPABASE_URL` and `SUPABASE_KEY`.
4. Run the generator: `python generate_latest_map.py`.
