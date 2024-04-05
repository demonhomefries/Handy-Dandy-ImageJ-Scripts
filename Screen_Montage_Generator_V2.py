from javax.swing import JFrame, JPanel, JLabel, JButton, JList, JScrollPane, JFileChooser, JComboBox, JCheckBox, ButtonGroup, DefaultComboBoxModel, JTextField, JOptionPane, BoxLayout, JTable, AbstractCellEditor, DefaultListModel
from javax.swing.table import TableCellRenderer, TableCellEditor, DefaultTableModel
from java.awt import BorderLayout, FlowLayout, Component
from java.lang import Thread, InterruptedException, Object
from java.awt.event import ActionListener, WindowAdapter, WindowEvent
from java.io import File
from java.util import Vector, Date
from java.text import SimpleDateFormat

import os
import json
import random

class ComboBoxCellEditor(AbstractCellEditor, TableCellEditor):
    def __init__(self, gui):
        self.gui = gui
        # print("Debugging ComboBoxCellEditor __init__")
        # print(type(self.gui))
        self.comboBox = JComboBox()

    def getTableCellEditorComponent(self, table, value, isSelected, row, column):
        # Set the dropdown options based on the row
        #options = self.gui.dropdownOptions[row] if row < len(self.gui.dropdownOptions) else []
        directory = table.getModel().getValueAt(row, 0)
        options = self.gui.directoryToOptions.get(directory, [])
        self.comboBox.setModel(DefaultComboBoxModel(options))
        self.comboBox.setSelectedItem(value)
        return self.comboBox

    def getCellEditorValue(self):
        # Return the current value selected in the combo box
        return self.comboBox.getSelectedItem()
    

class WindowCloseListener(WindowAdapter):
    def __init__(self, app):
        self.app = app

    def windowClosed(self, windowEvent):
        self.app.windowClosed = True

class MontageGUI(ActionListener):

    def __init__(self):

        self.directoryToOptions = {}
        
        self.frame = JFrame("Montage Settings")
        self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.frame.setSize(600, 830)
        self.frame.setLayout(BorderLayout())

        # Directory Manager components
        self.tableModel = DefaultTableModel()
        self.tableModel.addColumn("Directory")
        self.tableModel.addColumn("Read Step")
        self.table = JTable(self.tableModel)
        comboBoxEditor = ComboBoxCellEditor(self)
        self.table.getColumnModel().getColumn(1).setCellEditor(comboBoxEditor)


        scrollPane = JScrollPane(self.table)

        # Buttons for Directory Manager
        directoryPanel = JPanel(FlowLayout(FlowLayout.CENTER))
        addButton = JButton("Add")
        addButton.addActionListener(self)
        directoryPanel.add(addButton)

        removeButton = JButton("Remove")
        removeButton.addActionListener(self)
        directoryPanel.add(removeButton)

        # Panel to hold the list and buttons
        directoryListPanel = JPanel(BorderLayout())
        directoryListPanel.add(scrollPane, BorderLayout.CENTER)
        directoryListPanel.add(directoryPanel, BorderLayout.SOUTH)

        # Panel to hold the directory list and other settings
        combinedNorthPanel = JPanel()
        combinedNorthPanel.setLayout(BoxLayout(combinedNorthPanel, BoxLayout.Y_AXIS))
        combinedNorthPanel.add(directoryListPanel)

        self.data = {
            "Compounds": ["Compound 1", "Compound 2", "Compound 3", "Compound 4", "All compounds"],
            "Concentrations": ["20uM", "6.33uM", "2.01uM", "0.634uM", "0.201uM", "0.0635uM", "0.0201uM", "0.0064uM", "0.002uM", "0.0006uM"]
        }
        
        # Sort by options
        sortPanel = JPanel(FlowLayout(FlowLayout.LEFT))
        self.compoundsCheckBox = JCheckBox("Compounds")
        self.concentrationsCheckBox = JCheckBox("Concentrations")
        self.checkBoxGroup = ButtonGroup()
        self.checkBoxGroup.add(self.compoundsCheckBox)
        self.checkBoxGroup.add(self.concentrationsCheckBox)
        self.compoundsCheckBox.addActionListener(self.updateDropdown)
        self.concentrationsCheckBox.addActionListener(self.updateDropdown)
        sortLabel = JLabel("Sort by: ")
        sortPanel.add(sortLabel)
        sortPanel.add(self.compoundsCheckBox)
        sortPanel.add(self.concentrationsCheckBox)
        combinedNorthPanel.add(sortPanel)

        # Dynamic Combo Panel
        dynamicComboPanel = JPanel(FlowLayout(FlowLayout.LEFT))
        dynamicComboLabel = JLabel("Select group to montage: ")
        self.dynamicCombo = JComboBox([])
        self.dynamicCombo.setEnabled(False)
        dynamicComboPanel.add(dynamicComboLabel)
        dynamicComboPanel.add(self.dynamicCombo)
        combinedNorthPanel.add(dynamicComboPanel)

        # PolyGR Combo Panel
        polyGRComboPanel = JPanel(FlowLayout(FlowLayout.LEFT))
        polyGRComboLabel = JLabel("Include/Exclude PolyGR: ")
        self.polyGRCombo = JComboBox(Vector(["Include", "Exclude"]))
        polyGRComboPanel.add(polyGRComboLabel)
        polyGRComboPanel.add(self.polyGRCombo)
        combinedNorthPanel.add(polyGRComboPanel)

        # Quadrants Combo Panel
        quadrantsComboPanel = JPanel(FlowLayout(FlowLayout.LEFT))
        quadrantsComboLabel = JLabel("Quadrants: ")
        self.quadrantsCombo = JComboBox(Vector(["Top left", "Top Right", "Bottom Left", "Bottom Right", "Random Quadrant", "All Quadrants"]))
        quadrantsComboPanel.add(quadrantsComboLabel)
        quadrantsComboPanel.add(self.quadrantsCombo)
        combinedNorthPanel.add(quadrantsComboPanel)

        # Channel Combo Panel
        channelComboPanel = JPanel(FlowLayout(FlowLayout.LEFT))
        channelComboLabel = JLabel("Channel to Montage: ")
        self.channelCombo = JComboBox(Vector(["Composite", "RFP", "GFP", "DAPI", "Bright Field"]))
        channelComboPanel.add(channelComboLabel)
        channelComboPanel.add(self.channelCombo)
        combinedNorthPanel.add(channelComboPanel)

        # Scale Panel
        scalePanel = JPanel(FlowLayout(FlowLayout.LEFT))
        scaleLabel = JLabel("Scale: ")
        self.scaleField = JTextField("1.0", 10)
        scalePanel.add(scaleLabel)
        scalePanel.add(self.scaleField)
        combinedNorthPanel.add(scalePanel)

        # Label Font Size Panel
        labelFontSizePanel = JPanel(FlowLayout(FlowLayout.LEFT))
        labelFontSizeLabel = JLabel("Label font size: ")
        self.labelFontSizeField = JTextField("12", 10)
        labelFontSizePanel.add(labelFontSizeLabel)
        labelFontSizePanel.add(self.labelFontSizeField)
        combinedNorthPanel.add(labelFontSizePanel)

        # Border Size Panel
        borderSizePanel = JPanel(FlowLayout(FlowLayout.LEFT))
        borderSizeLabel = JLabel("Border size (pixels): ")
        self.borderSizeField = JTextField("10", 10)
        borderSizePanel.add(borderSizeLabel)
        borderSizePanel.add(self.borderSizeField)
        combinedNorthPanel.add(borderSizePanel)

        # Function call to get current date-time string
        datetimestr = self.getDateTimeStr()

        # Output Directory Panel
        outputDirectoryPanel = JPanel(FlowLayout(FlowLayout.LEFT))
        outputDirectoryLabel = JLabel("Output directory: ")
        self.outputDirectoryField = JTextField(20)
        outputDirectoryButton = JButton("Browse")
        outputDirectoryButton.addActionListener(self.selectOutputDirectory)
        outputDirectoryPanel.add(outputDirectoryLabel)
        outputDirectoryPanel.add(self.outputDirectoryField)
        outputDirectoryPanel.add(outputDirectoryButton)
        combinedNorthPanel.add(outputDirectoryPanel)

        # Output Suffix Panel
        outputSuffixPanel = JPanel(FlowLayout(FlowLayout.LEFT))
        outputSuffixLabel = JLabel("Output suffix: ")
        self.outputSuffixField = JTextField("_Montaged_{}".format(datetimestr), 20)
        outputSuffixPanel.add(outputSuffixLabel)
        outputSuffixPanel.add(self.outputSuffixField)
        combinedNorthPanel.add(outputSuffixPanel)

        self.frame.add(combinedNorthPanel, BorderLayout.NORTH)

        # Create Montage button
        montageButtonPanel = JPanel(FlowLayout())
        self.montageButton = JButton("Create Montage")
        self.montageButton.addActionListener(self)
        montageButtonPanel.add(self.montageButton)

        self.frame.add(montageButtonPanel, BorderLayout.SOUTH)

        # Display the frame
        self.frame.setVisible(True)

        # Default to negative
        self.createMontageClicked = False

        self.windowClosed = False
        self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.frame.addWindowListener(WindowCloseListener(self))

    def actionPerformed(self, event):
        if self.table.isEditing():
            self.table.getCellEditor().stopCellEditing()

        command = event.getActionCommand()
        if command == "Create Montage":
            if self.validateSettings():
                self.showConfirmationDialog()
            return
        elif command == "Add":
            self.addDirectory()
        elif command == "Remove":
            self.removeDirectory()


    def validateSettings(self):
        try:
            # Validate Input Directories
            if self.tableModel.getRowCount() == 0:
                JOptionPane.showMessageDialog(self.frame, "No input directories have been added.", "Settings Error", JOptionPane.ERROR_MESSAGE)
                return False

            for i in range(self.tableModel.getRowCount()):
                directory = self.tableModel.getValueAt(i, 0)  # Get directory from the first column
                fileObj = File(directory)
                if not fileObj.isDirectory():
                    JOptionPane.showMessageDialog(self.frame, "The directory '{}' is not valid.".format(directory), "Settings Error", JOptionPane.ERROR_MESSAGE)
                    return False
        
            # Validate Output Suffix
            output_suffix = self.outputSuffixField.getText()
            if not output_suffix:
                JOptionPane.showMessageDialog(self.frame, "Output suffix cannot be empty.", "Settings Error", JOptionPane.ERROR_MESSAGE)
                return False

            # Validate Output Directory
            output_directory = self.outputDirectoryField.getText()
            if not output_directory:
                JOptionPane.showMessageDialog(self.frame, "Output directory cannot  be empty.", "Settings Error", JOptionPane.ERROR_MESSAGE)
                return False
            elif not os.path.isdir(output_directory):
                JOptionPane.showMessageDialog(self.frame, "Output directory is not a valid directory.", "Settings Error", JOptionPane.ERROR_MESSAGE)
                return False
        
            # Validate Sortby Selection
            if not self.compoundsCheckBox.isSelected() and not self.concentrationsCheckBox.isSelected():
                JOptionPane.showMessageDialog(self.frame, "Please select a 'Sort by:' option (Compounds or Concentrations).", "Settings Error", JOptionPane.ERROR_MESSAGE)
                return False

            # Validate Scale
            scale = float(self.scaleField.getText())
            if scale < 0.1 or scale > 1.0:
                JOptionPane.showMessageDialog(self.frame, "Scale value must contain a value between 0.1 and 1.0", "Settings Error", JOptionPane.ERROR_MESSAGE)
                return False

            # Validate Label Font Size
            label_font_size = int(self.labelFontSizeField.getText())
            if label_font_size < 0 or label_font_size > 200 or label_font_size is None or label_font_size == "":
                JOptionPane.showMessageDialog(self.frame, "Label font value must contain a value between 0 and 200", "Settings Error", JOptionPane.ERROR_MESSAGE)
                return False

            # Validate Border Size
            border_size = int(self.borderSizeField.getText())
            if border_size < 0 or border_size > 200:
                JOptionPane.showMessageDialog(self.frame, "Border size value must contain a value between 0 and 200", "Settings Error", JOptionPane.ERROR_MESSAGE)
                return False

        except ValueError as e:
            JOptionPane.showMessageDialog(self.frame, str(e))
            return False

        return True

    def updateDropdown(self, event):
        if self.compoundsCheckBox.isSelected():
            self.dynamicCombo.setModel(DefaultComboBoxModel(Vector(self.data["Compounds"])))
            self.dynamicCombo.setEnabled(True)
        elif self.concentrationsCheckBox.isSelected():
            self.dynamicCombo.setModel(DefaultComboBoxModel(Vector(self.data["Concentrations"])))
            self.dynamicCombo.setEnabled(True)
        else:
            self.dynamicCombo.setModel(DefaultComboBoxModel([]))
            self.dynamicCombo.setEnabled(False)

    def updateDropdownForRow(self, rowIndex, options):
        # self.table.getColumnModel().getColumn(1).setCellEditor(comboBoxEditor)
        # Update the options in the directory-to-options mapping
        directory = self.tableModel.getValueAt(rowIndex, 0)
        self.directoryToOptions[directory] = options

        # Repaint the table to reflect the change
        self.table.repaint()

    def addDirectory(self):
        chooser = JFileChooser()
        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
        if hasattr(self, 'lastSelectedDirectory') and self.lastSelectedDirectory is not None:
            chooser.setCurrentDirectory(File(self.lastSelectedDirectory).getParentFile())
        returnValue = chooser.showOpenDialog(self.frame)

        if returnValue == JFileChooser.APPROVE_OPTION:
                directory = chooser.getSelectedFile().getAbsolutePath()
                read_steps = get_kinetic_read_list(directory)
                read_steps_str = [str(step) for step in read_steps]

                # Add dropdown options for this row to the list
                # self.dropdownOptions.append(read_steps_str)
                self.directoryToOptions[directory] = read_steps_str
                
                # Add the directory to the table with a default option
                self.tableModel.addRow([directory, read_steps_str[0] if read_steps_str else "No steps found"])

                # Update the dropdown for the new row
                rowIndex = self.tableModel.getRowCount() - 1  # Index of the new row
                self.updateDropdownForRow(rowIndex, read_steps_str)

                self.lastSelectedDirectory = directory

                # Update the dropdown for the new row
                rowIndex = self.tableModel.getRowCount() - 1  # Index of the new row
                self.updateDropdownForRow(rowIndex, read_steps_str)

    def removeDirectory(self):
        selectedRow = self.table.getSelectedRow()
        if selectedRow >= 0:
            directory = self.tableModel.getValueAt(selectedRow, 0)
            if directory in self.directoryToOptions:
                del self.directoryToOptions[directory]
            self.tableModel.removeRow(selectedRow)



    def getDirectoryList(self):
        return [(self.tableModel.getValueAt(i, 0), self.tableModel.getValueAt(i, 1)) for i in range(self.tableModel.getRowCount())]

    def processDirectories(self):
        directory_list = self.getDirectoryList()
        print("Selected directories:", directory_list)
        if len(directory_list) < 1:
            print("User has not selected any directories, exiting script...")
        self.closeWindow()
            
    def getDateTimeStr(self):
        dateFormat = SimpleDateFormat("ddMMMyyyy-HHmm")
        return dateFormat.format(Date())

    def selectOutputDirectory(self, event):
        chooser = JFileChooser()
        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
        returnValue = chooser.showOpenDialog(self.frame)
        if returnValue == JFileChooser.APPROVE_OPTION:
            directory = chooser.getSelectedFile()
            self.outputDirectoryField.setText(directory.getAbsolutePath())
        
    def showConfirmationDialog(self):
        settingsPanel = JPanel()
        settingsPanel.setLayout(BoxLayout(settingsPanel, BoxLayout.Y_AXIS))

        # Add components to settingsPanel for each setting
        # Input Directories
        if self.tableModel.getRowCount() > 0:
            inputDirs = "<html><b>Input Plate Directories:</b><br>" + "<br>".join([self.tableModel.getValueAt(i, 0) for i in range(self.tableModel.getRowCount())]) + "</html>"
            settingsPanel.add(JLabel(inputDirs))

        # Output Directory
        settingsPanel.add(JLabel("<html><b>Output directory:</b> " + self.getOutputDirectory() + "</html>"))

        # Output Suffix
        settingsPanel.add(JLabel("<html><b>Output suffix:</b> " + self.getOutputSuffix() + "</html>"))

        # Sort By
        sortBy = "Compounds" if self.getSelectedCompounds() else "Concentrations"
        settingsPanel.add(JLabel("<html><b>Sort by:</b> " + sortBy + "</html>"))

        # Dynamic Combo
        if self.getSelectedCompounds():
            settingsPanel.add(JLabel("<html><b>Compound selected:</b> " + self.getDynamicComboValue() + "</html>"))
        elif self.getSelectedConcentrations():
            settingsPanel.add(JLabel("<html><b>Concentration selected:</b> " + self.getDynamicComboValue() + "</html>"))

        # Other Settings
        settingsPanel.add(JLabel("<html><b>PolyGR:</b> " + self.getPolyGRComboValue() + "</html>"))
        settingsPanel.add(JLabel("<html><b>Quadrant:</b> " + self.getQuadrantsComboValue() + "</html>"))
        settingsPanel.add(JLabel("<html><b>Channel:</b> " + self.getChannelComboValue() + "</html>"))
        settingsPanel.add(JLabel("<html><b>Scale:</b> " + self.getScaleValue() + "</html>"))
        settingsPanel.add(JLabel("<html><b>Label font size:</b> " + self.getLabelFontSize() + "</html>"))
        settingsPanel.add(JLabel("<html><b>Border pixel size:</b> " + self.getBorderSize() + "</html>"))

        # Show confirmation dialog
        option = JOptionPane.showConfirmDialog(self.frame, settingsPanel, "Confirm Settings", JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE)

        # OK button pressed
        if option == JOptionPane.OK_OPTION:
            self.createMontageClicked = True
            self.frame.dispose()
        # Cancel button pressed - keep the application window open for modifications

    def getScaleValue(self):
        return self.scaleField.getText()

    def getLabelFontSize(self):
        return self.labelFontSizeField.getText()

    def getBorderSize(self):
        return self.borderSizeField.getText()

    def getOutputDirectory(self):
        return self.outputDirectoryField.getText()

    def getOutputSuffix(self):
        return self.outputSuffixField.getText()

    def getSelectedCompounds(self):
        return self.compoundsCheckBox.isSelected()

    def getSelectedConcentrations(self):
        return self.concentrationsCheckBox.isSelected()

    def getDynamicComboValue(self):
        return self.dynamicCombo.getSelectedItem()

    def getPolyGRComboValue(self):
        return self.polyGRCombo.getSelectedItem()

    def getQuadrantsComboValue(self):
        return self.quadrantsCombo.getSelectedItem()

    def getChannelComboValue(self):
        return self.channelCombo.getSelectedItem()
    
    def getAllSettings(self):
            # Retrieve all settings and return them
            return {
                "input_directory_list": self.getDirectoryList(), # Returns a list of tuples.
                "output_directory": self.getOutputDirectory(),
                "output_suffix": self.getOutputSuffix(),
                "sortby_value": self.getDynamicComboValue(),
                "compounds_selected": self.getSelectedCompounds(),
                "concentration_selection": self.getSelectedConcentrations(),
                "polygr_selection": self.getPolyGRComboValue(),
                "quadrant_selection": self.getQuadrantsComboValue(),
                "channel_selection": self.getChannelComboValue(),
                "scale": self.getScaleValue(),
                "label_font_size": self.getLabelFontSize(),
                "border_size": self.getBorderSize()
            }

def get_montage_settings(printout=False):
    gui = MontageGUI()
    gui.frame.setVisible(True)

    # Wait for the user to click Create Montage or close the window
    while not gui.createMontageClicked and not gui.windowClosed:
        try:
            Thread.sleep(100)
        except InterruptedException:
            break

    if gui.createMontageClicked:
        settings = gui.getAllSettings()
        return settings
    elif gui.windowClosed:
        print("Window closed by the user.")
        return None  # or exit the script as needed
    
def get_kinetic_read_list(directory):
    tif_files = find_tif_files_surfacedir(directory)
    if tif_files is None:
        print("ERROR get_kinetic_read_list: Could not find any .tif files")
        exit()
    unique_read_steps = []
    try:
        for file in tif_files:
            basename = os.path.basename(file)
            filename, ext = os.path.splitext(basename)
            filename_elements = filename.split("_")
            read_step = int(filename_elements[5]) # assumes read step number is 6th element in the underscore-delimited name
            if read_step not in unique_read_steps:
                unique_read_steps.append(read_step)
        unique_read_steps.sort()
    except Exception as e:
        unique_read_steps = ["Invalid: no read steps"]

    return unique_read_steps

def load_dict(wellID_config_fp):
    with open(wellID_config_fp, "r") as readfile:
        wellid_config = json.load(readfile)
        print("Successfully loaded wellID config from {}".format(wellID_config_fp))

def find_tif_files_surfacedir(directory):
    tif_files = []
    for item in os.listdir(directory):
        # Construct full file path
        full_path = os.path.join(directory, item)
        # Check if it's a file and has .tif extension
        if item.endswith('.tif'):
            #print(f"Adding {full_path} to list!")
            tif_files.append(full_path)
    if len(tif_files) < 1:
        tif_files = ["Invalid: no TIFs found"]
    return tif_files

def extract_well_id(filename):
    # Split the filename using underscore as a delimiter (this naming convention should not change from the Gen5 output)
    parts = filename.split('_')
    # Well ID is identified as a len >= 2 string where the first character is a number and subsequent characters are digits
    for part in parts:
        if len(part) >= 2 and part[0].isalpha() and part[1:].isdigit():
            return part
    # If well_id is not found, return None to be processed as an error
    return None

def isolate_wellIDs(settings, wellid_config):
    eligible_wellids = {}

    if settings["concentration_selection"] is False and settings["compounds_selected"] is True:
        compound = settings["sortby_value"]
        compound = compound.replace(" ", "")

        if settings["polygr_selection"] == "Include":
            gr_key = "1.8uMPolyGR"
        elif settings["polygr_selection"] == "Exclude":
            gr_key = "0uM"
        else:
            print("ERROR isolate_wellIDs: Settings returned polygr_selection as neither Include or Exclude")
            exit()

        # Ensuring that the keys and their nested structure exist
        if compound not in eligible_wellids:
            eligible_wellids[compound] = {}
        if gr_key not in eligible_wellids[compound]:
            eligible_wellids[compound][gr_key] = {}

        for sortby, value in wellid_config[compound][gr_key].items():
            eligible_wellids[compound][gr_key][sortby] = value

    elif settings["concentration_selection"] is True and settings["compounds_selected"] is False:
        if settings["polygr_selection"] == "Include":
            gr_key = "1.8uMPolyGR"
        elif settings["polygr_selection"] == "Exclude":
            gr_key = "0uM"

        sortby = settings["sortby_value"]

        for compound, value in wellid_config.items():
            if "Compound" in compound:
                # Extract the desired value
                eligible_value = value.get(gr_key, {}).get(sortby)
                if eligible_value is not None:
                    # Store the value in a nested structure
                    if compound not in eligible_wellids:
                        eligible_wellids[compound] = {}
                    if gr_key not in eligible_wellids[compound]:
                        eligible_wellids[compound][gr_key] = {}
                    
                    eligible_wellids[compound][gr_key][sortby] = eligible_value
    
    return eligible_wellids

def isolate_quadrants(settings, isolated_wellids):
    quadrant = settings["quadrant_selection"]
    selected_wellIDs = {}

    for compound, gr_dict in isolated_wellids.items():
        for gr_key, sortby_dict in gr_dict.items():
            if compound not in selected_wellIDs:
                selected_wellIDs[compound] = {}
            if gr_key not in selected_wellIDs[compound]:
                selected_wellIDs[compound][gr_key] = {}

            for sortby, well_list in sortby_dict.items():
                if quadrant.lower() == "all":
                    selected_wellIDs[compound][gr_key][sortby] = well_list
                elif quadrant.lower() == "top left":
                    selected_wellIDs[compound][gr_key][sortby] = [well_list[0]]
                elif quadrant.lower() == "top right":
                    selected_wellIDs[compound][gr_key][sortby] = [well_list[1]]
                elif quadrant.lower() == "bottom left":
                    selected_wellIDs[compound][gr_key][sortby] = [well_list[2]]
                elif quadrant.lower() == "bottom right":
                    selected_wellIDs[compound][gr_key][sortby] = [well_list[3]]
                elif quadrant.lower() == "random":
                    random_number = random.randint(0, 3)
                    selected_wellIDs[compound][gr_key][sortby] = [well_list[random_number]]
                else:
                    print("ERROR get_specified_wellID: quadrant value was not recognized: {}".format(quadrant))
                    return None

    return selected_wellIDs

def filter_eligible_tifs(settings, directory, kinetic_readstep):
    """
    Function is meant to be used in a loop - once per directory (easier data management)
    Filters the .tif files once using the kinetic read step and the channel selection
    Assumes read step number is 6th element in the underscore-delimited name: basename_elements[5]
    Assumes channel ID is 5th element in the underscore-delimited name: basename_elements[4]
    """
    kinetic_readstep = int(kinetic_readstep)
    filtered_filelist = []
    channel_id = settings["channel_selection"]
    file_list = find_tif_files_surfacedir(directory)
    for file in file_list:
        basename = os.path.basename(file)
        filename, ext = os.path.splitext(basename)
        basename_elements = filename.split("_")
        basename_readstep = int(basename_elements[5])
        if basename_readstep == kinetic_readstep: # Check that the sixth element (which should be the readstep) matches the selected readstep            
            if channel_id in basename_elements[4]: # Check that the fifth element (which should be the name) matches the selected channel ID
                filtered_filelist.append(file)
    
    if len(filtered_filelist) < 1:
        print("ERROR filter_eligible_tifs: module could either not find kinetic_readstep ({}) or channel_id ({}) for the files in the directory: {}".format(kinetic_readstep, channel_id, directory))

    return filtered_filelist

def match_tifs_to_wellIDs(eligible_tifs, eligible_wellIDs):
    
    for file in eligible_tifs:
        basename = os.path.basename(file)
        filename, ext = os.path.splitext(basename)
        extracted_wellid = extract_well_id(filename)

        for compound, dosages in eligible_wellIDs.items():
            for dosage, wells in dosages.items():
                for concentration, well_ids in wells.items():
                    wells[concentration] = [file if well_id == extracted_wellid else well_id for well_id in well_ids]

    return eligible_wellIDs

settings = get_montage_settings()
print("Captured Montage Settings")
if settings is None:
    print("Captured no settings")
print(settings)

        
wellid_config = load_dict(wellID_config_fp)
print(wellid_config)
exit()

for directory_tuple in settings["input_directory_list"]:
    directory, read_step = directory_tuple
    # Filter out the wellIDs according to concentration/compound & PolyGR +/-
    isolated_wellIDs = isolate_wellIDs(settings, wellid_config)
    # Further filter out the wellIDs based on quadrant selection
    isolated_quadrants = isolate_quadrants(settings, isolated_wellIDs)
    print(isolated_quadrants)
    eligible_tifs = filter_eligible_tifs(settings, directory, read_step)
    print(eligible_tifs)
    quadrant_filedict = match_tifs_to_wellIDs(eligible_tifs, isolated_quadrants)
    print(quadrant_filedict)


    with open(r"C:\Users\akmishra\Desktop\kachow.json", "w") as writefile:
        json.dump(quadrant_filedict, writefile, indent=4)
        print("Successfully loaded wellID config")


