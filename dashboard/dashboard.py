import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')


all_df = pd.read_csv("all_data.csv")
all_df.sort_values(by="datetime", inplace=True)
all_df['wd'] = 'Mean'
rain_index = all_df.columns.get_loc('RAIN')
all_df.insert(rain_index+1, 'wd', all_df.pop('wd'))
all_df.reset_index(inplace=True)
all_df['datetime'] = pd.to_datetime(all_df['datetime'])

min_date = all_df['datetime'].min()
max_date = all_df['datetime'].max()

with st.sidebar:
    st.image('https://upload.wikimedia.org/wikipedia/id/thumb/7/7a/Manchester_United_FC_crest.svg/330px-Manchester_United_FC_crest.svg.png')

    selected_date = st.date_input("Choose date", all_df['datetime'].iloc[0].date()) 
    selected_hour = st.selectbox("Pilih Jam", options=range(24), format_func=lambda x: f"{x}:00")
    # selected_hour = st.time_input("Choose hour", step=(60*60))
    selected_city = st.selectbox("Pilih Kota", options=['Changping', 'Dongsi', 'Guanyuan', 'Gucheng', 'Average'])

date_filtered = all_df[
    (all_df['datetime'].dt.date == selected_date) & (all_df['hour'] == selected_hour)
]

st.header('Dashboard Air-Quality Index :dash:')

st.subheader('Daily Date')

city_parameters = {
        'Changping': ['PM25_changping','PM10_changping','SO2_changping','NO2_changping','CO_changping','O3_changping','TEMP_changping','PRES_changping','DEWP_changping','RAIN_changping','wd_changping','WSPM_changping'],
        'Dongsi': ['PM25_dongsi','PM10_dongsi','SO2_dongsi','NO2_dongsi','CO_dongsi','O3_dongsi','TEMP_dongsi','PRES_dongsi','DEWP_dongsi','RAIN_dongsi','wd_dongsi','WSPM_dongsi'],
        'Guanyuan': ['PM25_guanyuan','PM10_guanyuan','SO2_guanyuan','NO2_guanyuan','CO_guanyuan','O3_guanyuan','TEMP_guanyuan','PRES_guanyuan','DEWP_guanyuan','RAIN_guanyuan','wd_guanyuan','WSPM_guanyuan'],
        'Gucheng': ['PM25_gucheng','PM10_gucheng','SO2_gucheng','NO2_gucheng','CO_gucheng','O3_gucheng','TEMP_gucheng','PRES_gucheng','DEWP_gucheng','RAIN_gucheng','wd_gucheng','WSPM_gucheng'],
        'Average': ['PM25','PM10','SO2','NO2','CO','O3','TEMP','PRES','DEWP','RAIN','wd','WSPM']
    }

# st.write(f"Date at {selected_date} {selected_hour}:00", date_filtered)

if not date_filtered.empty:
    parameters = city_parameters[selected_city]

    display_parameters = ['CO', 'PRES', 'wd']
    parameters_to_display = [param for param in parameters if any(dp in param for dp in display_parameters)]
    parameters_to_barplot = [param for param in parameters if param not in parameters_to_display]

    CO_value = date_filtered[[p for p in parameters if 'CO' in p]].values.flatten()[0]
    PRES_value = date_filtered[[p for p in parameters if 'PRES' in p]].values.flatten()[0]
    wd_value = date_filtered[[p for p in parameters if 'wd' in p]].values.flatten()[0]

    date = date_filtered[parameters_to_barplot].melt(var_name='Parameter', value_name='Value')
  
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CO value", f"{CO_value:.2f}")
    col2.metric("PRES value", f"{PRES_value:.2f}")
    col3.metric("wd", f"{wd_value}")
    col4.metric("Station", f"{selected_city}")

    sns.set(style='darkgrid')
    fig, ax  = plt.subplots(figsize=(10,6))
    sns.barplot(
        x='Value',
        y='Parameter',
        data=date,
        ax=ax,
        palette='viridis'
    )
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f')
    ax.set_title(f'{selected_city}', fontsize=20)
    ax.set_xlabel('Value')
    ax.set_ylabel('Parameter')

    st.pyplot(fig, use_container_width=True)

else:
    st.write('Date not available')

st.caption('Copyright (c) TsunamiTrophy 2025')