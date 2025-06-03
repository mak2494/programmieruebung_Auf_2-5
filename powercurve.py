# Pakete für Ausführung
import pandas as pd
import numpy as np
import plotly.graph_objects as go

## zuvor !pip install plotly
## ggf. auch !pip install nbformat
import plotly.express as px

from read_pandas import read_my_csv 

def load_power_curve_data():
    """A Function that knows where the power curve database is and returns a DataFrame with the power curve data"""
    df = read_my_csv()
    return df

df = load_power_curve_data()

#window size in sekunden als array 
window_size = [1,2,5,10,20,30,60, 120, 300, 600, 1200, 1800, 3600, 7200]
series=df['PowerOriginal']

def find_best_effort(series, window_size):
    return series.rolling(window=window_size, min_periods=window_size).mean().max()

# Funktion 2: Erstelle das Power Curve DataFrame
def create_powercurve_data(series, window_sizes):
    best_efforts = []

    for w in window_sizes:
        best_power = find_best_effort(series, w)
        best_efforts.append({
            'Window Size in seconds': w,
            'Best Average Power': best_power
        })

    return pd.DataFrame(best_efforts)



tick_labels = [
    "1s", "2s", "5s", "10s", "20s", "30s", 
    "1min", "2min", "5min", "10min", "20min", "30min", 
    "1h", "2h"
]

def create_powercurve_plot():
    powercurve_df = create_powercurve_data(series, window_size)
    figure = go.Figure()

    figure.add_trace(go.Scatter(
        x=powercurve_df['Window Size in seconds'],
        y=powercurve_df['Best Average Power'],
        mode='lines+markers', 
        fill='tozeroy',#füllt unter Linie
        fillcolor='rgba(128, 0, 128, 0.2)',
        line=dict(color='purple', width=2),
        marker=dict(size=6, color='purple'),
        name='Power Curve'
    ))

    figure.update_layout(
        title= dict(
            text='Power Curve',
            font=dict(size=24, color='Purple'),
            x=0.5,  # Zentriert den Titel
            y=0.95  # Position des Titels,
        ),
        xaxis=dict(
            type='log',
            title=dict(
                text='Time',
                font=dict(size=18, color='Purple'),
            ),
            tickmode='array',
            tickvals=(window_size),
            ticktext=tick_labels,
            showgrid=True,
            gridcolor='LightGray',
            gridwidth=1,
        ),
        yaxis= dict(
            title=dict(
                text='Power (W)',
                font=dict(size=18, color='Purple'),
            ),
            showgrid=True,
            gridcolor='LightGray',
            gridwidth=1),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )

    return figure

power_curve = create_powercurve_plot()
power_curve.write_image('data/power_curve.png')  # Speichert den Plot als PNG-Datei

