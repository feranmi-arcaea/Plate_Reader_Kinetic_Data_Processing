import pandas as pd

path_to_file = '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Plate_map_test.csv'

# Load CSV file into a dataframe
df = pd.read_csv(path_to_file, index_col=0)

# Convert dataframe to long format
df_melted = df.reset_index().melt(id_vars='index', value_name='Annotation')

# Create new row names based on row and column identifiers
df_melted['Well'] = df_melted['index'] + df_melted['variable'].astype(str)

# Drop unnecessary columns and reshape the dataframe
df_melted = df_melted[['Well', 'Annotation']].set_index('new_row')

# Export the original dataframe to Excel
path_to_excel = path_to_file.replace('.csv', '.xlsx')

with pd.ExcelWriter(path_to_excel, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name="Original_Data")
    df_melted.to_excel(writer, sheet_name="Reshaped_Data")

print(f"Data exported to {path_to_excel}")
