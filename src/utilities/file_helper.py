import cdflib
import pandas as pd

def read_cdf(filepath):
    """
    Load GRACE density CDF file as DataFrame.

    Columns:
        time              - UTC timestamp
        altitude_m        - Satellite altitude in meters
        longitude         - Degrees (-180 to 180)
        latitude          - Degrees (-90 to 90)
        local_solar_time  - Hours (0-24)
        density_kg_m3     - Thermospheric density in kg/m³
        density_orbitmean - Orbit-averaged density
        validity_flag     - 1=valid, 0=invalid
        validity_flag_orbitmean - 1=valid, 0=invalid

    Args:
        filepath: Path to CDF file
        valid_only: If True, filter to validity_flag==1. Set False for files with all invalid flags.
    """
    cdf = cdflib.CDF(filepath)

    df = pd.DataFrame({
        'time': cdflib.cdfepoch.to_datetime(cdf.varget('time')),
        'altitude_m': cdf.varget('altitude'),
        'longitude': cdf.varget('longitude'),
        'latitude': cdf.varget('latitude'),
        'local_solar_time': cdf.varget('local_solar_time'),
        'density_kg_m3': cdf.varget('density'),
        'density_orbitmean': cdf.varget('density_orbitmean'),
        'validity_flag': cdf.varget('validity_flag'),
        'validity_flag_orbitmean': cdf.varget('validity_flag_orbitmean')
    })

    return df

def read_f107_file(filepath,skiprows=40):
    # Expected column names from GFZ text file
    custom_column_names = ['Year', 'Month', 'Day', 'days', 'days_m', 'Bsr', 'dB', 'kp1', 'kp2', 'kp3', 'kp4', 'kp5',
                           'kp6', 'kp7', 'kp8', 'ap1', 'ap2', 'ap3', 'ap4', 'ap5', 'ap6', 'ap7', 'ap8', 'Ap', 'SN',
                           'F10.7obs', 'F10.7adj', 'D']
    # Read file as dataframe
    df = pd.read_csv(filepath,
                     sep='\s+',  # Use one or more whitespace as the delimiter
                     skiprows=skiprows,  # Skip the first N (3) lines of the file
                     names=custom_column_names,  # Assign custom column names
                     )

    return df