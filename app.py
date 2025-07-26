import streamlit as st
import pandas as pd
import pre_processor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

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
    
    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    
    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)
    
if user_menu=='Country-wise Analysis':
    
    st.sidebar.title('Country-wise Analysis')
    
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    
    selected_country=st.sidebar.selectbox('Select a Country',country_list)
    
    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country +" " + "Medal Tally over the Years")
    st.plotly_chart(fig)
    
    st.title(selected_country + " " + "Excels in the following sports")
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)
    
    st.title("Top 10 athletes of " + selected_country)
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu=="Athlete-wise Analysis":
    st.title("Distribution of Athlete Ages")

    athletes_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athletes_df['Age'].dropna()
    x2 = athletes_df[athletes_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athletes_df[athletes_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athletes_df[athletes_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False,
                             show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)
    
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug of War', 'Athletics', 'Swimming',
                    'Badminton', 'Gymnastics', 'Weightlifting', 'Wrestling', 'Hockey',
                    'Shooting', 'Boxing', 'Tennis', 'Golf', 'Archery']

    for sport in famous_sports:
        temp_df = athletes_df[athletes_df['Sport'] == sport]
        age_data = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if not age_data.empty:
            x.append(age_data)
            name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)

    st.title("Distribution of Age of Gold Medalists across Sports")
    st.plotly_chart(fig)
    
    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    
    st.title('Height vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_vs_height(df, selected_sport)

    fig, ax = plt.subplots()
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60, ax=ax)
    
    st.pyplot(fig)
    
st.title("Men vs Women Participation over the Years")

final = helper.men_vs_women(df)

required_columns = {'Year', 'Male', 'Female'}
if not final.empty and required_columns.issubset(final.columns):
    final_melted = final.melt(
        id_vars='Year',
        value_vars=['Male', 'Female'],
        var_name='Gender',
        value_name='Number of Athletes'
    )
    
    fig = px.line(
        final_melted,
        x='Year',
        y='Number of Athletes',
        color='Gender',
        markers=True,
        title="Trend of Male vs Female Participation"
    )
    
    st.plotly_chart(fig)
else:
    st.warning("No data available to show male vs female participation.")

