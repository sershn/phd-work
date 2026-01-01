import pandas as pd

# Load the data into a DataFrame
data = pd.read_csv('data3.csv')

# Group by 'total_$' and calculate the mean of the 'tw' columns
averaged_data = data.groupby('total_$', as_index=False).agg({
    'total_t': 'first',
    'tw0': 'mean',
    'tw1': 'mean',
    'tw3': 'mean',
    'tw4': 'mean'
})

# Save the new DataFrame to a CSV file (optional)
averaged_data.to_csv('averaged_data1.csv', index=False)

# Display the new DataFrame
print(averaged_data)