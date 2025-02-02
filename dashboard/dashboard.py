import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# load file csv
day_df = pd.read_csv('../data/day.csv')
hour_df = pd.read_csv('../data/hour.csv')

# helper function
def get_avg_metrics(df):
    temp = df['temp'].mean()
    atemp = df['atemp'].mean()
    humidity = df['hum'].mean()
    windspeed = df['windspeed'].mean()
    return {
        'temp': temp,
        'atemp': atemp,
        'hum': humidity,
        'windspeed': windspeed
    }

def convert_to_original(df):
    temp = round(df['temp'] * 41)
    atemp = round(df['atemp'] * 50)
    humidity = round(df['hum'] * 67)
    windspeed = round(df['windspeed'] * 100)
    return {
        'temp': temp,
        'atemp': atemp,
        'hum': humidity,
        'windspeed': windspeed
    }

# Styling Dashboard
st.title('Dashboard Bike Sharing Dataset:bike:')

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar: # Create sidebar
    st.image("../img.jpeg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )
    
    main_df = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]

Average = get_avg_metrics(main_df)  # Get average metrics element
environment_condition = convert_to_original(Average) # Convert metric elements to original units 

st.subheader('Kondisi Lingkungan & jumlah total penyewaan sepeda')
col1, col2, col3, col4, col5 = st.columns(5)

with col1: # Metric show average temp in a period
    temp = environment_condition['temp']
    st.metric(label='Temperature', value=f"{temp} °C")
    st.markdown('AVG')

with col2: # Metric show average apparent temp in a period
    atemp = environment_condition['atemp']
    st.metric(label='A.Temperature', value=f"{atemp} °C")
    st.markdown('AVG')


with col3: # Metric show average humidity in a period
    hum = environment_condition['hum']
    st.metric(label='Humidity', value=f"{hum}%")
    st.markdown('AVG')

with col4: # Metric show average windspeed in a period
    wind = environment_condition['windspeed']
    st.metric(label='Windspeed', value=f"{wind} m/s")
    st.markdown('AVG')

with col5: # Metric show total of bike shared in a period
    total = main_df['cnt'].sum()
    st.metric(label='Total rented', value=total)
    st.markdown('SUM')



st.subheader(f"Grafik penyewaan sepeda dalam sebuah periode")
fig, ax = plt.subplots(figsize=(20, 10))

ax.plot(main_df['dteday'], main_df['cnt'], color='darkblue', marker='s')
ax.set_title(f'Total penyewaan dalam periode {start_date}-{end_date}', loc='center', fontsize=20)
ax.set_xlabel('Tanggal', fontsize= 10)
ax.set_ylabel('Total', fontsize= 10)
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)


st.subheader(f"Perbandingan jumlah penyewaan user casual dan user registered setiap bulan")

daydf_bymonth = day_df.groupby(by=['yr', 'mnth']).agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
}).reset_index()

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 8))

month_name = ['jan', 'feb', 'mar', 'apr', 'may' ,'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

# Pada tahun pertama
ax[0].plot(daydf_bymonth[daydf_bymonth['yr'] == 0]['mnth'], daydf_bymonth[daydf_bymonth['yr'] == 0]['casual'], marker='s', linewidth=2, color='darkgreen', label='Casual')
ax[0].plot(daydf_bymonth[daydf_bymonth['yr'] == 0]['mnth'], daydf_bymonth[daydf_bymonth['yr'] == 0]['registered'], marker='s', linewidth=2, color='darkblue', label='Registered')
ax[0].set_title('Jumlah penyewaan sepeda berdasarkan bulan pada tahun pertama', loc='center')
ax[0].set_xlabel('Bulan', fontsize=10)
ax[0].set_ylabel('Jumlah total perbulan',fontsize=10)
ax[0].set_xticks(range(1, 13))
ax[0].set_xticklabels(month_name)
ax[0].legend(loc='upper right')
ax[0].tick_params(axis = 'y', labelsize=12)


# Pada tahun kedua
ax[1].plot(daydf_bymonth[daydf_bymonth['yr'] == 1]['mnth'], daydf_bymonth[daydf_bymonth['yr'] == 1]['casual'], marker='s', linewidth=2, color='darkgreen', label='Casual')
ax[1].plot(daydf_bymonth[daydf_bymonth['yr'] == 1]['mnth'], daydf_bymonth[daydf_bymonth['yr'] == 1]['registered'], marker='s', linewidth=2, color='darkblue', label='Registered')
ax[1].set_title('Jumlah penyewaan sepeda berdasarkan bulan pada tahun kedua', loc='center')
ax[1].set_xlabel('Bulan', fontsize=10)
ax[1].set_ylabel('Jumlah total perbulan', fontsize=10)
ax[1].set_xticks(range(1, 13))
ax[1].set_xticklabels(month_name)
ax[1].legend(loc='upper right')
ax[1].tick_params(axis = 'y', labelsize=12)
plt.suptitle('Perbandingan jumlah penyewaan sepeda user casual dan registered berdasarkan bulan', fontsize=20)
st.pyplot(fig)

metric1, metric2 = st.columns(2)

with metric1: # Metric show total of casual user rented
    casual = day_df['casual'].sum()
    st.metric('Casual Total', value=casual)
    st.markdown('SUM')

with metric2: # Metric show total of registered user rented
    registered = day_df['registered'].sum()
    st.metric('Registered Total', value=registered)
    st.markdown('SUM')


st.caption('Copyright (c) 2025')