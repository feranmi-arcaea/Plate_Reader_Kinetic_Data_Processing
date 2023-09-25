
import pandas as pd
import sys

import sys

input_data = sys.argv[1].strip()
output_path, Plate_map_input_file = input_data.split(',')



output_folder = "/".join(output_path.split("/")[:-1])  # Extracts directory from the full path



# Load CSV files into dataframes
od590_minus_od700_df_transposed = pd.read_csv(output_path, index_col=0)  # Assuming 'Well' is the index
df_annotation = pd.read_csv(Plate_map_input_file)

print(df_annotation)

# Set 'Well' column as index for df_annotation
df_annotation.set_index('Well', inplace=True)

# Merge data based on 'Well' column
Annotated_od590_minus_od700 = od590_minus_od700_df_transposed.join(df_annotation, how='left')

# Rename the 'Annotation' column to 'annotation'
Annotated_od590_minus_od700.rename(columns={'Annotation': 'Annotation'}, inplace=True)

print(Annotated_od590_minus_od700)


# Group by 'Annotation' and calculate the mean for each group
averaged_df = Annotated_od590_minus_od700.groupby('Annotation').mean()

# Split the index
split_index = averaged_df.index.str.split('_')

# Create new columns
averaged_df['Condition'] = split_index.str[0]
averaged_df['Microbe_Type'] = split_index.str[1]

# Define the desired order for the columns
cols = averaged_df.columns.tolist()
cols = [cols[-2]] + [cols[-1]] + cols[:-2]

# Reorder the columns
averaged_df = averaged_df[cols]

print(averaged_df)

output_path_averaged_df = f"{output_folder}/averaged_output.csv"  # Construct the output path for averaged_df
# Export the averaged_df to a CSV file
averaged_df.to_csv(output_path_averaged_df)

print("Averaged dataframe exported successfully!")
print(f"{output_path_averaged_df},{output_folder}")
