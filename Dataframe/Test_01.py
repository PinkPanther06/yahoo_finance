import pandas as pd
import yfinance as yfin
import datetime as dt

#test

# Start- und Enddatum festlegen
start = dt.datetime.now() - dt.timedelta(days=365)
end = dt.datetime.now()

# CSV-Datei mit den Symbolen einlesen
file = '2'
symbols_df_1 = pd.read_csv(f'{file}_Symbols.csv')
symbols_to_compare_1 = symbols_df_1['Symbol'].tolist()

# Daten für jedes Symbol abrufen und verarbeiten
for ticker in symbols_to_compare_1:
    try:
        # Daten herunterladen
        df = yfin.download(ticker, start, end, interval='1d', auto_adjust=False, progress=False)

        # Überprüfen, ob der DataFrame nicht leer ist
        if not df.empty:
            # Spaltennamen anpassen, um die zweite Ebene des MultiIndex zu entfernen
            df.columns = df.columns.get_level_values(0)

            # Nachkommastellen auf 2 Stellen runden
            df['Close'] = df['Close'].round(2)
            df['Open'] = df['Open'].round(2)
            df['High'] = df['High'].round(2)

            # -------------------------------------------------------------------------------------------------

            from ta.momentum import StochasticOscillator

            indicator_stoch = StochasticOscillator(high=df["High"], low=df["Low"], close=df["Close"], window=10,
                                                   smooth_window=3)
            df["stoch"] = round(indicator_stoch.stoch(), 2)
            # Berechnung der 10 niedrigsten STOCH-Werte (stoch)
            # Sortiere den DataFrame nach den niedrigsten RSI-Werten
            df_sorted_stoch = df.nsmallest(10, 'stoch')  # Wählt die 10 niedrigsten RSI5-Werte
            # Markiere die niedrigsten RSI5-Werte im Original-DataFrame
            df['Lowest_stoch'] = df['stoch'].apply(lambda x: x if x in df_sorted_stoch['stoch'].values else None)
            df['StoLow'] = df['Lowest_stoch'].min()
            df['StoMax'] = df['Lowest_stoch'].max()
            df['SigSto'] = (df['stoch'] < df['StoMax']).astype(int)

            # -------------------------------------------------------------------------------------------------

            # Ausgabe des DataFrames
            print(df.head())
        else:
            print(f"Keine Daten für {ticker} im angegebenen Zeitraum.")
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten für {ticker}: {e}")
