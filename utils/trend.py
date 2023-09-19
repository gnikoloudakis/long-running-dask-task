import numpy as np
from scipy import stats

# Define your data
time = [1, 2, 3, 4, 5]  # Time observations
execution_time = [10, 8, 6, 4, 2]  # Mean execution time observations

# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(time, execution_time)

# Interpret the results
if slope > 0 and p_value < 0.05:
    trend = "increasing"
elif slope < 0 and p_value < 0.05:
    trend = "decreasing"
else:
    trend = "no significant trend"

# Print the results
print("Slope:", slope)
print("P-value:", p_value)
print("Trend:", trend)
