# Create a new Original Name --> New Name Excel file or use a pre-made one?
    # Create:
        # Would you like to include files from subdirectories?
        # Generate the template file and exit script
    # Execute Renaming from Excel template:
        # Load original and final filenames for confirmation
        # Confirm source directory
        # log errors for missing files and dump at the end
        # Rename the files from the original to the new ones based on Excel input

import os
import pandas as pd
from datetime import datetime


class tc:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

    @classmethod
    def red(cls, text):
        return cls.RED + str(text) + cls.RESET

    @classmethod
    def green(cls, text):
        return cls.GREEN + str(text) + cls.RESET

    @classmethod
    def yellow(cls, text):
        return cls.YELLOW + str(text) + cls.RESET

    @classmethod
    def blue(cls, text):
        return cls.BLUE + str(text) + cls.RESET

    @classmethod
    def magenta(cls, text):
        return cls.MAGENTA + str(text) + cls.RESET

    @classmethod
    def cyan(cls, text):
        return cls.CYAN + str(text) + cls.RESET

    @classmethod
    def white(cls, text):
        return cls.WHITE + str(text) + cls.RESET

class customError(Exception):
    pass

def getDateTime():
    """
    Returns the date and time as a string in the format DDMMMYYYY-HHMM e.g. 05JUL2023-1207
    """
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d%b%Y-%H%M").upper()
    return formatted_datetime

def find_files_oftype_subdirs(directory, file_extension):
    file_list = []

    for root, dirs, files in os.walk(directory):
        if file_extension == "all":
            for file in files:
                file_list.append(os.path.join(root, file))
        else:
            for file in files:
                if file.endswith(file_extension):
                    file_list.append(os.path.join(root, file))
    return file_list

def find_files_oftype_surface(directory, file_extension):
    files = []
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if file_extension != "all":
            if item.endswith(file_extension):
                files.append(full_path)
        else:
                files.append(full_path)

    return files

def load_excel_as_tuples(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Check if the necessary columns are present
        if 'Original' not in df.columns or 'New' not in df.columns:
            raise customError("Excel file must contain 'Original' and 'New' columns")
        
        # # Check if the 'Directory' column is present and get the first value
        # master_dir = df['Directory'].iloc[0] if 'Directory' in df.columns and not df['Directory'].empty else None

        # Convert the DataFrame to a list of tuples
        tuples_list = list(df[['Original', 'New']].itertuples(index=False, name=None))
    except Exception as e:
        raise customError(f"ERROR load_excel_as_tuples: {e}")

    return tuples_list

def create_excel_from_list(original_list, file_path):
    try:
        # Create a DataFrame with the 'original' column from the list and an empty 'new' column
        df = pd.DataFrame({
            'Original': original_list,
            'New': [''] * len(original_list)  # Create an empty list of the same length as original_list
        })
        # # Add the 'Directory' column with the directory string in the first row
        # df['Directory'] = [directory] + [None] * (len(original_list) - 1)
        # Write the DataFrame to an Excel file
        df.to_excel(file_path, index=False, engine='openpyxl')
        return "completed"
    except Exception as e:
        raise customError(f"ERROR create_excel_from_list: {e}")
    
print(tc.red("\nEnter \"exit\" to quit script anytime."))
while True:

    create_execute_choice = input(tc.cyan("\nWould you like to Create a new template file for renaming, or Execute renaming from an existing file?\n\tType \"create\" or \"execute\": "))
    if create_execute_choice.lower() == "create" or create_execute_choice.lower() == "execute":
        break
    elif create_execute_choice.lower() == "exit":
        exit()
    else:
        print(tc.red(f"Not a valid option: {create_execute_choice}\n"))

template_output_fp = None
if create_execute_choice.lower() == "create":
    
    while True:
        query_directory_choice = input(tc.cyan("Would you like to populate your template with filenames from a directory?\n\ty/n? "))
        if query_directory_choice.lower() == "y" or query_directory_choice.lower() == "n":
            break
        elif query_directory_choice.lower() == "exit":
            exit()

    if query_directory_choice.lower() == "y":
        while True:
            source_directory = input(tc.cyan("Enter your source directory: "))
            if os.path.isdir(source_directory):
                break
            elif source_directory.lower() == "exit":
                exit()
            else:
                print(tc.red(f"\nError: {source_directory} is not a valid directory"))

        while True:
            include_subdir_choice = input(tc.cyan(f"Would you like to include the subdirectories from {os.path.basename(source_directory)}? y/n: "))
            if include_subdir_choice.lower() == "y" or include_subdir_choice.lower() == "n":
                break
            elif include_subdir_choice.lower() == "exit":
                exit()
    
    # Run the create functions
    filelist_to_populate = []
    if query_directory_choice.lower() == "y":
        if include_subdir_choice.lower() == "y":
            filelist_to_populate = find_files_oftype_subdirs(source_directory, "all")
        elif include_subdir_choice.lower() == "n":
            filelist_to_populate = find_files_oftype_surface(source_directory, "all")

    template_output_fp = os.path.dirname(os.path.abspath(__file__))
    template_output_fp = os.path.join(template_output_fp, f"BatchRename_Template_on_{getDateTime()}.xlsx")
    create_excel_from_list(filelist_to_populate, template_output_fp)

    while True:
        continue_choice = input(tc.cyan(f"\nThe file has been generated for you to modify: " + tc.white(template_output_fp) + "\n\tPlease add in your new names under \"New\" WITHOUT THE .xxx EXTENSION and save.\n\tAre you ready to continue? y/n: "))
        if continue_choice.lower() == "y":
            break
        elif continue_choice.lower() == "n":
            print(tc.yellow("Exiting script..."))
            exit()
        elif continue_choice.lower() == "exit":
            exit()

# elif create_execute_choice.lower() == "execute":

if not template_output_fp:
    while True:
        template_output_fp = input(tc.cyan("\n\nEnter your template filepath: "))
        if os.path.isfile(template_output_fp):
            break
        elif template_output_fp.lower() == "exit":
            exit()
        else:
            print(tc.red(f"\nError: {template_output_fp} is not a valid filepath"))

# Run the execute functions
filelist_to_rename = load_excel_as_tuples(template_output_fp)
print(tc.cyan(f"Starting execution for {len(filelist_to_rename)} operations"))


# Generate list of missing/erroneous filess
warning_list = []
renamed_list = []
for original_name, new_name in filelist_to_rename:

    if type(new_name) is float or new_name == "" or new_name is None:
        reason = f"New name not found for: {original_name} -> \"{str(new_name)}\""
        print(tc.red(reason))
        warning_list.append((original_name, reason))
        continue

    if not os.path.isfile(original_name):
        reason = f"Could not find file: {original_name}"
        print(reason)
        warning_list.append(original_name, reason)
        continue
    

    root_new, ext_new = os.path.splitext(new_name)
    root_original, ext_original = os.path.splitext(original_name)

    if ext_new == "" or ext_new is None:
        new_name = root_new + ext_original

    new_fp = os.path.join(os.path.dirname(original_name), new_name)
    renamed_list.append((original_name, new_fp))

# Ask Confirmation
while True:
    print(tc.yellow("WARNINGS: "))
    for originalname, reason in warning_list:
        print(tc.yellow(f"{originalname} because {reason}"))

    print(tc.green("VALID RENAME OPERATIONS: "))
    for originalname, newname in renamed_list:
        print(tc.white(f"{originalname} -> {newname}"))

    confirmation_choice = input(tc.cyan(f"Would you like to continue anyway with {len(renamed_list)} valid transactions? {len(warning_list)} Errors will not be processed. y/n: "))
    if confirmation_choice.lower() == "y":
        break
    elif confirmation_choice.lower() == "n" or confirmation_choice.lower() == "exit":
        exit()
    

print("\nStarting to rename....\n")
counter = 0
for original_name, new_name in renamed_list:
    try:
        os.rename(src=original_name, dst=new_name)
        print(f"Renamed {original_name} to {new_name}")
        counter += 1
    except Exception as e:
        print(f"ERROR trying to rename file: {e}")

print(tc.green(f"Successfully renamed {counter} files!"))