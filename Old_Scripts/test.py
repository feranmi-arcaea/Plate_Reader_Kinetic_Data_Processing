import pandas as pd

# Load the data
data = pd.read_csv("/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Test_export_dataset.csv", header=None)

num_reads=73

#print (data)
# Drop entirely NaN columns and rows
data_cleaned = data.dropna(axis=1, how='all')
data_cleaned = data_cleaned.dropna(axis=0, how='all').reset_index(drop=True)

# print (data_cleaned)

# Identifying all tables with reads for OD590 and OD700
od590_row_indices = data_cleaned[data_cleaned[0].str.contains(r'Read \d+:590', na=False)].index
od700_row_indices = data_cleaned[data_cleaned[0].str.contains(r'Read \d+:700', na=False)].index

print (od700_row_indices)
# Function to extract the data for a specific read (either OD590 or OD700) given its starting index
def extract_data_from_index(start_index):
    return data_cleaned.iloc[start_index + 1:start_index + num_reads]

# extract_data= extract_data_from_index(349)

# print (extract_data)

# Function to extract the OD values
def extract_od_values(od_index):
    od_table = extract_data_from_index(od_index).reset_index(drop=True)
    well_names = od_table.iloc[0][2:].values


    time_values = od_table.iloc[2:, 0].values
    
    od_numeric = od_table.drop([0, 1]).drop(od_table.columns[0], axis=1).astype(float)
    od_numeric.columns = well_names
    od_numeric['Time'] = time_values
    od_numeric.set_index('Time', inplace=True)
    
    return od_numeric


def convert_to_time_str(value):
    if isinstance(value, float):
        if not math.isnan(value):
            value = str(value)
            if "." in value:
                value = value.split(".")[0]  # Removing decimal part if present
        else:
            return None  # Return None for 'nan'
    return value
import datetime

def extract_od_values(od_index):
    
    # Extracting data
    print("Extracting data...")
    od_table = extract_data_from_index(od_index).reset_index(drop=True)
    print("Data extracted.")
    
    # Extracting well names
    print("Extracting well names...")
    well_names = od_table.iloc[0][2:].values
    print(f"Well names extracted: {well_names}.")



    
    # Extracting time values and converting to relative minutes
    print("Extracting and converting time values...")
    
    # Extracting raw time values from the 2nd column
    raw_time_values = od_table.iloc[2:, 1].values
    
    # Print the raw time values
    print(f"Raw time values: {raw_time_values}")

    raw_time_values = [convert_to_time_str(val) for val in raw_time_values]
    
    # Remove None values which represent 'nan' from raw_time_values
    raw_time_values = [val for val in raw_time_values if val is not None]
    
    if not raw_time_values:
        print("No valid time values found!")
        return None
    
    # Filter out the "0:00:00" time values
    raw_time_values = [val for val in raw_time_values if val != "0:00:00"]

    start_time = datetime.datetime.strptime(raw_time_values[0], '%H:%M:%S') - datetime.datetime(1900, 1, 1)
    time_values = [(datetime.datetime.strptime(time_str, '%H:%M:%S') - datetime.datetime(1900, 1, 1) - start_time).total_seconds() / 60 for time_str in raw_time_values]
    print(f"Converted time values to relative minutes: {time_values}.")
 
    
# Drop the rows corresponding to the "0:00:00" times (now negative relative minutes)
    od_table = od_table[od_table.iloc[:, 1] != "0:00:00"]
    
    # Formatting data
    print("Formatting data...")
    print("Well names:", well_names) 
    od_numeric = od_table.drop([0, 1]).drop(od_table.columns[:2], axis=1).astype(float)
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

print (od590_tables[3:4])



import pandas as pd

# Load the data
data = pd.read_csv("/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Test_export_dataset.csv", header=None)

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
def extract_data_from_index(start_index):
    return data_cleaned.iloc[start_index + 1:start_index + num_reads]


def convert_to_time_str(value):
    if isinstance(value, float):
        if not math.isnan(value):
            value = str(value)
            if "." in value:
                value = value.split(".")[0]  # Removing decimal part if present
        else:
            return None  # Return None for 'nan'
    return value
import datetime

def extract_od_values(od_index):
    
    # Extracting data
    print("Extracting data...")
    od_table = extract_data_from_index(od_index).reset_index(drop=True)
    print("Data extracted.")
    
    # Extracting well names
    print("Extracting well names...")
    well_names = od_table.iloc[0][3:].values
    #print(f"Well names extracted: {well_names}.")
    
    # Extracting time values and converting to relative minutes
    print("Extracting and converting time values...")
    
    # Extracting raw time values from the 2nd column
    raw_time_values = od_table.iloc[1:, 1].values
    
    # Print the raw time values
    print(f"Raw time values: {raw_time_values[:4]} ... {raw_time_values[70:]}")

    raw_time_values = [convert_to_time_str(val) for val in raw_time_values]
    
    # Remove None values which represent 'nan' from raw_time_values
    raw_time_values = [val for val in raw_time_values if val is not None]
    
    if not raw_time_values:
        print("No valid time values found!")
        return None
    
    # Filter out the "0:00:00" time values
    raw_time_values = [val for val in raw_time_values if val != "0:00:00"]

    start_time = datetime.datetime.strptime(raw_time_values[0], '%H:%M:%S') - datetime.datetime(1900, 1, 1)
    time_values = [(datetime.datetime.strptime(time_str, '%H:%M:%S') - datetime.datetime(1900, 1, 1) - start_time).total_seconds() / 60 for time_str in raw_time_values]
    print(f"Converted time values to relative minutes")
    # print(f"Converted time values to relative minutes: {time_values}.")
    
# Drop the rows corresponding to the "0:00:00" times (now negative relative minutes)
    od_table = od_table[od_table.iloc[:, 1] != "0:00:00"]
    
    # Formatting data
    print("Formatting data...")
   # print("Well names:", well_names) 
    #print(f"od_table: {od_table}")
    od_numeric = od_table.drop([0]).drop(od_table.columns[:3], axis=1).astype(float)
    #print(f"od_numeric: {od_numeric}")

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

print (f"od590_minus_od700_df: {od590_minus_od700_df}.")
