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
