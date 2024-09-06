// Get the input file
#@ File (label="Select a file") myFile

// Get the output Directory
outputDir = getDirectory("Select output directory");

// Open the file to begin processing
open(myFile);

// Get the name of the file so we can modify it for the output filepath
originalName = File.getNameWithoutExtension(myFile);

// Get the number of underscores in the name
underscoreIndex = indexOf(originalName, "_"); 
// If the number of underscores is more than 0
if (underscoreIndex != -1) { 
	// Get the string that's between the beginning of the filename and before the occurance of the first underscore
	wellID = substring(originalName, 0, underscoreIndex); //extracts the substring with the defined star and end indices
} else {
	// If the number of underscores is 0, we'll use the whole filename
    wellID = originalName;
}

// Add "MAX_" as the prefix to the wellID for the new filename with the .tif extension
newName = "MAX_" + wellID + ".tif";
// Add the new filename to the output directory we chose before
outputPath = outputDir + newName;

// Run the Z projection on the opened image
run("Z Project...", "projection=[Max Intensity]");

// Save the image to the output path
saveAs("Tiff", outputPath);

// Close the originally opened image and the Z projected image.
close();
close();



