# Image calibration settings (automate?)
microns_per_pixel = 0.325

# Threshold detector settings
detectorSettings = {
    'TARGET_CHANNEL': 1,
    'SIMPLIFY_CONTOURS': False,
    'INTENSITY_THRESHOLD': 100.0
}

# Area filter settings
featureFilterSettings = {
    'FEATURE': 'AREA',
    'IS_ABOVE': False, # Change True to False if filtering spots below threshold
    'THRESHOLD': 50.0,
}

# Kalman tracker settings
kalmanSettings = {
    'LINKING_MAX_DISTANCE': 5.0,
    'KALMAN_SEARCH_RADIUS': 5.0,
    'MAX_FRAME_GAP': 2
}

csv_merger_filepath = r"C:\Users\akmishra\Desktop\Batch Kalman TrackMate\Track-Spot_Merger_Auto.py"













import os
import sys
import shutil
import subprocess
from ij import IJ
from java.io import File
from ij.gui import GenericDialog
from ij.plugin import FolderOpener
from ij.measure import Calibration
from fiji.plugin.trackmate.io import TmXmlWriter
from fiji.plugin.trackmate.features import FeatureFilter
from fiji.plugin.trackmate.detection import ThresholdDetectorFactory
from fiji.plugin.trackmate.visualization.table import TrackTableView
from fiji.plugin.trackmate.gui.displaysettings import DisplaySettings
from fiji.plugin.trackmate.tracking.kalman import KalmanTrackerFactory
from fiji.plugin.trackmate import TrackMate, Model, Settings, Logger, SelectionModel

def warning_dialog(message):
    # Set up a dialog box and 
    warning_dialog = GenericDialog("Warning")
    warning_dialog.addMessage(message)
    warning_dialog.showDialog()

def find_tif_files(directory):
    tif_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.tif'):
                #print(f"Adding {filename} to list!")
                tif_files.append(os.path.join(root, filename))

    return tif_files

def find_csv_files(directory):
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.csv'):
                #print(f"Adding {filename} to list!")
                csv_files.append(os.path.join(root, filename))

    return csv_files

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

def replicate_folder_structure(input_dir, output_dir):
    # Create the output directory with "_autotracked" suffix
    base_output_dir = os.path.basename(os.path.normpath(input_dir))
    print("Basename: {}".format(base_output_dir))
    autotracked_dir = os.path.join(output_dir, base_output_dir + "_autotracked")

    # Create the base autotracked directory if it doesn't exist
    if not os.path.exists(autotracked_dir):
        os.makedirs(autotracked_dir)

    # Walk through the input directory and replicate the structure
    for root, dirs, files in os.walk(input_dir):
        # Create the corresponding directory structure in the autotracked directory
        relative_path = os.path.relpath(root, input_dir)
        target_path = os.path.join(autotracked_dir, relative_path)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

    #print("Folder structure replicated from '{}' to '{}'".format(input_dir, autotracked_dir))
    return autotracked_dir

def get_settings():
    input_dir = ""
    search_subdir = False
    output_dir = ""
    save_xml = False
    while True:
        gd = GenericDialog("Generate montage parameters")
        gd.addDirectoryField("Input directory: ", input_dir, 50)
        gd.addCheckbox("Search subdirectories", search_subdir)
        gd.addMessage("")
        gd.addDirectoryField("Output directory: ", output_dir, 50)
        gd.addCheckbox("Save XML", save_xml)


        gd.showDialog()

        input_dir = gd.getNextString()
        output_dir = gd.getNextString()
        search_subdir = gd.getNextBoolean()
        save_xml = gd.getNextBoolean()

        if gd.wasCanceled():
            print("get_montage_parameters was cancelled, restoring default values...")
            return None

        if os.path.isdir(input_dir):
            if search_subdir is True:
                tif_filelist = find_tif_files(input_dir)
            elif search_subdir is False:
                tif_filelist = find_tif_files_surfacedir(input_dir)
            num_images = len(tif_filelist)
            if num_images < 1:
                warning_dialog(str(input_dir) + "Contains 0 tif files. Please choose a directory with 1 or more .tifs")
                continue
        else:
            warning_dialog("Please choose a valid input directory")
            continue

        if not os.path.isdir(output_dir):
            warning_dialog("Please choose a valid output directory")
            continue

        return input_dir, tif_filelist, output_dir, save_xml


# Ensure the CSV Merger file is in the appropriate place
if not os.path.isfile(csv_merger_filepath):
    print("Could not find the CSV Merger file! Last known filepath: {}".format(csv_merger_filepath))
    exit()
    
# Retrieve settings for the run
input_dir, tif_filelist, output_dir, save_xml = get_settings()

# Create new folders for the output
autotracked_dir = replicate_folder_structure(input_dir, output_dir)
if not os.path.isdir(autotracked_dir):
    print("Something went wrong replicating the folder structure. Exiting script...")
    exit()
else:
    print("New folder structure generated successfully! {}".format(autotracked_dir))

print("output_dir: {}".format(output_dir))
print("input_dir: {}".format(input_dir))
print("autotracked_dir: {}".format(autotracked_dir))





# New list of tuples to collect completed files
tables_generated = []
for index, image in enumerate(tif_filelist):

    image_name = os.path.splitext(os.path.basename(image))[0]
    # replace the input name for the autotracked name, the rest of the folder structure should be the same since it was replicated
    input_dirname = os.path.dirname(image)
    final_output_dir = input_dirname.replace(input_dir, autotracked_dir)

    # In case there are any trailing backslashes
    if input_dir.endswith("\\"):
        input_dir = input_dir[:-1]

    # Get the output names
    spot_table_csv_filepath = os.path.join(final_output_dir, image_name + "_spottable_auto.csv")
    spot_table_csv_file = File(spot_table_csv_filepath)
    track_table_csv_filepath = os.path.join(final_output_dir, image_name + "_tracktable_auto.csv")
    track_table_csv_file = File(track_table_csv_filepath)

    print("spot_table_csv_filepath: {}".format(spot_table_csv_filepath))
    print("track_table_csv_filepath: {}".format(track_table_csv_filepath))

    xml_file = File(os.path.join(final_output_dir, image_name + "_auto.xml"))

    print("Starting to process image {}/{}".format(index +1, len(tif_filelist), image_name))

    # Open image
    imp = IJ.openImage(image)

    # Set image calibration to microns
    cal = Calibration()
    cal.pixelWidth = microns_per_pixel
    cal.pixelHeight = microns_per_pixel
    imp.setCalibration(cal)

    # Initialize model
    model = Model()
    # Set the units to microns
    model.setPhysicalUnits("microns", "seconds")
    # Log stuff
    logger = Logger.IJ_LOGGER
    model.setLogger(logger)

    # Get settings from the image
    settings = Settings(imp)

    # Threshold detector
    settings.detectorFactory = ThresholdDetectorFactory()
    settings.detectorSettings = {
        'TARGET_CHANNEL': detectorSettings["TARGET_CHANNEL"],
        'SIMPLIFY_CONTOURS': detectorSettings["SIMPLIFY_CONTOURS"],
        'INTENSITY_THRESHOLD': detectorSettings["INTENSITY_THRESHOLD"]
    }


    # Area filter of 15 units 
    filter1 = FeatureFilter(featureFilterSettings["FEATURE"], featureFilterSettings["THRESHOLD"], featureFilterSettings["IS_ABOVE"]) 
    settings.addSpotFilter(filter1)


    # Kalman tracker
    settings.trackerFactory = KalmanTrackerFactory()
    settings.trackerSettings = {
        'LINKING_MAX_DISTANCE': kalmanSettings["LINKING_MAX_DISTANCE"],
        'KALMAN_SEARCH_RADIUS': kalmanSettings["KALMAN_SEARCH_RADIUS"],
        'MAX_FRAME_GAP': kalmanSettings["MAX_FRAME_GAP"]
    }

    # Retrieve data from all the analyzers for output similar to GUI
    settings.addAllAnalyzers()

    # Instantiate TrackMate
    trackmate = TrackMate(model, settings)


    # Validate the inputs
    ok = trackmate.checkInput()
    if not ok:
        sys.exit(str(trackmate.getErrorMessage()))

    # Process the image with the settings
    print("\tStarting analysis")
    ok = trackmate.process()
    if not ok:
        sys.exit(str(trackmate.getErrorMessage()))

    sm = SelectionModel(model)
    ds = DisplaySettings()

    # relative_path = os.path.relpath(os.path.dirname(image), input_dir)
    # spot_table_csv_file = File(os.path.join(autotracked_dir, relative_path, image_name + "_spottable_auto.csv"))
    # track_table_csv_file = File(os.path.join(autotracked_dir, relative_path, image_name + "_tracktable_auto.csv"))
    # xml_file = File(os.path.join(autotracked_dir, relative_path, image_name + "_auto.xml"))

    # Working exports
    track_table_view = TrackTableView(trackmate.getModel(), sm, ds)
    track_table_view.getSpotTable().exportToCsv(spot_table_csv_file)
    print("\tSaved spot table to " + spot_table_csv_filepath)
    track_table_view.getTrackTable().exportToCsv(track_table_csv_file)
    print("\tSaved track table to " + track_table_csv_filepath)

    tables_generated.append((spot_table_csv_file, track_table_csv_file))

    # Close the image or you're gonna eat tons of ram
    imp.close()

    if save_xml:
        writer = TmXmlWriter(xml_file)
        print(type(model.getLogger().toString()))
        writer.appendLog(model.getLogger().toString())
        writer.appendModel( model )
        writer.appendSettings( settings )
        writer.appendDisplaySettings( ds )
        writer.writeToFile()
        print("Saved XML")

    autotracked_dir # new directory
    output_dir = os.path.join(autotracked_dir)

    # Create the merge command
    print("Executing merge with Python file at {}".format(csv_merger_filepath))
    csv_list_argument = "\"{},{}\"".format(spot_table_csv_file, track_table_csv_file)
    csv_merger_script_fp = "\"" + csv_merger_filepath + "\""
    command = "python " + csv_merger_script_fp + " --csvlist " + str(csv_list_argument)

    # Execute the command
    try:
        output_message = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        output_message = output_message.decode('utf-8')
        print(output_message)
    except subprocess.CalledProcessError as e:
        print("ERROR Track-Spot_Merger_Auto failed: ")
        print("Command: {}".format(command))
        print(e.output.decode('utf-8'))

    # Old code:
    # print(command)
    # output_message = subprocess.run(command, capture_output=True, text=True)
    # if output_message.returncode != 0:
    #     print("ERROR Track-Spot_Merger_Auto failed: ")
    #     print("Command: {}".format(command))
    #     print(output_message.stdout)
    #     print(output_message.stderr)

    # print(output_message.stdout)
