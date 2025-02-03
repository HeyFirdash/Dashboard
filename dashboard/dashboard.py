import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# load file csv
main_df = pd.read_csv('main.csv')
time_df = pd.read_csv('time.csv')

main_df['dteday'] = pd.to_datetime(main_df['dteday'])

# helper function

def get_avg_metrics(df):
    temp = df['temp'].mean()
    atemp = df['atemp'].mean()
    humidity = df['hum'].mean()
    windspeed = df['windspeed'].mean()
    return {
        'temp': round(temp),
        'atemp': round(atemp),
        'hum': round(humidity),
        'windspeed': round(windspeed)
    }


# Styling Dashboard
st.title('Dashboard Bike Sharing Dataset:bike:')

min_date = pd.to_datetime(main_df['dteday'].min())
max_date = pd.to_datetime(main_df['dteday'].max())

with st.sidebar: # Create sidebar
    st.image("../img.jpeg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )
    
    df = main_df[(main_df['dteday'] >= str(start_date)) & (main_df['dteday'] <= str(end_date))]

average = get_avg_metrics(df)  # Get average metrics element


st.subheader('Kondisi Lingkungan & jumlah total penyewaan sepeda')
col1, col2, col3, col4, col5 = st.columns(5)

with col1: # Metric show average temp in a period
    temp = average['temp']
    st.metric(label='Temperature', value=f"{temp} °C")
    st.markdown('AVG')

with col2: # Metric show average apparent temp in a period
    atemp = average['atemp']
    st.metric(label='A.Temperature', value=f"{atemp} °C")
    st.markdown('AVG')


with col3: # Metric show average humidity in a period
    hum = average['hum']
    st.metric(label='Humidity', value=f"{hum}%")
    st.markdown('AVG')

with col4: # Metric show average windspeed in a period
    wind = average['windspeed']
    st.metric(label='Windspeed', value=f"{wind} m/s")
    st.markdown('AVG')

with col5: # Metric show total of bike shared in a period
    total = main_df['cnt'].sum()
    st.metric(label='Total rented', value=total)
    st.markdown('SUM')



st.subheader(f"Grafik penyewaan sepeda dalam sebuah periode")
fig, ax = plt.subplots(figsize=(20, 15))

ax.plot(df['dteday'], df['cnt'], color='darkblue', marker='s')
ax.set_title(f'Total penyewaan dalam periode {start_date} hingga {end_date}', loc='center', fontsize=20)
ax.set_xlabel('Tanggal', fontsize= 10)
ax.set_ylabel('Total', fontsize= 10)
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)


st.subheader(f"Perbandingan jumlah penyewaan user casual dan user registered setiap bulan")

df_bymonth = df.groupby(by=['mnth','yr']).agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
}).reset_index()

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20, 8))

month_name = ['jan', 'feb', 'mar', 'apr', 'may' ,'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

# User casual tahun pertama
ax[0, 0].bar(df_bymonth[df_bymonth['yr'] == 0]['mnth'], df_bymonth[df_bymonth['yr'] == 0]['casual'], color='darkblue')
ax[0, 0].set_title('Jumlah penyewaan sepeda berdasarkan bulan user casual', loc='center')
ax[0, 0].set_xlabel('Bulan', fontsize=10)
ax[0, 0].set_ylabel('Jumlah total perbulan',fontsize=10)
ax[0, 0].set_xticks(range(1, 13))
ax[0, 0].set_xticklabels(month_name)
ax[0, 0].legend(loc='upper right')
ax[0, 0].tick_params(axis = 'y', labelsize=12)

# User registered tahun pertama
ax[0, 1].bar(df_bymonth[df_bymonth['yr'] == 0]['mnth'], df_bymonth[df_bymonth['yr'] == 0]['registered'], color='darkgreen')
ax[0, 1].set_title('Jumlah penyewaan sepeda berdasarkan bulan user registered', loc='center')
ax[0, 1].set_xlabel('Bulan', fontsize=10)
ax[0, 1].set_ylabel('Jumlah total perbulan', fontsize=10)
ax[0, 1].set_xticks(range(1, 13))
ax[0, 1].set_xticklabels(month_name)
ax[0, 1].legend(loc='upper right')
ax[0, 1].tick_params(axis = 'y', labelsize=12)

# User casual tahun kedua
ax[1, 0].bar(df_bymonth[df_bymonth['yr'] == 1]['mnth'], df_bymonth[df_bymonth['yr'] == 1]['casual'], color='darkblue')
ax[1, 0].set_title('Jumlah penyewaan sepeda berdasarkan bulan user casual', loc='center')
ax[1, 0].set_xlabel('Bulan', fontsize=10)
ax[1, 0].set_ylabel('Jumlah total perbulan', fontsize=10)
ax[1, 0].set_xticks(range(1, 13))
ax[1, 0].set_xticklabels(month_name)
ax[1, 0].legend(loc='upper right')
ax[1, 0].tick_params(axis = 'y', labelsize=12)

# User registered tahun kedua
ax[1, 1].bar(df_bymonth[df_bymonth['yr'] == 1]['mnth'], df_bymonth[df_bymonth['yr'] == 1]['registered'], color='darkgreen')
ax[1, 1].set_title('Jumlah penyewaan sepeda berdasarkan bulan user casual', loc='center')
ax[1, 1].set_xlabel('Bulan', fontsize=10)
ax[1, 1].set_ylabel('Jumlah total perbulan', fontsize=10)
ax[1, 1].set_xticks(range(1, 13))
ax[1, 1].set_xticklabels(month_name)
ax[1, 1].legend(loc='upper right')
ax[1, 1].tick_params(axis = 'y', labelsize=12)

plt.subplots_adjust(hspace=0.5, wspace=0.5)

plt.suptitle('Perbandingan jumlah penyewaan sepeda user casual dan registered berdasarkan bulan', fontsize=20)
st.pyplot(fig)

metric1, metric2 = st.columns(2)

with metric1: # Metric show total of casual user rented
    casual = df['casual'].sum()
    st.metric('Casual Total', value=casual)
    st.markdown('SUM')

with metric2: # Metric show total of registered user rented
    registered = df['registered'].sum()
    st.metric('Registered Total', value=registered)
    st.markdown('SUM')

st.subheader('Waktu penyewaan sepeda')

category1, category2, category3, category4 = st.columns(4)

with category1: # sum of total rented in the morning
    morning = time_df[time_df['time_category'] == 'Morning']['cnt'].sum()
    st.metric('Morning', value=morning)
    st.markdown('SUM')

with category2: # sum of total rented in the day 
    day = time_df[time_df['time_category'] == 'Day']['cnt'].sum()
    st.metric('Day', value=day)
    st.markdown('SUM')

with category3: # sum of total rented in the afternoon
    afternoon = time_df[time_df['time_category'] == 'Afternoon']['cnt'].sum()
    st.metric('Afternoon', value=afternoon)
    st.markdown('SUM')

with category4: # sum of total rented in the night
    night = time_df[time_df['time_category'] == 'Night']['cnt'].sum()
    st.metric('night', value=night)
    st.markdown('SUM')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 9))

# tahun pertama
ax[0].bar(time_df[time_df['yr'] == 0]['time_category'], time_df[time_df['yr'] == 0 ]['cnt'], color='skyblue')
ax[0].set_title('Jumlah penyewaan sepeda berdasarkan waktu tahun pertama')
ax[0].set_xlabel('waktu')
ax[0].set_ylabel('Total penyewaan tiap waktu')
ax[0].tick_params(axis='y', labelsize=12)

# tahun kedua
ax[1].bar(time_df[time_df['yr'] == 1]['time_category'], time_df[time_df['yr'] == 1 ]['cnt'], color='lightgreen')
ax[1].set_title('Jumlah penyewaan sepeda berdasarkan waktu tahun kedua')
ax[1].set_xlabel('waktu')
ax[1].set_ylabel('Total penyewaan tiap waktu')
ax[1].tick_params(axis='y', labelsize=12)

plt.suptitle('Jumlah peminjam sepeda berdasarkan kategori waktu', fontsize=15)
st.pyplot(fig)

st.caption('Copyright (c) 2025')