# 🏅 Olympics Analysis Web App

A Streamlit-based interactive web application for in-depth analysis and visualization of the Summer Olympics dataset. This project enables users to explore trends, medal tallies, country-wise performance, and athlete statistics in an engaging and insightful way.

## 📊 Features

- 📍 **Medal Tally Viewer**  
  View overall or year/country-specific medal tallies.

- 🌍 **Overall Olympics Analysis**  
  Key statistics including editions, host cities, sports, nations, athletes, and events over time.  
  Includes:
  - Participating nations over years
  - Number of events and athletes trend
  - Heatmap of events per sport per year
  - Most successful athletes overall or per sport

- 🏳️ **Country-wise Analysis**  
  Detailed analysis of a selected country's Olympic history:
  - Medal tally over years
  - Sport-wise performance heatmap
  - Top 10 most successful athletes

- 🧍‍♂️🧍‍♀️ **Athlete-wise Analysis**  
  Visual distribution of athlete ages:
  - Medal-specific age distributions
  - Gold medalist age distribution by sport
  - Height vs Weight visualization across sports

- 👨‍🦰👩 **Male vs Female Participation**  
  Line chart visualizing participation trends of men vs women across years.

---

## 📂 Dataset Used

- **[athlete_events.csv](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)**  
  Athlete-level data including sport, event, medal, and demographics.

- **noc_regions.csv**  
  Mapping between NOC (National Olympic Committee) codes and their respective regions/countries.

---

## 🛠️ Tech Stack

- **Frontend & Interactivity**: [Streamlit](https://streamlit.io/)
- **Data Handling**: Pandas, NumPy
- **Visualization**: Plotly, Seaborn, Matplotlib
- **IDE for Analysis**: Jupyter Notebook (for initial exploration)

---

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/olympics-analysis-app.git
   cd olympics-analysis-app
