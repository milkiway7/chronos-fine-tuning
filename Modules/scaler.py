from sklearn.preprocessing import StandardScaler
import pandas as pd
import os
import pickle
from constants import CONSTANTS_GLOBAL

class Scaler():
    def __init__ (self, df: pd.DataFrame):
        self.df = df
        self.scalers = {}
        self.scaled_df = None
        self.scalers_path = f"scalers/"
        self.scaled_data_path = f"scaled_data/"
        os.makedirs(self.scalers_path, exist_ok=True)
        os.makedirs(self.scaled_data_path, exist_ok=True)
    
    def scale(self):
        interval = self.df.iloc[0]["Interval"]

        for symbol in CONSTANTS_GLOBAL["symbol"]:
            # crete df with only the symbol
            df_symbol = self.df[self.df["Symbol"] == symbol].copy()
            # get columns to scale
            columns_not_to_scale = ["Symbol", "Interval","CloseTime"]
            columns_to_scale = [col for col in df_symbol.columns if col not in columns_not_to_scale]
            # create scaler and scale data
            scaler = StandardScaler()
            #tu już mam dane skalowane ale jeszcze nie zapisane to tak jakby gotowe danie
            df_symbol[columns_to_scale] = scaler.fit_transform(df_symbol[columns_to_scale])
            self.scaled_df = df_symbol
            # tu zapisuje scaler do pliku który jest przepisem na to danie potrzebuję tego aby potem odtworzyć to danie
            with open(f"{self.scalers_path}/{symbol}_{interval}.pkl", "wb") as f:
                pickle.dump(scaler, f)
            #zapisz skalowane dane do pliku grupując po interwale i symbolu
            self.scaled_df.to_parquet(f"{self.scaled_data_path}/{symbol}_{interval}.paruquet")
            print(f"{self.scaled_df.head()}")
            print(f"{len(self.scaled_df)}")



            



