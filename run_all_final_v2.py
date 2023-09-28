import subprocess
# input_1 = '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Buffered_Lotions_SLM_09_20_23_R1_FA.xlsx' # Raw plate reader file
# input_2 = '/mnt/g/Shared drives/Personal Folders/Feranmi/Experimental Data/Plate_map_input_file.csv' # Plate_map_input_file
# input_3 = '/mnt/g/Shared drives/Personal Folders/Feranmi/Experimental Data/Buffered_Lotions/Output_folder_1' #Output_folder
# input_1 = '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Spray_Wipes_SLM_09_26_23_R1_FA.xlsx'
# input_2= '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/plate_map_input_file_9_26.csv'
# input_3= '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Plate_Reader_Kinetic_Data_Processing_Output/Spray_Wipes_SLM_09_26_23_R1_FA'
input_1 = '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/GitHub_Code/Plate_Reader_Kinetic_Data_Processing/Sample Files/AAs_SLM_variations_09_19_23_R1_FA.xlsx'
input_2= '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/GitHub_Code/Plate_Reader_Kinetic_Data_Processing/Sample Files/Plate_map_input_file.csv'
input_3= '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/GitHub_Code/Plate_Reader_Kinetic_Data_Processing/Sample Files/Output_folder'


# input_1 = '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Buffered_Lotions_SLM_09_20_23_R1_FA.csv'
# input_2= '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Plate_map_input_file.csv'
# input_3= '/mnt/g/Shared drives/Arcaea Shared Drive/Personal Folders/Feranmi/Experimental Data/Test_PReader_Pipeline/Output_folder_4'
import subprocess
import os

def run_script(command_list):
    """Execute a script and log its output."""
    result = subprocess.run(command_list, capture_output=True, text=True)
    
    log_output(result)
    
    if result.returncode != 0:
        print(f"Error executing {' '.join(command_list)}")
        exit(1)  # Stops the script if there's an error
    
    return result.stdout.strip().split('\n')[-1] if result.stdout else ""

def log_output(result):
    """Append the script's stdout and stderr to the log file and print relevant lines."""
    with open(f"{input_3}/log.txt", "a") as log_file:
        log_file.write(result.stdout)
        log_file.write(result.stderr)

    print('\n'.join(result.stdout.split('\n')[:5]))
    print('\n'.join(result.stdout.split('\n')[:-5]))
    if result.stdout:
        print(result.stdout.strip().split('\n')[-1])
    if result.stderr:
        print(result.stderr)

def main():
    # Ensure the directory exists, if not create it
    os.makedirs(input_3, exist_ok=True)
    
    # Clearing or creating the log file
    open(f"{input_3}/log.txt", 'w').close()


    last_output = run_script(['python3', 'Extract_OD_final_v2.py', input_1, input_2, input_3])
    print("Extract_OD_final_v1 done")

    last_output = run_script(['python3', 'Annotate_extracted_data.py', last_output])
    print("Annotate_extracted_data done")

    last_output = run_script(['python3', 'subtract_blanks_final_v1.py', last_output])
    print("subtract_blanks_final_v1 done")

    last_output = run_script(['python3', 'calculate_AUC.py', last_output])
    print("calculate_AUC done")

    run_script(['python3', 'plot_time_course_graphs.py', last_output])
    print("plot_time_course_graphs done")

if __name__ == "__main__":
    input_1 = input_1
    input_2= input_2
    input_3= input_3
    main()
