import streamlit as st
import pandas as pd
import pre_processor, helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = pre_processor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, countries = helper.country_year_list(df)
    
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)
    
    medal_tally_df = helper.fetch_medal_tally(df, selected_year, selected_country)
    
    title = ''
    if selected_year == 'Overall' and selected_country == 'Overall':
        title = 'Overall Medal Tally'
    elif selected_year == 'Overall':
        title = f"Medal Tally for {selected_country}"
    elif selected_country == 'Overall':
        title = f"Medal Tally in {selected_year} Olympics"
    else:
        title = f"{selected_country} Performance in {selected_year} Olympics"

    st.title(title)
    st.dataframe(medal_tally_df)
