import os
import time
import random
import shutil
from ij import IJ, ImageStack, ImagePlus
from ij.gui import GenericDialog
from ij.plugin import FolderOpener

def find_tif_files(directory):
    tif_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.tif'):
                #print(f"Adding {filename} to list!")
                tif_files.append(os.path.join(root, filename))

    return tif_files

def find_tif_files_surfacedir(directory):
    tif_files = []
    for item in os.listdir(directory):
        # Construct full file path
        full_path = os.path.join(directory, item)
        # Check if it's a file and has .tif extension
        if item.endswith('.tif'):
            #print(f"Adding {full_path} to list!")
            tif_files.append(full_path)

    return tif_files

def warning_dialog(message):
    # Set up a dialog box and 
    warning_dialog = GenericDialog("Warning")
    warning_dialog.addMessage(message)
    warning_dialog.showDialog()

def get_384_quadrant_wellID(quadrant):
    # Dictionary 
    quadrant_transform = {
        "Top Left": (0, 0),
        "Top Right": (0, 1),
        "Bottom Left": (1, 0),
        "Bottom Right": (1, 1)
    }

    well_ids = []
    for row in range(1, 17, 2):  # Skip every other row to match the 96-well layout
        for col in range(1, 25, 2):  # Skip every other column
            if quadrant != "Random":
                # Calculate row and column for the specific quadrant
                delta_row, delta_col = quadrant_transform[quadrant]
                well_id = "{}{}".format(chr(64 + row + delta_row), col + delta_col)
                well_ids.append(well_id)
            else:
                # Select a random well from the 2x2 block
                delta_row, delta_col = random.choice(list(quadrant_transform.values()))
                well_id = "{}{}".format(chr(64 + row + delta_row), col + delta_col)
                well_ids.append(well_id)

    return well_ids

def sort_montage_images(filelist, sort_order):
    pass

def create_stack(filelist):
    stack = None
    for filepath in filelist:
        img = IJ.openImage(filepath)
        if stack is None:
            # Initialize the stack with the first image
            stack = ImageStack(img.getWidth(), img.getHeight())
        stack.addSlice(img.getProcessor())
        print("Added slice {}".format(filepath))
    print("Stack Generated")
    # Create an ImagePlus object with the stack and show it
    stackedImage = ImagePlus("Stacked Image", stack)
    stackedImage.show()
    return stackedImage


class Montage():
    def __init__(self):
        self.input_dir = ""
        self.output_dir = ""
        self.file_name = ""
        self.num_images = 0
        self.num_columns = 12
        self.num_rows = 8
        self.mode_options = ["96-Well", "384-Well", "384w to 96w", "All Images"]
        self.mode_selection = self.mode_options[1]
        self.quadrant_options = ["Top Left", "Top Right", "Bottom Left", "Bottom Right", "Random"]
        self.quadrant_selection = self.quadrant_options[0]
        self.scale = 1
        self.font_size = 12
        self.border_value = 0
        self.search_subdir = False
        self.tif_filelist = None

    def get_montage_parameters(self):
        while True:
            gd = GenericDialog("Montage parameters")
            gd.addDirectoryField("Input directory: ", self.input_dir, 50)
            gd.addCheckbox("Include TIFs from subdirectories", self.search_subdir)
            gd.addMessage("")
            gd.addNumericField("Number of Columns: ", self.num_columns, 0)
            gd.addNumericField("Number of Rows: ", self.num_rows, 0)
            gd.addChoice("Mode: ", self.mode_options, self.mode_selection)
            gd.addMessage("Quadrant options are usable only when \"384-Well\" or \"384w to 96w\" modes are selected")
            gd.addChoice("Quadrant: ", self.quadrant_options, self.quadrant_selection)
            gd.addNumericField("Scale: (1.0-0.1)", self.scale, 1)
            gd.addNumericField("Label font size: ", self.font_size, 0)
            gd.addNumericField("Border size (pixels): ", self.border_value, 0)
            gd.addDirectoryField("Output directory: ", self.output_dir, 50)
            gd.addStringField("Output filename: ", self.file_name, 50)

            gd.showDialog()

            self.input_dir = gd.getNextString()
            self.search_subdir = gd.getNextBoolean()
            self.num_columns = gd.getNextNumber()
            self.num_rows = gd.getNextNumber()
            self.quadrant_selection = gd.getNextChoice()
            self.scale = gd.getNextNumber()
            self.font_size = gd.getNextNumber()
            self.border_value = gd.getNextNumber()
            self.output_dir = gd.getNextString()
            self.file_name = gd.getNextString()

            if gd.wasCanceled():
                print("get_montage_parameters was cancelled, restoring default values...")
                return None

            
            if os.path.isdir(self.input_dir):
                if self.search_subdir is True:
                    self.tif_filelist = find_tif_files(self.input_dir)
                elif self.search_subdir is False:
                    self.tif_filelist = find_tif_files_surfacedir(self.input_dir)
                self.num_images = len(self.tif_filelist)
                if self.num_images < 1:
                    warning_dialog(str(self.input_dir) + "Contains 0 tif files. Please choose a directory with 1 or more .tifs")
                    continue
            else:
                warning_dialog("Please choose a valid input directory")
                continue

            if not os.path.isdir(self.output_dir):
                warning_dialog("Please choose a valid output directory")
                continue

            if self.num_columns <= 0:
                warning_dialog("Number of columns must be 1 or above")
                continue

            if self.num_rows <= 0:
                warning_dialog("Number of rows must be 1 or above")
                continue
            if self.num_rows * self.num_columns < self.num_images:
                warning_dialog("{} rows x {} columns = {} plates. This is fewer than the {} images in your directory.\nPlease enter an appropriate number of rows and columns to contain all your images.".format(self.num_rows, self.num_columns, self.num_rows * self.num_columns, self.num_images))
                continue

            confirmation = self.confirm_settings()
            if confirmation:
                self.montage_parameters = self.input_dir, self.output_dir, self.file_name, self.num_images, self.num_columns, self.num_rows, self.quadrant_selection, self.scale, self.font_size, self.border_value, self.tif_filelist
                return self.montage_parameters

    def confirm_settings(self):
        self.output_filepath = os.path.join(self.input_dir, self.file_name + ".tif")
        gd = GenericDialog("Confirm Montage Settings")
        gd.addMessage("Input directory:                        " + self.input_dir)
        gd.addMessage("# of images to montage:      " + str(int(self.num_images)))
        gd.addMessage("Output file:                               " + self.output_filepath)
        gd.addMessage("# of Columns:                         " + str(int(self.num_columns)))
        gd.addMessage("# of Rows:                                " + str(int(self.num_rows)))
        gd.addMessage("384w Quadrant:                            " + str(self.quadrant_selection))
        gd.addMessage("Scale:                                        " + str(self.scale))
        gd.addMessage("Label font size:                        " + str(int(self.font_size)))
        gd.addMessage("Border size (pixels):                   " + str(int(self.border_value)))
        gd.addMessage("\n\nIf the settings above are correct, click OK to continue.\nTo revise these settings, click Cancel.")
        gd.showDialog()

        if gd.wasOKed():
            return True
        elif gd.wasCanceled():
            return False

montage_instance = Montage()
settings = montage_instance.get_montage_parameters()

if settings is None:
    print("No settings recorded")
    exit()
else:
    input_dir, output_dir, file_name, num_images, num_columns, num_rows, quadrant_selection, scale, font_size, border_size, tif_filelist = settings

output_filepath = os.path.join(output_dir, file_name + ".tif")

print("\n\nGenerating Montage with settings:\nInput directory: {}\nOutput filepath: {}\nNumber of images: {}\nNumber of columns: {}\nNumber of rows: {}\nScale: {}\nFont size: {}\nQuadrant: {}\nBorder size: {}".format(input_dir, output_filepath, num_images, num_columns, num_rows, scale, font_size, quadrant_selection, border_size))

if tif_filelist is None:
    print("ERROR: internal code issue, tif_filelist was None")
    exit()

sorted_file_list = sort_montage_images(tif_filelist, quadrant_selection)
stack = create_stack(sorted_file_list)

command = "Make Montage...", "columns={} rows={} scale={} font={} border={} label".format(num_columns, num_rows, scale, font_size, border_size)
montage = IJ.run(stack, command)
IJ.saveAs(montage, "Tiff", output_filepath)
print("\n\nMontage generated successfully: {}".format(output_filepath))