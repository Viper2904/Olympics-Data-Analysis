import streamlit as st
import pandas as pd
import pre_processor,helper

df=pre_processor.preprocess()

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)
st.dataframe(df)
if user_menu=='Medal Tally':
    medal_tally=helper.medal_tally(df)
    st.dataframe(medal_tally)