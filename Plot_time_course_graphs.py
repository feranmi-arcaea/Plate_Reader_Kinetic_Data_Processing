import pandas as pd
import matplotlib.pyplot as plt

import sys
# # Read output_folder and output_path_corrected_data from the file
# with open("config.txt", "r") as f:
#     output_folder = f.readline().strip()
#     output_path_corrected_data = f.readline().strip()

# Assuming 'data' is the path to your CSV file

input_data = sys.argv[1].strip()
output_path_corrected_data, output_folder = input_data.split(",")
data_path = output_path_corrected_data

# Read the data into a DataFrame
corrected_data = pd.read_csv(output_path_corrected_data)

# Unique microbes
microbes = corrected_data['Microbe_Type'].unique()

# Remove any non-numeric 'Microbe_Type' entries like 'Blank'
microbes = [microbe for microbe in microbes if pd.notna(microbe)]

# Define x values (Time)
x = corrected_data.columns[2:]

# Iterate over each microbe and plot the graph
for microbe in microbes:
    plt.figure(figsize=(12, 6))
    plt.title(f'OD vs Time for {microbe}')
    plt.xlabel('Time')
    plt.ylabel('OD')
    
    # Subset data for the current microbe
    microbe_corrected_data = corrected_data[corrected_data['Microbe_Type'] == microbe]
    
    for index, row in microbe_corrected_data.iterrows():
        condition = row['Condition']
        y = row[2:]
        plt.plot(x, y, label=condition)

    # Set every 3rd x-tick
    plt.xticks(x[::3])
    
    plt.legend()
    plt.grid(True)
    
    # Save the plot to the specified output folder
    plot_path = f"{output_folder}/OD_vs_Time_for_{microbe}.png"
    plt.savefig(plot_path, dpi=300)
    plt.show()

print(f"Plots saved to: {output_folder}")

