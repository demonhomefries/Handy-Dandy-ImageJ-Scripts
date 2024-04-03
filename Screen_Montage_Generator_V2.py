
# # from javax.swing import JFrame, JPanel, JLabel, JButton, JList, JScrollPane, JFileChooser, JComboBox, JCheckBox, ButtonGroup, DefaultComboBoxModel, JTextField, JOptionPane, BoxLayout
# # from java.lang import Thread, InterruptedException
# # from java.awt import BorderLayout, FlowLayout
# # from javax.swing import DefaultListModel
# # from java.awt.event import ActionListener
# # from java.io import File
# # from java.util import Vector
# # from java.text import SimpleDateFormat
# # from java.util import Date
# # from java.awt.event import WindowAdapter, WindowEvent
# # import os
# # import json
# # import random


# # class WindowCloseListener(WindowAdapter):
# #     def __init__(self, app):
# #         self.app = app

# #     def windowClosed(self, windowEvent):
# #         self.app.windowClosed = True

# # class Application(ActionListener):

# #     def __init__(self):
# #         self.frame = JFrame("Montage Settings")
# #         self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
# #         self.frame.setSize(500, 600)
# #         self.frame.setLayout(BorderLayout())

# #         # Directory Manager components
# #         self.listModel = DefaultListModel()
# #         self.list = JList(self.listModel)
# #         scrollPane = JScrollPane(self.list)

# #         # Buttons for Directory Manager
# #         directoryPanel = JPanel(FlowLayout(FlowLayout.LEFT))
# #         addButton = JButton("Add")
# #         addButton.addActionListener(self)
# #         directoryPanel.add(addButton)

# #         removeButton = JButton("Remove")
# #         removeButton.addActionListener(self)
# #         directoryPanel.add(removeButton)

# #         # Panel to hold the list and buttons
# #         directoryListPanel = JPanel(BorderLayout())
# #         directoryListPanel.add(scrollPane, BorderLayout.CENTER)
# #         directoryListPanel.add(directoryPanel, BorderLayout.SOUTH)

# #         # Panel to hold the directory list and other settings
# #         combinedNorthPanel = JPanel()
# #         combinedNorthPanel.setLayout(BoxLayout(combinedNorthPanel, BoxLayout.Y_AXIS))
# #         combinedNorthPanel.add(directoryListPanel)

# #         self.data = {
# #             "Compounds": ["Compound 1", "Compound 2", "Compound 3", "Compound 4", "All compounds"],
# #             "Concentrations": ["20uM", "6.33uM", "2.01uM", "0.634uM", "0.201uM", "0.0635uM", "0.0201uM", "0.0064uM", "0.002uM", "0.0006uM"]
# #         }
        
# #         # Sort by options
# #         sortPanel = JPanel(FlowLayout(FlowLayout.LEFT))
# #         self.compoundsCheckBox = JCheckBox("Compounds")
# #         self.concentrationsCheckBox = JCheckBox("Concentrations")
# #         self.checkBoxGroup = ButtonGroup()
# #         self.checkBoxGroup.add(self.compoundsCheckBox)
# #         self.checkBoxGroup.add(self.concentrationsCheckBox)
# #         self.compoundsCheckBox.addActionListener(self.updateDropdown)
# #         self.concentrationsCheckBox.addActionListener(self.updateDropdown)
# #         sortLabel = JLabel("Sort by: ")
# #         sortPanel.add(sortLabel)
# #         sortPanel.add(self.compoundsCheckBox)
# #         sortPanel.add(self.concentrationsCheckBox)
# #         combinedNorthPanel.add(sortPanel)

# #         # Dynamic Combo Panel
# #         dynamicComboPanel = JPanel(FlowLayout(FlowLayout.LEFT))
# #         dynamicComboLabel = JLabel("Select group to montage: ")
# #         self.dynamicCombo = JComboBox([])
# #         self.dynamicCombo.setEnabled(False)
# #         dynamicComboPanel.add(dynamicComboLabel)
# #         dynamicComboPanel.add(self.dynamicCombo)
# #         combinedNorthPanel.add(dynamicComboPanel)

# #         # PolyGR Combo Panel
# #         polyGRComboPanel = JPanel(FlowLayout(FlowLayout.LEFT))
# #         polyGRComboLabel = JLabel("Include/Exclude PolyGR: ")
# #         self.polyGRCombo = JComboBox(Vector(["Include", "Exclude"]))
# #         polyGRComboPanel.add(polyGRComboLabel)
# #         polyGRComboPanel.add(self.polyGRCombo)
# #         combinedNorthPanel.add(polyGRComboPanel)

# #         # Quadrants Combo Panel
# #         quadrantsComboPanel = JPanel(FlowLayout(FlowLayout.LEFT))
# #         quadrantsComboLabel = JLabel("Quadrants: ")
# #         self.quadrantsCombo = JComboBox(Vector(["Top left", "Top Right", "Bottom Left", "Bottom Right", "Random Quadrant", "All Quadrants"]))
# #         quadrantsComboPanel.add(quadrantsComboLabel)
# #         quadrantsComboPanel.add(self.quadrantsCombo)
# #         combinedNorthPanel.add(quadrantsComboPanel)

# #         # Scale Panel
# #         scalePanel = JPanel(FlowLayout(FlowLayout.LEFT))
# #         scaleLabel = JLabel("Scale: ")
# #         self.scaleField = JTextField("1.0", 10)
# #         scalePanel.add(scaleLabel)
# #         scalePanel.add(self.scaleField)
# #         combinedNorthPanel.add(scalePanel)

# #         # Label Font Size Panel
# #         labelFontSizePanel = JPanel(FlowLayout(FlowLayout.LEFT))
# #         labelFontSizeLabel = JLabel("Label font size: ")
# #         self.labelFontSizeField = JTextField("12", 10)
# #         labelFontSizePanel.add(labelFontSizeLabel)
# #         labelFontSizePanel.add(self.labelFontSizeField)
# #         combinedNorthPanel.add(labelFontSizePanel)

# #         # Border Size Panel
# #         borderSizePanel = JPanel(FlowLayout(FlowLayout.LEFT))
# #         borderSizeLabel = JLabel("Border size (pixels): ")
# #         self.borderSizeField = JTextField("10", 10)
# #         borderSizePanel.add(borderSizeLabel)
# #         borderSizePanel.add(self.borderSizeField)
# #         combinedNorthPanel.add(borderSizePanel)

# #         # Function call to get current date-time string
# #         datetimestr = self.getDateTimeStr()

# #         # Output Directory Panel
# #         outputDirectoryPanel = JPanel(FlowLayout(FlowLayout.LEFT))
# #         outputDirectoryLabel = JLabel("Output directory: ")
# #         self.outputDirectoryField = JTextField(20)
# #         outputDirectoryButton = JButton("Browse")
# #         outputDirectoryButton.addActionListener(self.selectOutputDirectory)
# #         outputDirectoryPanel.add(outputDirectoryLabel)
# #         outputDirectoryPanel.add(self.outputDirectoryField)
# #         outputDirectoryPanel.add(outputDirectoryButton)
# #         combinedNorthPanel.add(outputDirectoryPanel)

# #         # Output Suffix Panel
# #         outputSuffixPanel = JPanel(FlowLayout(FlowLayout.LEFT))
# #         outputSuffixLabel = JLabel("Output suffix: ")
# #         self.outputSuffixField = JTextField("_Montaged_{}".format(datetimestr), 20)
# #         outputSuffixPanel.add(outputSuffixLabel)
# #         outputSuffixPanel.add(self.outputSuffixField)
# #         combinedNorthPanel.add(outputSuffixPanel)

# #         self.frame.add(combinedNorthPanel, BorderLayout.NORTH)

# #         # Create Montage button
# #         montageButtonPanel = JPanel(FlowLayout())
# #         self.montageButton = JButton("Create Montage")
# #         self.montageButton.addActionListener(self)
# #         montageButtonPanel.add(self.montageButton)

# #         self.frame.add(montageButtonPanel, BorderLayout.SOUTH)

# #         # Display the frame
# #         self.frame.setVisible(True)

# #         # Default to negative
# #         self.createMontageClicked = False

# #         self.windowClosed = False
# #         self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
# #         self.frame.addWindowListener(WindowCloseListener(self))

# #     def actionPerformed(self, event):
# #         command = event.getActionCommand()
# #         if command == "Create Montage":
# #             if self.validateSettings():
# #                 self.showConfirmationDialog()
# #             return
# #         elif command == "Add":
# #             self.addDirectory()
# #         elif command == "Remove":
# #             self.removeDirectory()


# #     def validateSettings(self):
# #         try:
# #             # Validate Input Directories
# #             if self.listModel.getSize() == 0:
# #                 JOptionPane.showMessageDialog(self.frame, "No input directories have been added.", "Settings Error", JOptionPane.ERROR_MESSAGE)
# #                 return False

# #             for i in range(self.listModel.getSize()):
# #                 directory = self.listModel.getElementAt(i)
# #                 fileObj = File(directory)
# #                 if not fileObj.isDirectory():
# #                     JOptionPane.showMessageDialog(self.frame, "The directory '{}' is not valid.".format(directory), "Settings Error", JOptionPane.ERROR_MESSAGE)
# #                     return False

# #             # Validate Output Suffix
# #             output_suffix = self.outputSuffixField.getText()
# #             if not output_suffix:
# #                 JOptionPane.showMessageDialog(self.frame, "Output suffix cannot be empty.", "Settings Error", JOptionPane.ERROR_MESSAGE)
# #                 return False

# #             # Validate Output Directory
# #             output_directory = self.outputDirectoryField.getText()
# #             if not output_directory:
# #                 JOptionPane.showMessageDialog(self.frame, "Output directory cannot  be empty.", "Settings Error", JOptionPane.ERROR_MESSAGE)
# #                 return False
# #             elif not os.path.isdir(output_directory):
# #                 JOptionPane.showMessageDialog(self.frame, "Output directory is not a valid directory.", "Settings Error", JOptionPane.ERROR_MESSAGE)
# #                 return False
        
# #             # Validate Sortby Selection
# #             if not self.compoundsCheckBox.isSelected() and not self.concentrationsCheckBox.isSelected():
# #                 JOptionPane.showMessageDialog(self.frame, "Please select a 'Sort by:' option (Compounds or Concentrations).", "Settings Error", JOptionPane.ERROR_MESSAGE)
# #                 return False

# #             # Validate Scale
# #             scale = float(self.scaleField.getText())
# #             if scale < 0.1 or scale > 1.0:
# #                 JOptionPane.showMessageDialog(self.frame, "Scale value must contain a value between 0.1 and 1.0", "Settings Error", JOptionPane.ERROR_MESSAGE)
# #                 return False

# #             # Validate Label Font Size
# #             label_font_size = int(self.labelFontSizeField.getText())
# #             if label_font_size < 0 or label_font_size > 200 or label_font_size is None or label_font_size == "":
# #                 JOptionPane.showMessageDialog(self.frame, "Label font value must contain a value between 0 and 200", "Settings Error", JOptionPane.ERROR_MESSAGE)
# #                 return False

# #             # Validate Border Size
# #             border_size = int(self.borderSizeField.getText())
# #             if border_size < 0 or border_size > 200:
# #                 JOptionPane.showMessageDialog(self.frame, "Border size value must contain a value between 0 and 200", "Settings Error", JOptionPane.ERROR_MESSAGE)
# #                 return False

# #         except ValueError as e:
# #             JOptionPane.showMessageDialog(self.frame, str(e))
# #             return False

# #         return True

# #     def updateDropdown(self, event):
# #         if self.compoundsCheckBox.isSelected():
# #             self.dynamicCombo.setModel(DefaultComboBoxModel(Vector(self.data["Compounds"])))
# #             self.dynamicCombo.setEnabled(True)
# #         elif self.concentrationsCheckBox.isSelected():
# #             self.dynamicCombo.setModel(DefaultComboBoxModel(Vector(self.data["Concentrations"])))
# #             self.dynamicCombo.setEnabled(True)
# #         else:
# #             self.dynamicCombo.setModel(DefaultComboBoxModel([]))
# #             self.dynamicCombo.setEnabled(False)

# #     def addDirectory(self):
# #         chooser = JFileChooser()
# #         chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
# #         if hasattr(self, 'lastSelectedDirectory') and self.lastSelectedDirectory is not None:
# #             chooser.setCurrentDirectory(File(self.lastSelectedDirectory).getParentFile())
# #         returnValue = chooser.showOpenDialog(self.frame)
# #         if returnValue == JFileChooser.APPROVE_OPTION:
# #             directory = chooser.getSelectedFile()
# #             self.listModel.addElement(directory.getAbsolutePath())
# #             self.lastSelectedDirectory = directory.getAbsolutePath()

# #     def removeDirectory(self):
# #         index = self.list.getSelectedIndex()  # Corrected method name here
# #         if index >= 0:
# #             self.listModel.remove(index)

# #     def getDirectoryList(self):
# #         return [self.listModel.getElementAt(i) for i in range(self.listModel.size())]

# #     def processDirectories(self):
# #         directory_list = self.getDirectoryList()
# #         print("Selected directories:", directory_list)
# #         if len(directory_list) < 1:
# #             print("User has not selected any directories, exiting script...")
# #         self.closeWindow()
            
# #     def getDateTimeStr(self):
# #         dateFormat = SimpleDateFormat("ddMMMyyyy-HHmm")
# #         return dateFormat.format(Date())

# #     def selectOutputDirectory(self, event):
# #         chooser = JFileChooser()
# #         chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
# #         returnValue = chooser.showOpenDialog(self.frame)
# #         if returnValue == JFileChooser.APPROVE_OPTION:
# #             directory = chooser.getSelectedFile()
# #             self.outputDirectoryField.setText(directory.getAbsolutePath())
        
# #     def showConfirmationDialog(self):
# #         settingsPanel = JPanel()
# #         settingsPanel.setLayout(BoxLayout(settingsPanel, BoxLayout.Y_AXIS))

# #         # Add components to settingsPanel for each setting
# #         # Input Directories
# #         if self.listModel.getSize() > 0:
# #             inputDirs = "<html><b>Input Plate Directories:</b><br>" + "<br>".join([self.listModel.getElementAt(i) for i in range(self.listModel.getSize())]) + "</html>"
# #             settingsPanel.add(JLabel(inputDirs))

# #         # Output Directory
# #         settingsPanel.add(JLabel("<html><b>Output directory:</b> " + self.getOutputDirectory() + "</html>"))

# #         # Output Suffix
# #         settingsPanel.add(JLabel("<html><b>Output suffix:</b> " + self.getOutputSuffix() + "</html>"))

# #         # Sort By
# #         sortBy = "Compounds" if self.getSelectedCompounds() else "Concentrations"
# #         settingsPanel.add(JLabel("<html><b>Sort by:</b> " + sortBy + "</html>"))

# #         # Dynamic Combo
# #         if self.getSelectedCompounds():
# #             settingsPanel.add(JLabel("<html><b>Compound selected:</b> " + self.getDynamicComboValue() + "</html>"))
# #         elif self.getSelectedConcentrations():
# #             settingsPanel.add(JLabel("<html><b>Concentration selected:</b> " + self.getDynamicComboValue() + "</html>"))

# #         # Other Settings
# #         settingsPanel.add(JLabel("<html><b>PolyGR:</b> " + self.getPolyGRComboValue() + "</html>"))
# #         settingsPanel.add(JLabel("<html><b>Quadrant:</b> " + self.getQuadrantsComboValue() + "</html>"))
# #         settingsPanel.add(JLabel("<html><b>Scale:</b> " + self.getScaleValue() + "</html>"))
# #         settingsPanel.add(JLabel("<html><b>Label font size:</b> " + self.getLabelFontSize() + "</html>"))
# #         settingsPanel.add(JLabel("<html><b>Border pixel size:</b> " + self.getBorderSize() + "</html>"))

# #         # Show dialog
# #         option = JOptionPane.showConfirmDialog(self.frame, settingsPanel, "Confirm Settings", JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE)

# #         # OK button pressed
# #         if option == JOptionPane.OK_OPTION:
# #             self.createMontageClicked = True
# #             self.frame.dispose()
# #         # Cancel button pressed - keep the application window open for modifications

# #     def getScaleValue(self):
# #         return self.scaleField.getText()

# #     def getLabelFontSize(self):
# #         return self.labelFontSizeField.getText()

# #     def getBorderSize(self):
# #         return self.borderSizeField.getText()

# #     def getOutputDirectory(self):
# #         return self.outputDirectoryField.getText()

# #     def getOutputSuffix(self):
# #         return self.outputSuffixField.getText()

# #     def getSelectedCompounds(self):
# #         return self.compoundsCheckBox.isSelected()

# #     def getSelectedConcentrations(self):
# #         return self.concentrationsCheckBox.isSelected()

# #     def getDynamicComboValue(self):
# #         return self.dynamicCombo.getSelectedItem()

# #     def getPolyGRComboValue(self):
# #         return self.polyGRCombo.getSelectedItem()

# #     def getQuadrantsComboValue(self):
# #         return self.quadrantsCombo.getSelectedItem()
    
# #     def getAllSettings(self):
# #             # Retrieve all settings and return them
# #             return {
# #                 "input_directory_list": self.getDirectoryList(),
# #                 "output_directory": self.getOutputDirectory(),
# #                 "output_suffix": self.getOutputSuffix(),
# #                 "sortby_value": self.getDynamicComboValue(),
# #                 "compounds_selected": self.getSelectedCompounds(),
# #                 "concentration_selection": self.getSelectedConcentrations(),
# #                 "polygr_selection": self.getPolyGRComboValue(),
# #                 "quadrant_selection": self.getQuadrantsComboValue(),
# #                 "scale": self.getScaleValue(),
# #                 "label_font_size": self.getLabelFontSize(),
# #                 "border_size": self.getBorderSize()
# #             }

# # def get_montage_settings(printout=False):
# #     gui = Application()
# #     gui.frame.setVisible(True)

# #     # Wait for the user to click Create Montage or close the window
# #     while not gui.createMontageClicked and not gui.windowClosed:
# #         try:
# #             Thread.sleep(100)
# #         except InterruptedException:
# #             break

# #     if gui.createMontageClicked:
# #         settings = gui.getAllSettings()
# #         if printout:
# #             print("""Montage Settings:
# #                   Input Plate Directories:

# #                   """)
# #             return settings
# #     elif gui.windowClosed:
# #         print("Window closed by the user.")
# #         return None  # or exit the script as needed


# # get_montage_settings()
# # # def get_associated_quadrant_wellIDs(well_id):
# # #     rows = "ABCDEFGHIJKLMNOP"
# # #     row = well_id[0].upper()
# # #     col = int(well_id[1:])

# # #     # Adjust row and column to top-left of the quadrant
# # #     row_index = rows.index(row)
# # #     if row_index % 2 != 0:
# # #         top_row = rows[row_index - 1]
# # #         bottom_row = row
# # #     else:
# # #         top_row = row
# # #         bottom_row = rows[row_index + 1]

# # #     left_col = col - 1 if col % 2 == 0 else col

# # #     # Generate the well IDs of the quadrant
# # #     quadrant_wells = [
# # #         f"{top_row}{left_col}",
# # #         f"{top_row}{left_col + 1}",
# # #         f"{bottom_row}{left_col}",
# # #         f"{bottom_row}{left_col + 1}"
# # #     ]

# # #     return quadrant_wells

# # # def get_384_quadrants(quadrant):
# # #     """
# # #     Returns a list of 384w wellIDs (one from each quadrant) as specified
# # #     """
# # #     # Dictionary 
# # #     quadrant_transform = {
# # #         "Top Left": (0, 0),
# # #         "Top Right": (0, 1),
# # #         "Bottom Left": (1, 0),
# # #         "Bottom Right": (1, 1)
# # #     }

# # #     well_ids = []
# # #     for row in range(1, 17, 2):  # Skip every other row to match the 96-well layout
# # #         for col in range(1, 25, 2):  # Skip every other column
# # #             if quadrant != "Random":
# # #                 # Calculate row and column for the specific quadrant
# # #                 delta_row, delta_col = quadrant_transform[quadrant]
# # #                 well_id = "{}{}".format(chr(64 + row + delta_row), col + delta_col)
# # #                 well_ids.append(well_id)
# # #             else:
# # #                 # Select a random well from the 2x2 block
# # #                 delta_row, delta_col = random.choice(list(quadrant_transform.values()))
# # #                 well_id = "{}{}".format(chr(64 + row + delta_row), col + delta_col)
# # #                 well_ids.append(well_id)

# # #     return well_ids

# # # # Usage example
# # # settings = get_montage_settings(True)
# # # if settings is None:
# # #     exit()

# # # print(get_384_quadrants("Top Left"))


# from javax.swing import JFrame, JPanel, JLabel, JButton, JList, JScrollPane, JFileChooser, JComboBox, JCheckBox, ButtonGroup, DefaultComboBoxModel, JTextField, JOptionPane, BoxLayout, JTable, AbstractCellEditor, DefaultListModel
# from javax.swing.table import TableCellRenderer, TableCellEditor, DefaultTableModel
# from java.awt import BorderLayout, FlowLayout, Component
# from java.lang import Thread, InterruptedException, Object
# from java.awt.event import ActionListener, WindowAdapter, WindowEvent
# from java.io import File
# from java.util import Vector, Date
# from java.text import SimpleDateFormat

# import os
# import json
# import random


# class ComboBoxCellEditor(AbstractCellEditor, TableCellEditor):
#     def __init__(self, items):
#         self.comboBox = JComboBox(items)

#     def getCellEditorValue(self):
#         return self.comboBox.getSelectedItem()

#     def getTableCellEditorComponent(self, table, value, isSelected, row, column):
#         self.comboBox.setSelectedItem(value)
#         return self.comboBox

# class WindowCloseListener(WindowAdapter):
#     def __init__(self, app):
#         self.app = app

#     def windowClosed(self, windowEvent):
#         self.app.windowClosed = True

# class Application(ActionListener):

#     def __init__(self):
#         self.frame = JFrame("Montage Settings")
#         self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
#         self.frame.setSize(500, 600)
#         self.frame.setLayout(BorderLayout())

#         # Directory Manager components
#         self.tableModel = DefaultTableModel()
#         self.tableModel.addColumn("Directory")
#         self.tableModel.addColumn("Option")
#         self.table = JTable(self.tableModel)
#         comboBoxEditor = ComboBoxCellEditor(["Option1", "Option2"])
#         self.table.getColumnModel().getColumn(1).setCellEditor(comboBoxEditor)

#         scrollPane = JScrollPane(self.table)

#         # Buttons for Directory Manager
#         directoryPanel = JPanel(FlowLayout(FlowLayout.LEFT))
#         addButton = JButton("Add")
#         addButton.addActionListener(self)
#         directoryPanel.add(addButton)

#         removeButton = JButton("Remove")
#         removeButton.addActionListener(self)
#         directoryPanel.add(removeButton)

#         # Panel to hold the list and buttons
#         directoryListPanel = JPanel(BorderLayout())
#         directoryListPanel.add(scrollPane, BorderLayout.CENTER)
#         directoryListPanel.add(directoryPanel, BorderLayout.SOUTH)

#         # Panel to hold the directory list and other settings
#         combinedNorthPanel = JPanel()
#         combinedNorthPanel.setLayout(BoxLayout(combinedNorthPanel, BoxLayout.Y_AXIS))
#         combinedNorthPanel.add(directoryListPanel)

#         self.data = {
#             "Compounds": ["Compound 1", "Compound 2", "Compound 3", "Compound 4", "All compounds"],
#             "Concentrations": ["20uM", "6.33uM", "2.01uM", "0.634uM", "0.201uM", "0.0635uM", "0.0201uM", "0.0064uM", "0.002uM", "0.0006uM"]
#         }
        
#         # Sort by options
#         sortPanel = JPanel(FlowLayout(FlowLayout.LEFT))
#         self.compoundsCheckBox = JCheckBox("Compounds")
#         self.concentrationsCheckBox = JCheckBox("Concentrations")
#         self.checkBoxGroup = ButtonGroup()
#         self.checkBoxGroup.add(self.compoundsCheckBox)
#         self.checkBoxGroup.add(self.concentrationsCheckBox)
#         self.compoundsCheckBox.addActionListener(self.updateDropdown)
#         self.concentrationsCheckBox.addActionListener(self.updateDropdown)
#         sortLabel = JLabel("Sort by: ")
#         sortPanel.add(sortLabel)
#         sortPanel.add(self.compoundsCheckBox)
#         sortPanel.add(self.concentrationsCheckBox)
#         combinedNorthPanel.add(sortPanel)

#         # Dynamic Combo Panel
#         dynamicComboPanel = JPanel(FlowLayout(FlowLayout.LEFT))
#         dynamicComboLabel = JLabel("Select group to montage: ")
#         self.dynamicCombo = JComboBox([])
#         self.dynamicCombo.setEnabled(False)
#         dynamicComboPanel.add(dynamicComboLabel)
#         dynamicComboPanel.add(self.dynamicCombo)
#         combinedNorthPanel.add(dynamicComboPanel)

#         # PolyGR Combo Panel
#         polyGRComboPanel = JPanel(FlowLayout(FlowLayout.LEFT))
#         polyGRComboLabel = JLabel("Include/Exclude PolyGR: ")
#         self.polyGRCombo = JComboBox(Vector(["Include", "Exclude"]))
#         polyGRComboPanel.add(polyGRComboLabel)
#         polyGRComboPanel.add(self.polyGRCombo)
#         combinedNorthPanel.add(polyGRComboPanel)

#         # Quadrants Combo Panel
#         quadrantsComboPanel = JPanel(FlowLayout(FlowLayout.LEFT))
#         quadrantsComboLabel = JLabel("Quadrants: ")
#         self.quadrantsCombo = JComboBox(Vector(["Top left", "Top Right", "Bottom Left", "Bottom Right", "Random Quadrant", "All Quadrants"]))
#         quadrantsComboPanel.add(quadrantsComboLabel)
#         quadrantsComboPanel.add(self.quadrantsCombo)
#         combinedNorthPanel.add(quadrantsComboPanel)

#         # Scale Panel
#         scalePanel = JPanel(FlowLayout(FlowLayout.LEFT))
#         scaleLabel = JLabel("Scale: ")
#         self.scaleField = JTextField("1.0", 10)
#         scalePanel.add(scaleLabel)
#         scalePanel.add(self.scaleField)
#         combinedNorthPanel.add(scalePanel)

#         # Label Font Size Panel
#         labelFontSizePanel = JPanel(FlowLayout(FlowLayout.LEFT))
#         labelFontSizeLabel = JLabel("Label font size: ")
#         self.labelFontSizeField = JTextField("12", 10)
#         labelFontSizePanel.add(labelFontSizeLabel)
#         labelFontSizePanel.add(self.labelFontSizeField)
#         combinedNorthPanel.add(labelFontSizePanel)

#         # Border Size Panel
#         borderSizePanel = JPanel(FlowLayout(FlowLayout.LEFT))
#         borderSizeLabel = JLabel("Border size (pixels): ")
#         self.borderSizeField = JTextField("10", 10)
#         borderSizePanel.add(borderSizeLabel)
#         borderSizePanel.add(self.borderSizeField)
#         combinedNorthPanel.add(borderSizePanel)

#         # Function call to get current date-time string
#         datetimestr = self.getDateTimeStr()

#         # Output Directory Panel
#         outputDirectoryPanel = JPanel(FlowLayout(FlowLayout.LEFT))
#         outputDirectoryLabel = JLabel("Output directory: ")
#         self.outputDirectoryField = JTextField(20)
#         outputDirectoryButton = JButton("Browse")
#         outputDirectoryButton.addActionListener(self.selectOutputDirectory)
#         outputDirectoryPanel.add(outputDirectoryLabel)
#         outputDirectoryPanel.add(self.outputDirectoryField)
#         outputDirectoryPanel.add(outputDirectoryButton)
#         combinedNorthPanel.add(outputDirectoryPanel)

#         # Output Suffix Panel
#         outputSuffixPanel = JPanel(FlowLayout(FlowLayout.LEFT))
#         outputSuffixLabel = JLabel("Output suffix: ")
#         self.outputSuffixField = JTextField("_Montaged_{}".format(datetimestr), 20)
#         outputSuffixPanel.add(outputSuffixLabel)
#         outputSuffixPanel.add(self.outputSuffixField)
#         combinedNorthPanel.add(outputSuffixPanel)

#         self.frame.add(combinedNorthPanel, BorderLayout.NORTH)

#         # Create Montage button
#         montageButtonPanel = JPanel(FlowLayout())
#         self.montageButton = JButton("Create Montage")
#         self.montageButton.addActionListener(self)
#         montageButtonPanel.add(self.montageButton)

#         self.frame.add(montageButtonPanel, BorderLayout.SOUTH)

#         # Display the frame
#         self.frame.setVisible(True)

#         # Default to negative
#         self.createMontageClicked = False

#         self.windowClosed = False
#         self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
#         self.frame.addWindowListener(WindowCloseListener(self))

#     def actionPerformed(self, event):
#         command = event.getActionCommand()
#         if command == "Create Montage":
#             if self.validateSettings():
#                 self.showConfirmationDialog()
#             return
#         elif command == "Add":
#             self.addDirectory()
#         elif command == "Remove":
#             self.removeDirectory()


#     def validateSettings(self):
#         try:
#             # Validate Input Directories
#             if self.tableModel.getRowCount() == 0:
#                 JOptionPane.showMessageDialog(self.frame, "No input directories have been added.", "Settings Error", JOptionPane.ERROR_MESSAGE)
#                 return False

#             for i in range(self.tableModel.getRowCount()):
#                 directory = self.tableModel.getValueAt(i, 0)  # Get directory from the first column
#                 fileObj = File(directory)
#                 if not fileObj.isDirectory():
#                     JOptionPane.showMessageDialog(self.frame, "The directory '{}' is not valid.".format(directory), "Settings Error", JOptionPane.ERROR_MESSAGE)
#                     return False
        
#             # Validate Output Suffix
#             output_suffix = self.outputSuffixField.getText()
#             if not output_suffix:
#                 JOptionPane.showMessageDialog(self.frame, "Output suffix cannot be empty.", "Settings Error", JOptionPane.ERROR_MESSAGE)
#                 return False

#             # Validate Output Directory
#             output_directory = self.outputDirectoryField.getText()
#             if not output_directory:
#                 JOptionPane.showMessageDialog(self.frame, "Output directory cannot  be empty.", "Settings Error", JOptionPane.ERROR_MESSAGE)
#                 return False
#             elif not os.path.isdir(output_directory):
#                 JOptionPane.showMessageDialog(self.frame, "Output directory is not a valid directory.", "Settings Error", JOptionPane.ERROR_MESSAGE)
#                 return False
        
#             # Validate Sortby Selection
#             if not self.compoundsCheckBox.isSelected() and not self.concentrationsCheckBox.isSelected():
#                 JOptionPane.showMessageDialog(self.frame, "Please select a 'Sort by:' option (Compounds or Concentrations).", "Settings Error", JOptionPane.ERROR_MESSAGE)
#                 return False

#             # Validate Scale
#             scale = float(self.scaleField.getText())
#             if scale < 0.1 or scale > 1.0:
#                 JOptionPane.showMessageDialog(self.frame, "Scale value must contain a value between 0.1 and 1.0", "Settings Error", JOptionPane.ERROR_MESSAGE)
#                 return False

#             # Validate Label Font Size
#             label_font_size = int(self.labelFontSizeField.getText())
#             if label_font_size < 0 or label_font_size > 200 or label_font_size is None or label_font_size == "":
#                 JOptionPane.showMessageDialog(self.frame, "Label font value must contain a value between 0 and 200", "Settings Error", JOptionPane.ERROR_MESSAGE)
#                 return False

#             # Validate Border Size
#             border_size = int(self.borderSizeField.getText())
#             if border_size < 0 or border_size > 200:
#                 JOptionPane.showMessageDialog(self.frame, "Border size value must contain a value between 0 and 200", "Settings Error", JOptionPane.ERROR_MESSAGE)
#                 return False

#         except ValueError as e:
#             JOptionPane.showMessageDialog(self.frame, str(e))
#             return False

#         return True

#     def updateDropdown(self, event):
#         if self.compoundsCheckBox.isSelected():
#             self.dynamicCombo.setModel(DefaultComboBoxModel(Vector(self.data["Compounds"])))
#             self.dynamicCombo.setEnabled(True)
#         elif self.concentrationsCheckBox.isSelected():
#             self.dynamicCombo.setModel(DefaultComboBoxModel(Vector(self.data["Concentrations"])))
#             self.dynamicCombo.setEnabled(True)
#         else:
#             self.dynamicCombo.setModel(DefaultComboBoxModel([]))
#             self.dynamicCombo.setEnabled(False)

#     def addDirectory(self):
#         chooser = JFileChooser()
#         chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
#         if hasattr(self, 'lastSelectedDirectory') and self.lastSelectedDirectory is not None:
#             chooser.setCurrentDirectory(File(self.lastSelectedDirectory).getParentFile())
#         returnValue = chooser.showOpenDialog(self.frame)
#         if returnValue == JFileChooser.APPROVE_OPTION:
#             directory = chooser.getSelectedFile()
#             self.tableModel.addRow([directory.getAbsolutePath(), "DefaultOption"])  # Add row to the table
#             self.lastSelectedDirectory = directory.getAbsolutePath()

#     def removeDirectory(self):
#         selectedRow = self.table.getSelectedRow()
#         if selectedRow >= 0:
#             self.tableModel.removeRow(selectedRow)

#     def getDirectoryList(self):
#         return [(self.tableModel.getValueAt(i, 0), self.tableModel.getValueAt(i, 1)) for i in range(self.tableModel.getRowCount())]

#     def processDirectories(self):
#         directory_list = self.getDirectoryList()
#         print("Selected directories:", directory_list)
#         if len(directory_list) < 1:
#             print("User has not selected any directories, exiting script...")
#         self.closeWindow()
            
#     def getDateTimeStr(self):
#         dateFormat = SimpleDateFormat("ddMMMyyyy-HHmm")
#         return dateFormat.format(Date())

#     def selectOutputDirectory(self, event):
#         chooser = JFileChooser()
#         chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
#         returnValue = chooser.showOpenDialog(self.frame)
#         if returnValue == JFileChooser.APPROVE_OPTION:
#             directory = chooser.getSelectedFile()
#             self.outputDirectoryField.setText(directory.getAbsolutePath())
        
#     def showConfirmationDialog(self):
#         settingsPanel = JPanel()
#         settingsPanel.setLayout(BoxLayout(settingsPanel, BoxLayout.Y_AXIS))

#         # Add components to settingsPanel for each setting
#         # Input Directories
#         if self.tableModel.getRowCount() > 0:
#             inputDirs = "<html><b>Input Plate Directories:</b><br>" + "<br>".join([self.tableModel.getValueAt(i, 0) for i in range(self.tableModel.getRowCount())]) + "</html>"
#             settingsPanel.add(JLabel(inputDirs))

#         # Output Directory
#         settingsPanel.add(JLabel("<html><b>Output directory:</b> " + self.getOutputDirectory() + "</html>"))

#         # Output Suffix
#         settingsPanel.add(JLabel("<html><b>Output suffix:</b> " + self.getOutputSuffix() + "</html>"))

#         # Sort By
#         sortBy = "Compounds" if self.getSelectedCompounds() else "Concentrations"
#         settingsPanel.add(JLabel("<html><b>Sort by:</b> " + sortBy + "</html>"))

#         # Dynamic Combo
#         if self.getSelectedCompounds():
#             settingsPanel.add(JLabel("<html><b>Compound selected:</b> " + self.getDynamicComboValue() + "</html>"))
#         elif self.getSelectedConcentrations():
#             settingsPanel.add(JLabel("<html><b>Concentration selected:</b> " + self.getDynamicComboValue() + "</html>"))

#         # Other Settings
#         settingsPanel.add(JLabel("<html><b>PolyGR:</b> " + self.getPolyGRComboValue() + "</html>"))
#         settingsPanel.add(JLabel("<html><b>Quadrant:</b> " + self.getQuadrantsComboValue() + "</html>"))
#         settingsPanel.add(JLabel("<html><b>Scale:</b> " + self.getScaleValue() + "</html>"))
#         settingsPanel.add(JLabel("<html><b>Label font size:</b> " + self.getLabelFontSize() + "</html>"))
#         settingsPanel.add(JLabel("<html><b>Border pixel size:</b> " + self.getBorderSize() + "</html>"))

#         # Show dialog
#         option = JOptionPane.showConfirmDialog(self.frame, settingsPanel, "Confirm Settings", JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE)

#         # OK button pressed
#         if option == JOptionPane.OK_OPTION:
#             self.createMontageClicked = True
#             self.frame.dispose()
#         # Cancel button pressed - keep the application window open for modifications

#     def getScaleValue(self):
#         return self.scaleField.getText()

#     def getLabelFontSize(self):
#         return self.labelFontSizeField.getText()

#     def getBorderSize(self):
#         return self.borderSizeField.getText()

#     def getOutputDirectory(self):
#         return self.outputDirectoryField.getText()

#     def getOutputSuffix(self):
#         return self.outputSuffixField.getText()

#     def getSelectedCompounds(self):
#         return self.compoundsCheckBox.isSelected()

#     def getSelectedConcentrations(self):
#         return self.concentrationsCheckBox.isSelected()

#     def getDynamicComboValue(self):
#         return self.dynamicCombo.getSelectedItem()

#     def getPolyGRComboValue(self):
#         return self.polyGRCombo.getSelectedItem()

#     def getQuadrantsComboValue(self):
#         return self.quadrantsCombo.getSelectedItem()
    
#     def getAllSettings(self):
#             # Retrieve all settings and return them
#             return {
#                 "input_directory_list": self.getDirectoryList(), # Returns a list of tuples.
#                 "output_directory": self.getOutputDirectory(),
#                 "output_suffix": self.getOutputSuffix(),
#                 "sortby_value": self.getDynamicComboValue(),
#                 "compounds_selected": self.getSelectedCompounds(),
#                 "concentration_selection": self.getSelectedConcentrations(),
#                 "polygr_selection": self.getPolyGRComboValue(),
#                 "quadrant_selection": self.getQuadrantsComboValue(),
#                 "scale": self.getScaleValue(),
#                 "label_font_size": self.getLabelFontSize(),
#                 "border_size": self.getBorderSize()
#             }

# def get_montage_settings(printout=False):
#     gui = Application()
#     gui.frame.setVisible(True)

#     # Wait for the user to click Create Montage or close the window
#     while not gui.createMontageClicked and not gui.windowClosed:
#         try:
#             Thread.sleep(100)
#         except InterruptedException:
#             break

#     if gui.createMontageClicked:
#         settings = gui.getAllSettings()
#         return settings
#     elif gui.windowClosed:
#         print("Window closed by the user.")
#         return None  # or exit the script as needed


# settings = get_montage_settings()
# print("Captured Montage Settings")
# if settings is None:
#     print("Captured no settings")
# settings_dump_fp = r"C:\Users\akmishra\Desktop\Example_settings.json"
# with open(settings_dump_fp, "w") as writefile:
#     print("Writing shit to file")
#     json.dump(settings, writefile, indent=4)

# print("Done")


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


# class ComboBoxCellEditor(AbstractCellEditor, TableCellEditor):
#     def __init__(self, items):
#         self.comboBox = JComboBox(items)

#     def getCellEditorValue(self):
#         return self.comboBox.getSelectedItem()

#     def getTableCellEditorComponent(self, table, value, isSelected, row, column):
#         self.comboBox.setSelectedItem(value)
#         return self.comboBox

class ComboBoxCellEditor(AbstractCellEditor, TableCellEditor):
    def __init__(self, items):
        self.comboBox = JComboBox(items)

    def getCellEditorValue(self):
        return self.comboBox.getSelectedItem()

    def getTableCellEditorComponent(self, table, value, isSelected, row, column):
        self.comboBox.setSelectedItem(value)
        return self.comboBox

class WindowCloseListener(WindowAdapter):
    def __init__(self, app):
        self.app = app

    def windowClosed(self, windowEvent):
        self.app.windowClosed = True

class Application(ActionListener):

    def __init__(self):
        self.frame = JFrame("Montage Settings")
        self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.frame.setSize(600, 820)
        self.frame.setLayout(BorderLayout())

        # Directory Manager components
        self.tableModel = DefaultTableModel()
        self.tableModel.addColumn("Directory")
        self.tableModel.addColumn("Read Step")
        self.table = JTable(self.tableModel)
        comboBoxEditor = ComboBoxCellEditor(["Option1", "Option2"])
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
        comboBoxEditor = ComboBoxCellEditor(options)
        self.table.getColumnModel().getColumn(1).setCellEditor(comboBoxEditor)


    def addDirectory(self):
        chooser = JFileChooser()
        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
        if hasattr(self, 'lastSelectedDirectory') and self.lastSelectedDirectory is not None:
            chooser.setCurrentDirectory(File(self.lastSelectedDirectory).getParentFile())
        returnValue = chooser.showOpenDialog(self.frame)

        if returnValue == JFileChooser.APPROVE_OPTION:
                directory = chooser.getSelectedFile().getAbsolutePath()
                read_steps = get_kinetic_read_list(directory)
                read_steps_str = [str(step) for step in read_steps]  # Convert to string if needed

                # Add the directory to the table with a default option
                self.tableModel.addRow([directory, read_steps_str[0] if read_steps_str else "No steps found"])

                # Update the dropdown for the new row
                rowIndex = self.tableModel.getRowCount() - 1  # Index of the new row
                self.updateDropdownForRow(rowIndex, read_steps_str)

                self.lastSelectedDirectory = directory


        # if returnValue == JFileChooser.APPROVE_OPTION:
        #     directory = chooser.getSelectedFile()
        #     self.tableModel.addRow([directory.getAbsolutePath(), "DefaultOption"])  # Add row to the table
        #     self.lastSelectedDirectory = directory.getAbsolutePath()

    def removeDirectory(self):
        selectedRow = self.table.getSelectedRow()
        if selectedRow >= 0:
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
        settingsPanel.add(JLabel("<html><b>Scale:</b> " + self.getScaleValue() + "</html>"))
        settingsPanel.add(JLabel("<html><b>Label font size:</b> " + self.getLabelFontSize() + "</html>"))
        settingsPanel.add(JLabel("<html><b>Border pixel size:</b> " + self.getBorderSize() + "</html>"))

        # Show dialog
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
                "scale": self.getScaleValue(),
                "label_font_size": self.getLabelFontSize(),
                "border_size": self.getBorderSize()
            }

def get_montage_settings(printout=False):
    gui = Application()
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

settings = get_montage_settings()
print("Captured Montage Settings")
if settings is None:
    print("Captured no settings")
print(settings)