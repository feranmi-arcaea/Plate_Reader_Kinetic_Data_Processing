import pandas as pd

import sys

input_data = sys.argv[1].strip()

# input_data = sys.stdin.read().strip()
output_path_averaged_df, output_folder = input_data.split(",") # Extracts directory from the full path


# Load CSV files into dataframes
data = pd.read_csv(output_path_averaged_df, index_col=0)  # Assuming 'Well' is the index

print (data)
print (data['Condition'])

# Get unique conditions
unique_conditions = data['Condition'].unique()
print (unique_conditions)
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

output_path_corrected_data = f"{output_folder}/corrected_data_output.csv"  # Construct the output path for averaged_df
# Export the blank corrected_data to a CSV file
corrected_data.to_csv(output_path_corrected_data, index=False)

print("corrected_data dataframe exported successfully!")

print(f"{output_path_corrected_data},{output_folder}")