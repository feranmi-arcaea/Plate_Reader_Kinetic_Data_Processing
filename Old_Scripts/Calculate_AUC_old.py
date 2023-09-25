import os
import pandas as pd
import numpy as np
from sklearn.metrics import auc

# Define a helper function to check if a file is locked (in use)
def file_is_locked(filepath):
    locked = None
    file_object = None
    if os.path.exists(filepath):
        try:
            # Try opening the file with "append" mode
            # This mode won't modify your file
            file_object = open(filepath, 'a')
        except PermissionError:
            locked = True
        else:
            locked = False
        finally:
            if file_object:
                file_object.close()
    return locked

# File name of the CSV
csv_file = output_path_corrected_data
# Name of the Excel file to write the results
AUC_output_file = f"{output_folder}/Final_AUC_output_file.xlsx"

while file_is_locked(csv_file):
    input(f"The file {csv_file} is currently open. Please close it and press Enter to continue.")

# Check if the file exists
if not os.path.exists(csv_file):
    print(f"File {csv_file} not found.")
else:
    # Import data from the CSV
    corrected_data_for_AUC = pd.read_csv(csv_file)

    # Extract time points from the columns
    time_points = corrected_data_for_AUC.columns[2:].astype(float).to_list()

    # Calculate AUC above the baseline of 0 for each condition and microbe
    auc_results = []

    # Maintain the original order of the conditions
    original_order_conditions = corrected_data_for_AUC['Condition'].drop_duplicates().tolist()

    for condition in original_order_conditions:
        for microbe in corrected_data_for_AUC['Microbe_Type'].unique():
            sub_corrected_data_for_AUC = corrected_data_for_AUC[(corrected_data_for_AUC['Condition'] == condition) & (corrected_data_for_AUC['Microbe_Type'] == microbe)]
            y_values = sub_corrected_data_for_AUC.iloc[:, 2:].values.flatten()

            # Calculate AUC above the baseline of 0
            auc_value = auc(time_points, np.maximum(y_values - 0, 0))  # Calculate AUC above baseline

            auc_results.append({
                'Condition': condition,
                'Microbe_Type': microbe,
                'AUC': auc_value
            })

    # Create a dataframe to store AUC results
    auc_corrected_data = pd.DataFrame(auc_results)

    # Reshape the DataFrame to have microbes in rows and conditions in columns
    # while keeping the original order of the conditions
    pivot_auc_corrected_data = auc_corrected_data.pivot(index='Microbe_Type', columns='Condition', values='AUC')[original_order_conditions]



    # Write both corrected_data and pivot_auc_corrected_data to the Excel file
    with pd.ExcelWriter(AUC_output_file, engine='openpyxl') as writer:
        corrected_data_for_AUC.to_excel(writer, sheet_name='corrected_data', index=False)
        pivot_auc_corrected_data.to_excel(writer, sheet_name='Calculated_AUC')

    print("corrected_data and calculated AUC exported successfully!")