import streamlit as st
import pandas as pd
import pre_processor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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

if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()
    
    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Hosts")
        st.title(cities)
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Sports")
        st.title(sports)
        st.header("Athletes")
        st.title(athletes)
    
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Year", y="count")
    st.title("Participating Nations over the Years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Year", y="count")
    st.title("Events over the Years")
    st.plotly_chart(fig)
    
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Year", y="count")
    st.title("Athletes over the Years")
    st.plotly_chart(fig)
    
    st.title("No. of Events over time(Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)
