import json
import pandas as pd
import plotly.express as px
import plotly   
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"  # Setzt den Renderer auf Browser, um die Plots anzuzeigen

# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms'])
        start_time = self.df['Zeit in ms'].iloc[0]
    
        # Zeitwerte so verschieben, dass der erste Zeitwert 0 ist
        self.df['Zeit in ms'] = self.df['Zeit in ms'] - start_time
    
        print(self.df.head())


    def plot_time_series(self):
        fig = go.Figure()
    
        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit auf der x-Achse
        fig.add_trace(go.Scatter(x=self.df["Zeit in ms"], y=self.df["Messwerte in mV"], mode='lines', name='EKG Messwerte'))

        peaks = self.find_peaks()
        filtered_peaks = [i for i in peaks if self.df["Zeit in ms"].iloc[i] <= 5000]
        
        fig.add_trace(go.Scatter(
            x=self.df["Zeit in ms"].iloc[filtered_peaks],
            y=self.df["Messwerte in mV"].iloc[filtered_peaks],
            mode='markers',
            name='Peaks',
            marker=dict(color='red', size=5)
        ))
        fig.update_layout(
            title=f"EKG Messwerte für ID {self.id}",
            xaxis_title="Zeit in ms",
            yaxis_title="Messwerte in mV",
            xaxis=dict(range=[0, 5000]),  # Setzt die x-Achse auf 0 bis 5000 ms
        )
        return fig

    @staticmethod
    def load_by_id(id):
        """Lädt die EKG-Daten für eine bestimmte ID"""
        with open("data/person_db.json") as file:
            ekg_list=json.load(file)
        
        for eintrag in ekg_list:
            if eintrag["id"] == id:
                return EKGdata(eintrag)
        
        return None


    def find_peaks(self, threshold=None, window_size=3):
        series = self.df["Messwerte in mV"]
    
        # Glätten mit moderner Methode
        smooth = series.rolling(window=window_size*2+1, center=True).mean().bfill().ffill()

        if threshold is None:
            threshold = smooth.quantile(0.95)

        peaks = []

        for i in range(window_size, len(smooth) - window_size):
            window = smooth.iloc[i - window_size:i + window_size + 1]
            center_value = smooth.iloc[i]

            if center_value == window.max() and center_value > threshold:
                if len(peaks) == 0 or i - peaks[-1] > window_size:
                    peaks.append(i)

        return peaks

    def estimate_hr(self, threshold=None, window_size=3):
        peaks = self.find_peaks(threshold, window_size)
        if not peaks:
            return 0

        # Zeitstempel der Peaks
        peak_times = self.df["Zeit in ms"].iloc[peaks].values

        if len(peak_times) < 2:
            return 0

        # Zeitdifferenzen in ms
        intervals = [peak_times[i] - peak_times[i - 1] for i in range(1, len(peak_times))]
        if not intervals:
            return 0

        avg_interval = sum(intervals) / len(intervals)
        hr = 60000 / avg_interval
        return hr



if __name__ == "__main__":
    
    with open("data/person_db.json") as file:
        person_data = json.load(file)
        
    ekg_dict = person_data[0]["ekg_tests"][0]
    ekg = EKGdata(ekg_dict)

    # Plot der Zeitreihe
    fig = ekg.plot_time_series()
    fig.show()

    # Herzfrequenz
    hr = ekg.estimate_hr()
    print(f"Estimated Heart Rate: {hr:.2f} bpm")



   