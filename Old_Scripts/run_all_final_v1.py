import subprocess
# input_1 = '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Buffered_Lotions_SLM_09_20_23_R1_FA.xlsx' # Raw plate reader file
# input_2 = '/mnt/g/Shared drives/Personal Folders/Feranmi/Experimental Data/Plate_map_input_file.csv' # Plate_map_input_file
# input_3 = '/mnt/g/Shared drives/Personal Folders/Feranmi/Experimental Data/Buffered_Lotions/Output_folder_1' #Output_folder
input_1 = '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Buffered_Spray_AAs_SLM_09_14_23_R3_FA.csv'
input_2= '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Plate_map_input_file.csv'
input_3= '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Test_PReader_Pipeline/Output_folder_3'

print(input_1)
print(input_2)
print(input_3)
# Execute the first script with the provided inputs and capture its output
result = subprocess.run(['python3', 'Extract_OD_final_v1.py', input_1, input_2, input_3], capture_output=True, text=True)
lines = result.stdout.strip().split('\n')
last_line = lines[-1] if lines else ""
print('\n'.join(result.stdout.split('\n')[:5]))
print(last_line)
print(result.stderr.strip().split('\n'))
print("Extract_OD_final_v1 done")

# Execute the second script and pass the last line of the first script's output as an argument
result = subprocess.run(['python3', 'Annotate_extracted_data.py', last_line], capture_output=True, text=True)
lines = result.stdout.strip().split('\n')
last_line = lines[-1] if lines else ""
print('\n'.join(result.stdout.split('\n')[:5]))
print(last_line)
print("Annotate_extracted_data done")

# Execute the third script and pass the last line of the second script's output as an argument
result = subprocess.run(['python3', 'subtract_blanks_final_v1.py', last_line], capture_output=True, text=True)
lines = result.stdout.strip().split('\n')
last_line = lines[-1] if lines else ""
print('\n'.join(result.stdout.split('\n')[:5]))
print(last_line)
print("subtract_blanks_final_v1 done")

# Execute the fourth script and pass the last line of the third script's output as an argument
subprocess.run(['python3', 'calculate_AUC.py', last_line], capture_output=True, text=True)
lines = result.stdout.strip().split('\n')
last_line = lines[-1] if lines else ""
print('\n'.join(result.stdout.split('\n')[:5]))
print(last_line)
print("calculate_AUC done")

# Execute the fourth script and pass the last line of the third script's output as an argument
subprocess.run(['python3', 'plot_time_course_graphs.py', last_line])
lines = result.stdout.strip().split('\n')
last_line = lines[-1] if lines else ""
print('\n'.join(result.stdout.split('\n')[:5]))
print(last_line)
print("plot_time_course_graphs done")