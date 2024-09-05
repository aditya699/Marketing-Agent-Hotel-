import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Create 50 rows of random data for Campaign Run Timings (in hours), Likes, and Dislikes
data = {
    'Campaign_Run_Timings': np.random.randint(1, 24, 50),  # Random timings between 1 to 24 hours
    'Likes': np.random.randint(50, 500, 50),               # Random likes between 50 and 500
    'Dislikes': np.random.randint(0, 50, 50)               # Random dislikes between 0 and 50
}

# Create DataFrame
df = pd.DataFrame(data)

df.to_csv("../Staging/prev_campaign.csv",index=False)
