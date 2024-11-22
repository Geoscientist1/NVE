import pandas as pd
import matplotlib.pyplot as plt

from NVE_alminnelig_forbruk import aggregated_df, aggregate_df

# Les Excel-filen (sett riktig filbane til din Excel-fil)
df = pd.read_excel('C:/Users/moham/Downloads/Datasett_2_SSB_kraftintensiv_industri_Norge.xlsx')

df['År'] = df['Dato'].str[:4]
df['Måned'] = df['Dato'].str[5:]

# Lag en datokolonne
df['Dato'] = pd.to_datetime(df['År'] + '-' + df['Måned'], format='%Y-%m')


df = df.drop(columns=['År', 'Måned'])

# Sjekk DataFrame for å sikre at det ble lastet riktig
print(df.head(10))

plt.figure(figsize=(12, 6))

# Filtrer for en spesifikk måned og år (for eksempel januar 2013)
# month = 1


df = df.set_index('Dato')
aggregated_df = df.resample("ME").mean()  #aggregere per måned
#aggregated_df = df.resample("YS").mean() #aggregere per år
aggregate_df=aggregated_df
print(aggregate_df.head(5))
# Plot alle NOx-kolonnene per time
for col in ['NO1', 'NO2', 'NO3', 'NO4', 'NO5']:
    plt.plot(aggregate_df.index, aggregate_df[col], marker='o', label=col)

# Legge til tittel og etiketter
#plt.title('Gjennomsnittlig årlig kraftintensivt forbruk i Norge i MWh for periode 2013-2021 i prisområdene (NO1-NO5).', fontsize=14)
plt.xlabel('År', fontsize=12)
plt.ylabel('Gjennomsnittlig kraftintensivt forbruk i MWh per måned', fontsize=12)

# Vise legend
plt.legend(title='Prisområder')

# Rotere x-aksen etiketter for bedre lesbarhet
plt.xticks(rotation=45)

# Vise plottet
plt.tight_layout()
plt.show()
