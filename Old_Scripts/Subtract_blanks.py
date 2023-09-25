import pandas as pd

# Load CSV files into dataframes
data = pd.read_csv("/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/averaged_output.csv", index_col=0)  # Assuming 'Well' is the index

print (data)
# Get unique conditions
unique_conditions = data['Condition'].unique()

# Create an empty DataFrame to store the corrected values
corrected_data = pd.DataFrame()

for condition in unique_conditions:
    # Filter rows for the current condition
    condition_data = data[data['Condition'] == condition].copy()
    
    # Find the blank row for the condition
    blank_row = condition_data[condition_data['Microbe_Type'] == 'Blank'].iloc[0]
    
    # Subtract the values in the blank row from all the other rows of the same condition
    for column in condition_data.columns[2:]:
        condition_data[column] = condition_data[column] - blank_row[column]
    
    # Append the corrected rows to the corrected_data
    corrected_data = pd.concat([corrected_data, condition_data], ignore_index=True)


# Iterate through the columns starting from the 3rd column (0-indexed). 
# Subtract time 0 from other times to normalize starting OD to 0
for column in corrected_data.columns[3:]:
    corrected_data[column] = corrected_data[column] - corrected_data['0.0']

# Zero out the '0.0' column by subtracting from itself
corrected_data['0.0'] = corrected_data['0.0'] - corrected_data['0.0']

# Print the corrected DataFrame
print(corrected_data)

# Export the blank corrected_data to a CSV file
corrected_data.to_csv('/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/corrected_data_output.csv', index=False)

print("corrected_data dataframe exported successfully!")

