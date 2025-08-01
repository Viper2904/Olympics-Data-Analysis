import numpy as np

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df.copy()
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country].copy()
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)].copy()
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)].copy()

    for medal in ['Gold', 'Silver', 'Bronze']:
        if medal not in temp_df.columns:
            temp_df[medal] = 0

    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x[['Gold', 'Silver', 'Bronze', 'total']] = x[['Gold', 'Silver', 'Bronze', 'total']].astype(int)

    return x

def overall_medal_tally(df):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_df = medal_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()
    medal_df['total'] = medal_df['Gold'] + medal_df['Silver'] + medal_df['Bronze']
    medal_df[['Gold', 'Silver', 'Bronze', 'total']] = medal_df[['Gold', 'Silver', 'Bronze', 'total']].astype(int)
    return medal_df

def country_year_list(df):
    years = df['Year'].dropna().unique().tolist()
    years = sorted(years)
    years.insert(0, 'Overall')

    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries

def data_over_time(df, col):
    df_unique = df.drop_duplicates(subset=['Year', col])
    count_df = df_unique.groupby('Year').count()[col].reset_index()
    count_df.rename(columns={col: 'count'}, inplace=True)
    return count_df

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Name', 'Medals']

    merged_df = top_athletes.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates('Name')

    return merged_df

def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    
    return final_df

def country_event_heatmap(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    
    new_df=temp_df[temp_df['region']=='India']
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Name', 'Medals']

    top_athletes = top_athletes.head(10)

    merged_df = top_athletes.merge(df[['Name', 'Sport']], on='Name', how='left').drop_duplicates('Name')

    return merged_df

def weight_vs_height(df,sport):
    athletes_df=df.drop_duplicates(subset=['Name','region'])
    athletes_df['Medal'].fillna('No Medal',inplace=True)
    temp_df=athletes_df[athletes_df['Sport']=='Athletics']
    return temp_df

def men_vs_women(df):
    athletes_df=df.drop_duplicates(subset=['Name','region'])
    
    men=athletes_df[athletes_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=athletes_df[athletes_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    
    final=men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'})
    
    final.fillna(0,inplace=True)
    return final
