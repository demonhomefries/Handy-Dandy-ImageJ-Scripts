import os
import time
from ij import IJ
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

class Montage():
    def __init__(self):
        self.input_dir = ""
        self.output_dir = ""
        self.file_name = ""
        self.num_images = 0
        self.num_columns = 12
        self.num_rows = 8
        self.scale = 1
        self.font_size = 12

    def get_montage_parameters(self):
        while True:
            gd = GenericDialog("Generate montage parameters")
            gd.addDirectoryField("Input directory: ", self.input_dir, 50)
            gd.addDirectoryField("Output directory: ", self.output_dir, 50)
            gd.addStringField("Output filename: ", self.file_name, 50)
            gd.addNumericField("Number of Columns: ", self.num_columns, 0)
            gd.addNumericField("Number of Rows: ", self.num_rows, 0)
            gd.addNumericField("Scale: ", self.scale, 1)
            gd.addNumericField("Label font size: ", self.font_size, 0)

            gd.showDialog()

            self.input_dir = gd.getNextString()
            self.output_dir = gd.getNextString()
            self.file_name = gd.getNextString()
            self.num_columns = gd.getNextNumber()
            self.num_rows = gd.getNextNumber()
            self.scale = gd.getNextNumber()
            self.font_size = gd.getNextNumber()

            if gd.wasCanceled():
                print("get_montage_parameters was cancelled, restoring default values...")
                return None

            if os.path.isdir(self.input_dir):
                tif_filelist = find_tif_files(self.input_dir)
                self.num_images = len(tif_filelist)
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
                self.montage_parameters = self.input_dir, self.output_dir, self.file_name, self.num_images, self.num_columns, self.num_rows, self.scale, self.font_size
                return self.montage_parameters

    def confirm_settings(self):
        self.output_filepath = os.path.join(self.input_dir, self.file_name + ".tif")
        gd = GenericDialog("Confirm Montage Settings")
        gd.addMessage("Input directory:                        " + self.input_dir)
        gd.addMessage("# of images to montage:      " + str(int(self.num_images)))
        gd.addMessage("Output file:                               " + self.output_filepath)
        gd.addMessage("# of Columns:                         " + str(int(self.num_columns)))
        gd.addMessage("# of Rows:                                " + str(int(self.num_rows)))
        gd.addMessage("Scale:                                        " + str(self.scale))
        gd.addMessage("Label font size:                        " + str(int(self.font_size)))
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
    input_dir, output_dir, file_name, num_images, num_columns, num_rows, scale, font_size = settings

output_filepath = os.path.join(output_dir, file_name + ".tif")

print("\n\nGenerating Montage with settings:\nInput directory: {}\nOutput filepath: {}\nNumber of images: {}\nNumber of columns: {}\nNumber of rows: {}\nScale: {}\nFont size: {}".format(input_dir, output_filepath, num_images, num_columns, num_rows, scale, font_size))

imp = FolderOpener.open(input_dir, "")
montage = IJ.run(imp, "Make Montage...", "columns={} rows={} scale={} font={} label".format(num_columns, num_rows, scale, font_size))
IJ.saveAs(montage, "Tiff", output_filepath)
print("\n\nMontage generated successfully: {}".format(output_filepath))