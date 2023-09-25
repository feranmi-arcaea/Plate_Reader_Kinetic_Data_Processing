
import pandas as pd

# Load CSV files into dataframes
od590_minus_od700_df_transposed = pd.read_csv("/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Test_v1_ExtractOD_output_file.csv", index_col=0)  # Assuming 'Well' is the index
df_annotation = pd.read_csv("/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Plate_map_input_file.csv")

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

# Export the averaged_df to a CSV file
averaged_df.to_csv('/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/averaged_output.csv')

print("Averaged dataframe exported successfully!")
