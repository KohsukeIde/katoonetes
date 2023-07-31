import pandas as pd
import numpy as np

def process_csv_file(file_path):
    # Read data
    df = pd.read_csv(file_path)

    # Normalize data
    df_centered = df - df.mean()
    df_normalized = df_centered / df_centered.std()

    # Save mean and standard deviation
    output_file_mean = 'mean.csv'
    output_file_std = 'std.csv'
    df.mean().to_csv(output_file_mean, index=False)
    df.std().to_csv(output_file_std, index=False)

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

    # Save as CSV file
    # For learning data
    output_file = 'poses3d_fixed.csv'
    df_interpolated.to_csv(output_file, index=False)

    # For visualization
    # output_file = 'poses3d_fixed_inversed.csv'
    # df_inv_normalized.to_csv(output_file, index=False)

process_csv_file('/content/drive/MyDrive/dev/Research/ide/front-right/yourfile.csv')
