import csv
import pandas as pd
import os

# Determine the file type
def get_file_type(filename):
    return os.path.splitext(filename)[1]

# Extract microbes and conditions from the input file
microbes = []
conditions = []

input_filename = "/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Plate_Outline_9_26.csv"
output_filename = "/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/plate_map_input_file_9_26.csv"

# Based on file type, read accordingly
if get_file_type(input_filename) == ".csv":
    with open(input_filename, "r") as file:
        reader = csv.reader(file)

        # Extract microbes from the first row, starting from the third column (including "Blank")
        microbes = next(reader)[2:]

        # Extract conditions from the second column, starting from the second row
        for row in reader:
            conditions.append(row[1])
elif get_file_type(input_filename) == ".xlsx":
    df_input = pd.read_excel(input_filename)
    microbes = df_input.columns[2:].tolist()
    conditions = df_input.iloc[:, 1].tolist()
else:
    print(f"Unsupported file type for {input_filename}")
    exit()

# Generate the well IDs
rows = 'ABCDEFGHIJKLMNOP'
cols = list(range(1, 25))
wells = [f"{r}{c}" for c in cols for r in rows]

# Grouping by microbes first
combinations = [(microbe, condition) for microbe in microbes for _ in range(3) for condition in conditions]

# Generate the required data structure for the DataFrame
data = []
for well, (microbe, condition) in zip(wells, combinations):
    data.append((well, f"{condition}_{microbe}"))

# Convert to DataFrame
df = pd.DataFrame(data, columns=['Well', 'Annotation'])
print(df)

# Export DataFrame to a CSV file
df.to_csv(output_filename, index=False)

print(f"Data exported to {output_filename}")
