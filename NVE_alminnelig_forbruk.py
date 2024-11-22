import pandas as pd
import matplotlib.pyplot as plt

# Les Excel-filen (sett riktig filbane til din Excel-fil)
df = pd.read_excel('/Datasett_1_Nordpool_forbruksdata_Norge.xlsx')


# Konverter 'Dato' kolonnen til datetime (for eksempel '01-01-2013')
df['Dato'] = pd.to_datetime(df['Dato'], format='%d-%m-%Y')

# Rydd opp i 'Hours' kolonnen for å fjerne eventuelle ekstra tegn (som mellomrom rundt bindestreken)
df['Hours'] = df['Hours'].str.replace(' - ', ' - ', regex=False)  # Rydde opp bindestreken (fjerne ekstra tegn)

# Lag en datetime-kolonne ved å kombinere datoen med starten av timeintervallet
df['Start_Hour'] = df['Hours'].str.split(' - ').str[0]

# Lag en datetime-kolonne som kombinerer 'Dato' og 'Start_Hour'
df['Datetime'] = pd.to_datetime(df['Dato'].astype(str) + ' ' + df['Start_Hour'], format='%Y-%m-%d %H')

#Droppe kolonner vi ikke trenger
drop_col = ['Start_Hour', 'Hours', 'Dato', 'Unnamed: 0']
for col in drop_col:
    if col in df.columns:
        df = df.drop(col, axis=1)


df = df.set_index('Datetime')

#aggregated_df = df.resample("ME").mean() #Aggregere per måned
aggregated_df = df.resample("YS").mean() #Aggregere per år

#aggregated_df = df

# Plotting
plt.figure(figsize=(12, 6))

# Filtrer for en spesifikk måned og år (for eksempel januar 2013)
# month = 1
aggregate_df = aggregated_df  # & (df['Datetime'].dt.month == month)# # ]

# Plot alle NOx-kolonnene per time
for col in ['NO1', 'NO2', 'NO3', 'NO4', 'NO5']:
    plt.plot(aggregate_df.index, aggregate_df[col], marker='o', label=col)


# Legge til tittel og etiketter
#plt.title('Gjennomsnittlig årlig strømforbruk i MWh for periode 2013-2021 i prisområdene (NO1-NO5).', fontsize=14)
plt.xlabel('År', fontsize=12)
plt.ylabel('Gjennomsnittlig strømforbruk i MWh per år', fontsize=12)

# Vise legend
plt.legend(title='Prisområder')

# Rotere x-aksen etiketter for bedre lesbarhet
plt.xticks(rotation=45)
# Vise plottet
plt.tight_layout()
plt.show()
