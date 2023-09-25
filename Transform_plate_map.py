import pandas as pd

def transform_csv(input_path, output_path):
    # Read the CSV file, skipping the last NaN column and using "Unnamed: 1" as the index
    df = pd.read_csv(input_path, usecols=lambda column: column != "Unnamed: 10", index_col="Unnamed: 1")

    # Prepare new DataFrame for the transformed data
    transformed_df = pd.DataFrame()

    # For each row in the original DataFrame
    for index, row in df.iterrows():
        # Get the condition for the row (e.g. "Condition 1")
        condition = index

        # For the first column (the alphanumeric label)
        transformed_df.at[index, '2'] = condition

        # For each microbe in the row, excluding the first column which is now the index
        for i, microbe in enumerate(row[1:]):  # Exclude first column
            # Append three times
            for _ in range(3):
                new_col_name = i * 3 + _ + 3  # Calculate the new column number (starting at 3 for the first microbe)
                if condition == "Column":  # Handle the header row separately
                    transformed_df.at[index, new_col_name] = microbe
                else:
                    transformed_df.at[index, new_col_name] = f"{microbe}_{condition}"

    # Add the first column (index) as a new column
    transformed_df.insert(0, '1', transformed_df.index)

    # Reorder columns based on integer order (since they're now stored as strings)
    transformed_df = transformed_df[sorted(transformed_df.columns, key=int)]

    # Drop the '2' column as it contains the conditions, which you wanted discarded
    transformed_df.drop(columns=['2'], inplace=True)

    # Save the transformed data to a new CSV
    transformed_df.to_csv(output_path, index=False)

# Usage example
# transform_csv('input.csv', 'output.csv')

# Use the function
transform_csv('plate_map_template.csv', 'plate_map_template_output.csv')
