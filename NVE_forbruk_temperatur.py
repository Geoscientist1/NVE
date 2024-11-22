# -*- coding: utf-8 -*-
import time
import os
import warnings

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
matplotlib.use('TkAgg')

def render_nve_plot(aggregation: str, harmonize_data=True):
    """
    method for rendering multiple plots based on data from NVE

    Parameters
    ----------
    aggregation               : str
                                aggregation level, possible values include

                                'D': Daily
                                'B': Business day (Monday through Friday)
                                'W': Weekly (defaulting to Sunday)
                                'M': Month end
                                'MS': Month start
                                'Q': Quarter end
                                'QS': Quarter start
                                'A' or 'Y': Year end
                                'AS' or 'YS': Year start
                                'H': Hourly
                                'T' or 'min': Minute-based frequency
                                'S': Second-based frequency
                                'L': Millisecond-based frequency
                                'U': Microsecond-based frequency
                                'N': Nanosecond-based frequency
                                'BH': Business hour frequency (from 9 AM to 5 PM, Monday through Friday)
                                'W-MON', 'W-TUE', etc.: Weekly frequency with custom week start days
                                'BM': Business month end (the last business day of the month)
                                'BMS': Business month start (the first business day of the month)
                                'BA': Business year end (the last business day of the year)
                                'BAS': Business year start (the first business day of the year)

    harmonize_data            : bool
                                flag to insure harmonized data, i.e. same number of
                                rows in all internal dfs


    """
    start = time.time()

    data_dir = os.path.dirname(__file__) + '/data/'
    data_dfs = {}

    for i, file in enumerate(os.listdir(data_dir)):
        if i == 1:
            continue
        dataset_name = file.replace(' ', '_').replace('.xlsx', '').lower()

        df = pd.read_excel(data_dir + file)
        print(f"finished reading data from file '{file}' (elapsed time : {time.time() - start})")

        for col in df.columns.tolist():
            if 'Unnamed' in col:
                df = df.drop(col, axis=1)

        if 'timestamp' not in df.columns and all(
                col for col in df.columns.tolist() if col in ['Dato', 'Hours']):
            df['timestamp'] = pd.to_datetime(df['Dato'] + ' ' + df['Hours'],
                                             format='%d-%m-%Y %H - %M')
            df = df.drop(columns=['Dato', 'Hours'])
            df = df[['timestamp', 'NO1', 'NO2', 'NO3', 'NO4', 'NO5']]
        else:
            df['timestamp'] = pd.to_datetime(df['timestamp'])

        df.set_index('timestamp', inplace=True)
        df = df.resample(aggregation).mean()

        data_dfs.update({dataset_name: df})

        print(f"finished parsing data for '{dataset_name}' (elapsed time : {time.time() - start})")

    consumption_data = data_dfs['datasett_1_nordpool_forbruksdata_norge']
    consumption_colors = ['r', 'g', 'b', 'orange', 'purple']

    temperature_data = data_dfs['datasett_3_met_temperatur_norge']
    temperature_colors = ['c', 'm', 'y', 'b', 'k']

    if harmonize_data:
        temperature_data = temperature_data[temperature_data.index.isin(consumption_data.index)]

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for i, col in enumerate(consumption_data.columns):
        ax = axes[i]
        ax.plot(consumption_data.index, consumption_data[col], linestyle='-',
                color=consumption_colors[i], label=f"{col} Consumption")
        ax2 = ax.twinx()
        ax2.plot(temperature_data.index, temperature_data[col], linestyle='--',
                 color=temperature_colors[i], label=f'{col} Temperature')

        ax.set_title(col)
        ax.set_xlabel('År')
        ax.set_ylabel('MWh per måned')
        ax2.set_ylabel('Temperatur (C)')
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')

    fig.delaxes(axes[5])
    plt.tight_layout()

    print(f"finished rendering plots, elapsed time : {time.time() - start}")

    plt.show()


if __name__ == "__main__":
    render_nve_plot('M')
