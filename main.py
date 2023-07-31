from fastapi import FastAPI, UploadFile, File
import pandas as pd
import numpy as np
from io import StringIO

app = FastAPI()

@app.post("/uploadcsv/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    s = str(content, 'utf-8')
    data = StringIO(s) 
    df = pd.read_csv(data)

    # Normalize data
    df_centered = df - df.mean()
    df_normalized = df_centered / df_centered.std()

    # Repair outliers
    for col in df_normalized.columns:
        bool_outliers = np.abs(df_normalized[col] - df_normalized[col].mean()) > 3*df_normalized[col].std()
        df_normalized.loc[bool_outliers, col] = np.nan

    # Interpolate
    df_interpolated = df_normalized.interpolate(method='linear', limit_direction='both')

    # If there are still null values, interpolate again
    if df_interpolated.isnull().sum().sum() > 0:
        df_interpolated = df_interpolated.interpolate(method='linear', limit_direction='both')

    # Inverse normalization (for visualization purposes)
    df_inv_normalized = df_interpolated * df_centered.std() + df.mean()

    # Convert the processed dataframe to csv
    result = df_inv_normalized.to_csv(index=False)
    
    return {"filename": file.filename, "processed_file": result}
