import pandas as pd
import matplotlib.pyplot as plt

# Les Excel-filen (sett riktig filbane til din Excel-fil)
df = pd.read_excel('C:/Users/ametta/Downloads/Datasett_1_Nordpool_forbruksdata_Norge.xlsx')

# Sjekk DataFrame for å sikre at det ble lastet riktig
# print(df.head())

# Konverter 'Dato' kolonnen til datetime (for eksempel '01-01-2013')
df['Dato'] = pd.to_datetime(df['Dato'], format='%d-%m-%Y')

# Rydd opp i 'Hours' kolonnen for å fjerne eventuelle ekstra tegn (som mellomrom rundt bindestreken)
df['Hours'] = df['Hours'].str.replace(' - ', ' - ', regex=False)  # Rydde opp bindestreken (fjerne ekstra tegn)

# Lag en datetime-kolonne ved å kombinere datoen med starten av timeintervallet
df['Start_Hour'] = df['Hours'].str.split(' - ').str[0]

# Lag en datetime-kolonne som kombinerer 'Dato' og 'Start_Hour'
df['Datetime'] = pd.to_datetime(df['Dato'].astype(str) + ' ' + df['Start_Hour'], format='%Y-%m-%d %H')

drop_col = ['Start_Hour', 'Hours', 'Dato', 'Unnamed: 0']

for col in drop_col:
    if col in df.columns:
        df = df.drop(col, axis=1)

df['hour'] = df['Datetime'].dt.hour
df = df.drop('Datetime', axis=1)
aggregated_df = df.groupby('hour').mean()

# Plotting
plt.figure(figsize=(12, 6))
# Plot alle NOx-kolonnene per time
for col in ['NO1', 'NO2', 'NO3', 'NO4', 'NO5']:
    plt.plot(aggregated_df.index, aggregated_df[col], marker='o', label=col)

# Legge til tittel og etiketter
#plt.title('Gjennomsnittlig strømforbruk i MWh per time (periode 2013-2021 i prisområdene (NO1-NO5)).', fontsize=14)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Gjennomsnittlig strømforbruk i MWh per time', fontsize=12)

# Vise legend
plt.legend(title='Prisområder')

# Rotere x-aksen etiketter for bedre lesbarhet
plt.xticks(rotation=45)
plt.xticks(range(24))  # Vis alle timer fra 0 til 23

# Vise plottet
plt.tight_layout()
plt.show()
