import os
import pandas as pd
import readline  # Just import it

# Ask user for input file path and output folder
# input_file_path = input("Enter the path to the Exported plate reader data file (either .csv or .xlsx): ").strip()
# Plate_map_input_file = input("Enter the path to the Plate map annotation file (must be .csv file): ").strip()
# output_folder = input("Enter the path to the desired output folder: ").strip().replace("'", "")
# input_1 = '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Buffered_Spray_AAs_SLM_09_14_23_R3_FA.csv'
# input_2= '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Plate_map_input_file.csv'
# input_3= '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Test_PReader_Pipeline/Output_folder_2'

import sys

# Ensure that we have the correct number of arguments (1 script name + 3 inputs = 4 total)
if len(sys.argv) != 4:
    print("Usage: Extract_OD_final_v1.py <input_1> <input_2> <input_3>")
    sys.exit(1)

input_1, input_2, input_3 = sys.argv[1], sys.argv[2], sys.argv[3]
input_file_path = input_1.strip()
Plate_map_input_file = input_2.strip()
output_folder = input_3.strip()
output_path = f"{output_folder}/ExtractOD_output_file.csv"  # Construct the output path

# Extract the file extension
file_extension = os.path.splitext(input_file_path)[1].strip().lower()
print (file_extension)

# Convert .xlsx to .csv if necessary
if file_extension == '.xlsx':
    # Read the Excel file
    df = pd.read_excel(input_file_path, header=None)
    
    # Construct new .csv file path
    new_csv_path = os.path.splitext(input_file_path)[0] + ".csv"
    
    # Save the dataframe to .csv
    df.to_csv(new_csv_path, index=False, header=False)
    
    # Update the input_file_path to the new .csv path
    input_file_path = new_csv_path
    file_extension = '.csv'  # update file_extension to '.csv' for later checks
print (input_file_path)

# Check if output folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Strip the quotes from the input paths (if they exist)
input_file_path = input_file_path.strip("'").strip('"')

# Extract the file extension
file_extension = os.path.splitext(input_file_path)[1].strip().lower()


# Load the data based on file extension
if file_extension == '.csv':
    data = pd.read_csv(input_file_path, header=None)
elif file_extension == '.xlsx':
    data = pd.read_excel(input_file_path, header=None)
else:
    print(f"Detected file extension: '{file_extension}'")
    print("Unsupported file type")
    exit()  # Exit the script if the file type is unsupported


num_reads=73
# Drop entirely NaN columns and rows
data_cleaned = data.dropna(axis=1, how='all')
data_cleaned = data_cleaned.dropna(axis=0, how='all').reset_index(drop=True)
print (data_cleaned[348:])

# Identifying all tables with reads for OD590 and OD700
od590_row_indices = data_cleaned[data_cleaned[0].str.contains(r'Read \d+:590', na=False)].index
od700_row_indices = data_cleaned[data_cleaned[0].str.contains(r'Read \d+:700', na=False)].index

print (od700_row_indices)
# Function to extract the data for a specific read (either OD590 or OD700) given its starting index
# Add 2 to num_reads because there are two lines between start index of Read \d+:590 and time readings
def extract_data_from_index(start_index):
    return data_cleaned.iloc[start_index + 1:start_index + num_reads +2]


def excel_datetime_to_time_str(excel_datetime_str):
    """Extract the time portion from an Excel date-time string and add 24h depending on days since 1900-01-01."""
    date_str, time_str = excel_datetime_str.split()
    year, month, day = map(int, date_str.split('-'))
    # Subtracting 1 day because we are considering from 1900-01-01
    days_from_1900 = (datetime.date(year, month, day) - datetime.date(1900, 1, 1)).days + 1
    added_hours = 24 * days_from_1900

    hours, minutes, seconds = map(int, time_str.split(":"))
    hours += added_hours
    print(f"Extract the time portion: {hours:02d}:{minutes:02d}:{seconds:02d}")
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Modify the convert_to_time_str function to handle Excel date-time format
def convert_to_time_str(value):
    if isinstance(value, float):
        if not math.isnan(value):
            value = str(value)
            if "." in value:
                value = value.split(".")[0]  # Removing decimal part if present
        else:
            return None  # Return None for 'nan'
    if value.startswith("1900-"):  # Check for Excel's datetime format
        value = excel_datetime_to_time_str(value)
    return value

# Now, before processing, let's convert .xlsx files to .csv
if file_extension == '.xlsx':
    temp_csv_path = os.path.join(output_folder, "temp_converted.csv")
    data_xlsx = pd.read_excel(input_file_path, header=None)
    data_xlsx.to_csv(temp_csv_path, index=False, header=False)
    data = pd.read_csv(temp_csv_path, header=None)
    os.remove(temp_csv_path)  # remove the temporary .csv file after reading
elif file_extension == '.csv':
    data = pd.read_csv(input_file_path, header=None)
else:
    print(f"Detected file extension: '{file_extension}'")
    print("Unsupported file type")
    exit()  # Exit the script if the file type is unsupported


import datetime

def time_to_str(time_obj):
    """Convert a datetime.time object to a string."""
    return time_obj.strftime('%H:%M:%S')

from datetime import timedelta

def convert_to_timedelta(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def extract_od_values(od_index):
# Extracting data
    print("Extracting data...")
    od_table = extract_data_from_index(od_index).reset_index(drop=True)
    print("Data extracted.")
    
    # Drop the rows corresponding to the "0:00:00" times
    od_table = od_table[od_table.iloc[:, 1] != "0:00:00"]

    # Extracting well names
    print("Extracting well names...")
    well_names = od_table.iloc[0][3:].values
    # print(f"Well names extracted: {well_names}.")
    
    # Extracting and converting time values
    print("Extracting and converting time values...")
    
    # Extracting raw time values from the 2nd column after filtering
    raw_time_values = od_table.iloc[1:, 1].values
    
    # Print the raw time values
    print(f"Raw time values: {raw_time_values[:4]} ... {raw_time_values[-4:]}")

    # Convert raw_time_values to strings if they are datetime.time objects
    raw_time_values = [time_to_str(val) if isinstance(val, datetime.time) else val for val in raw_time_values]
    
    raw_time_values = [convert_to_time_str(val) for val in raw_time_values]
    
    # Remove None values which represent 'nan' from raw_time_values
    raw_time_values = [val for val in raw_time_values if val is not None]
    
    if not raw_time_values:
        print("No valid time values found!")
        return None

    # Convert the time strings to timedeltas
    time_deltas = [convert_to_timedelta(time_str) for time_str in raw_time_values]

    # Compute the starting time (first value in time_deltas)
    start_time = time_deltas[0]

    # Convert the time_deltas to relative minutes
    time_values = [(td - start_time).total_seconds() / 60 for td in time_deltas]
    print(f"Converted time values to relative minutes")
    
    # Formatting data
    print("Formatting data...")
    od_numeric = od_table.drop([0]).drop(od_table.columns[:3], axis=1).astype(float)
    od_numeric.columns = well_names
    od_numeric['Time'] = time_values
    od_numeric.set_index('Time', inplace=True)
    
    # Returning processed data
    print("Returning processed data.")
    return od_numeric



# od590_table = [extract_od_values(349)]
# print(f"od590_table: {od590_table}.")

od590_tables = [extract_od_values(index) for index in od590_row_indices]
od700_tables = [extract_od_values(index) for index in od700_row_indices]

# Combine all OD590 tables into one DataFrame based on the Time index
print("Combining OD590 and OD700 tables into one DataFrame each...")
# Assuming the first DataFrame in the list as the base
combined_od590 = od590_tables[0]

# Iteratively merge the rest of the dataframes based on the index (Time)
for df in od590_tables[1:]:
    combined_od590 = combined_od590.merge(df, left_index=True, right_index=True, how='outer')

# Handle any NaN values if necessary (e.g., fill with 0 or other appropriate value)
# combined_od590.fillna(0, inplace=True)
combined_od700 = od700_tables[0]

# Iteratively merge the rest of the dataframes based on the index (Time)
for df in od700_tables[1:]:
    combined_od700 = combined_od700.merge(df, left_index=True, right_index=True, how='outer')

# Handle any NaN values if necessary (e.g., fill with 0 or other appropriate value)
# combined_od590.fillna(0, inplace=True)



#print(f"od590_table: {combined_od590}.")

#print(f"od700_table: {combined_od700}.")

# Combine all OD590 tables into one DataFrame based on the Time index
print("Subtracting OD700 from OD590...")
od590_minus_od700_df = combined_od590 - combined_od700
od590_minus_od700_df_transposed=od590_minus_od700_df.T

# Convert the time index to hours
od590_minus_od700_df_transposed.columns = od590_minus_od700_df_transposed.columns / 60

print (f"od590_minus_od700_df: {od590_minus_od700_df_transposed}.")

# Export to CSV

od590_minus_od700_df_transposed.to_csv(output_path)
print(f"Data exported to {output_path}")
print ("check")
print(f"{output_path},{Plate_map_input_file}")