from chronos import ChronosModel, ChronosPipeline
import pandas as pd
import numpy as np
import torch

local_model_path = "C:/Users/alexm/.cache/huggingface/hub/models--amazon--chronos-t5-small/snapshots/6bcab32367f856115ca07bdd7f4956eced00a4b5"

# Załaduj model z lokalnej ścieżki
pipeline = ChronosPipeline.from_pretrained(
    local_model_path,
    device_map="cpu",  # Możesz zmienić na "cuda" jeśli masz GPU
    torch_dtype=torch.float32,
)

# Przykładowe dane (syntetyczne)
context = torch.tensor([100, 120, 130, 150, 170, 190, 210], dtype=torch.float32)

# Wykonanie predykcji
prediction_length = 5
forecast = pipeline.predict(context, prediction_length)

# Wyświetlenie prognozy
print("Prognoza:", forecast)    