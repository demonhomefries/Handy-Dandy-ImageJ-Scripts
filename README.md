# Handy-Dandy-ImageJ-Scripts
Useful single-run scripts for Fiji ImageJ's batch analysis of cell plates.

# Usage Notes
Image files MUST follow this Gen5 naming convention from the C10 for script-compatibility:<br />
<WELL>_<READ_STEP_SEQUENCE>_<CHANNEL_INDEX>_<IMAGE_IN_WELL_INDEX>_<CHANNEL>_<READ_INDEX>.tif<br />
Example: A1_01_1_1_DAPI_001.tif<br />

## Generate Montage (Generate Montage.py)
Creates customized montage images from a folder of source TIFs. UI-enabled. Drag-and-drop into ImageJ and click run.

## Batch File Rename (Batch File Rename.py)
Allows files from a folder and subdirectory to be batch-renamed. On first usage, enter the folder of interest and it will generate a manifest of files inside the folder in an Excel workbook. Enter the new filename for each file in the second column, exit the workbook and follow the prompts. Run in terminal with a command line interface.

## Montage Generator for Screens (Montage Generator for Screens.py)
Creates montaged images from a folder of source TIFs based on a specific well configuration for 384-well plates used for drug screens. UI-enabled. Drag-and-drop into ImageJ and click run.
