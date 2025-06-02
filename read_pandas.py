# %%

# Paket für Bearbeitung von Tabellen
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default = "browser"  # Plotly in Browser anzeigen


# Paket
## zuvor !pip install plotly
## ggf. auch !pip install nbformat
import plotly.express as px


def read_my_csv():
    # Einlesen eines Dataframes
    ## "," steht für das Trennzeichen in der csv-Datei (Tabulator anstelle von Beistrich)
    ## header = None: es gibt keine Überschriften 
    df= pd.read_csv("data/activities/activity.csv")

    time= np.arange(0, len(df))  # Zeit in s
    df["time"] = time  # Zeit in s wird als neue Spalte hinzugefügt 

    # Gibt den geladen Dataframe zurück
    return df

def heart_rate_zone(df, max_hr):
    # Funktion, die die Herzfrequenzzonen berechnet
    # Die Zonen sind in der Regel:
    zones = {
        "Zone 1": [0.50 * max_hr, 0.60 * max_hr],
        "Zone 2": [0.60 * max_hr, 0.70 * max_hr],
        "Zone 3": [0.70 * max_hr, 0.80 * max_hr],
        "Zone 4": [0.80 * max_hr, 0.90 * max_hr],
        "Zone 5": [0.90 * max_hr, max_hr]
    }

    def assign_zone(hr):
        for zone, (lower, upper) in zones.items():
            if lower <= hr < upper:
                return zone
    
    df['HeartRateZone'] = df['HeartRate'].apply(assign_zone)
    return df, zones
        

def make_plot(df,zones):
    # Farben zuweisen
    zone_colors = {
        "Zone 1": "blue",
        "Zone 2": "green",
        "Zone 3": "purple",
        "Zone 4": "orange",
        "Zone 5": "red"
    }
    fig = go.Figure()

    #Power Original hinzufügen
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['PowerOriginal'],
        mode='lines',
        name='Power Original',
        line=dict(color='grey', width=1.5)
    ))  

    # Herzfrequenzzonen farbig hinzufügen
    for zone in df['HeartRateZone'].dropna().unique():
        df_zone= df.copy()
        df_zone['HeartRateMasked'] = df_zone.apply(
            lambda row: row['HeartRate'] if row['HeartRateZone'] == zone else np.nan, axis=1
        )

        fig.add_trace(go.Scatter(
            x=df_zone['time'],
            y=df_zone['HeartRateMasked'],
            mode='lines',
            name=f"Heart Rate {zone}",  
            line=dict(color=zone_colors.get(zone, 'gray'), width=2)
        ))
    
    
    for zone_name, (lower, upper) in zones.items():
        fig.add_shape(
            type='line',
            x0=df['time'].min(), x1=df['time'].max(),
            y0=lower, y1=lower,
            line=dict(color= 'gray',width=1, dash='dot'),
        )

        fig.add_shape(
            type='line',
            x0=df['time'].min(), x1=df['time'].max(),
            y0=upper, y1=upper,  
            line=dict(color='gray',width=1, dash='dot'),
        )   
    fig.update_layout(
        title='Heart Rate and Power Over Time',
        xaxis_title='Time (s)',
        yaxis_title='Heart Rate / Power',
        template='plotly_white'
    )
    x_text = df['time'].max() + 5  # Etwas rechts vom Plotbereich
    for zone_name, (lower, upper) in zones.items():
        y_middle = (lower + upper) / 2  # Vertikale Mitte der Zone
        fig.add_annotation(
            x=x_text,
            y=y_middle,
            text=zone_name,
            showarrow=False,
            font=dict(color=zone_colors[zone_name], size=12),
            align="left"
        )
    return fig

def max_mean_power(df):
    # Funktion, die den maximalen und mittleren Powerwert berechnet
    max_power = df["PowerOriginal"].max()
    mean_power = df["PowerOriginal"].mean()
    
    return max_power, mean_power


    
if __name__ == "__main__":
    # Wenn das Skript direkt ausgeführt wird, wird der Plot generiert
    df = read_my_csv()
    df, zones = heart_rate_zone(df, max_hr)  # Beispiel mit max Herzfrequenz 199
    fig_activity = make_plot(df,zones)
    fig_activity.show()  # Zeigt den Plot im Browser an
    
   

   








 
# %%
