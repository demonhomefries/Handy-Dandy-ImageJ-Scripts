# Specify the INPUT directory containing the TIFF files:
directory = r"T:\Images\240802_133628_08.02_LV_Kinetics_20X_08-02-2024\240802_133628_LV_Kinetics_20X_08-02-2024_!PLATE_BARCODE!"

# Specify the OUTPUT directory for the newly created stack:
# Copy the folder path and paste it here, just make sure the "r" character is before the quotation marks
output_directory = r"C:\Users\Name\Desktop\Foldername"







import os
import json
from ij import ImageStack
from ij import IJ, ImagePlus
from ij.io import FileSaver
from ij import IJ

def find_tif_files(directory):
    tif_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.tif'):
                print("\tAdding {} to list!".format(os.path.basename(filename)))
                tif_files.append(os.path.join(root, filename))

    return tif_files

def match_files_to_keywords(filelist, keywords):
    keymatched_list = []
    for file in filelist:
        basename = os.path.basename(file)
        if all(keyword in basename for keyword in keywords):
            keymatched_list.append(file)
    return keymatched_list

def categorize_into_wellnames(filelist):
    organized_wells = {}

    for file in filelist:
        basename = os.path.basename(file)
        wellname = basename.split("_")[0]
        #print(wellname)
        if wellname not in organized_wells:
            organized_wells[wellname] = []  # Initialize a list for this wellname if it doesn't exist
        organized_wells[wellname].append(file)

    return organized_wells

def write_dict_to_json(filepath, data_dict):
    try:
        with open(filepath, 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
        print("Dictionary successfully written to {}".format(filepath))
    except Exception as e:
        print("An error occurred while writing to JSON: {}".format(e))

def create_and_save_stack(filelist, filename, output_path):
    stack = ImageStack()

    for filename in filelist:
        imp = IJ.openImage(filename)
        if imp is not None:
            # Add the image to the stack
            stack.addSlice(imp.getProcessor())
            print("\tAdded slice {} to stack".format(os.path.basename(filename)))


    # Create an ImagePlus from the stack
    imp_stack = ImagePlus(filename, stack)

    # Convert the stack to 8-bit
    IJ.run(imp_stack, "8-bit", "")

    # Set the micron size to 0.325 microns per pixel
    IJ.run(imp_stack, "Properties...", "channels=1 slices=" + str(imp_stack.getNSlices()) +
           " frames=1 pixel_width=0.325 pixel_height=0.325 voxel_depth=0.325")
    
    print("\tStarting to save stack")
    FileSaver(imp_stack).saveAsTiff(output_path)

    imp_stack = None
    stack = None

    return None


# Define the array of keywords to search for in the basename
keywords = ["CY5", "Confocal"]

# Find tif files
print("Finding .tif files")
matching_files = find_tif_files(directory)
print("Found {} tif files".format(len(matching_files)))

# Match the files to the keywords
print("Sorting filenames to keywords")
matching_files = match_files_to_keywords(matching_files, keywords)
print("Found {} keyword-matched tif files".format(len(matching_files)))

# Create dict with wellIDs
print("Organizing filenames by wellID")
matching_file_dict = categorize_into_wellnames(matching_files)

print("Starting image stacking")

# Stack images
final_stack_paths = []
for well in matching_file_dict:
    print("Starting to process {}".format(well))
    output_path = os.path.join(output_directory, "{}_AutoImageStack.tif".format(well))
    
    output = create_and_save_stack(matching_file_dict[well], well, output_path)
    if output is None:
        print("{} Stack created successfully:".format(well))
        final_stack_paths.append(output_path)
    else:
        print("ERROR: could not generate a stack for {}".format(well))

print("Stacks created! Output files: ")
for index, file in enumerate(final_stack_paths):
    index+=1
    print("\t{}. {}".format(index, file))
exit()