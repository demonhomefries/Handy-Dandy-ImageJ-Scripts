import os
import pip
import argparse

try:
    import pandas as pd
except ImportError:
    pip.main(["install", "pandas"])
    import pandas as pd

class tc:
    def black(text):
        return f'\033[30m{text}\033[0m'
    def red(text):
        return f'\033[31m{text}\033[0m'
    def green(text):
        return f'\033[32m{text}\033[0m'
    def yellow(text):
        return f'\033[33m{text}\033[0m'
    def blue(text):
        return f'\033[34m{text}\033[0m'
    def magenta(text):
        return f'\033[35m{text}\033[0m'
    def cyan(text):
        return f'\033[36m{text}\033[0m'
    def white(text):
        return f'\033[37m{text}\033[0m'

def get_csv_fps(input_folder):
    csv_filepaths = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.csv'):
                csv_filepaths.append(os.path.join(root, file))
    return csv_filepaths

def sort_filepaths(filepaths):
    # Create a dictionary to store file paths based on common parts of filenames
    files_dict = {}

    # Iterate through the list of file paths
    for filepath in filepaths:
        # Get the filename without the directory path
        filename = os.path.basename(filepath)
        # Determine if it's a "spots" or "tracks" file
        if "spots" in filename:
            # Remove "spots" from filename to get the common part
            common_part = filename.replace("spots", "")
            if common_part not in files_dict:
                files_dict[common_part] = [None, None, None]
            files_dict[common_part][0] = filepath
        elif "tracks" in filename:
            # Remove "tracks" from filename to get the common part
            common_part = filename.replace("tracks", "")
            if common_part not in files_dict:
                files_dict[common_part] = [None, None, None]
            files_dict[common_part][1] = filepath

    # Create a list of tuples from the dictionary
    sorted_filepaths = []
    for common_part, paths in files_dict.items():
        spots_path, tracks_path, _ = paths
        if spots_path:
            # Generate the output filepath
            output_filename = os.path.basename(spots_path).replace("spots", "merged")
            output_filepath = os.path.join(os.path.dirname(spots_path), output_filename)
            sorted_filepaths.append((spots_path, tracks_path, output_filepath))

    return sorted_filepaths

def create_merged_df (spots_fp, tracks_fp):
    # Load and process spots
    spots_df = pd.read_csv(spots_fp, low_memory=False)
    spots_df = spots_df.drop([0, 1, 2]) # Remove the first three rows after the column headers as they are just secondary headers, not useful values
    # Convert all the columns into numbers as datatypes
    for column in spots_df.columns:
        if column != 'LABEL':
            spots_df[column] = pd.to_numeric(spots_df[column])

    # Load and process tracks
    tracks_df = pd.read_csv(tracks_fp, low_memory=False)
    tracks_df = tracks_df.drop([0, 1, 2]) # Remove the first three rows after the column headers as they are just secondary headers, not useful values
    # Convert all the columns into numbers as datatypes
    for column in tracks_df.columns:
        if column != 'LABEL':
            tracks_df[column] = pd.to_numeric(tracks_df[column])


    # Group by TRACK_ID and calculate the average AREA for each group
    spots_areaAvg = spots_df.groupby('TRACK_ID')['AREA'].mean().reset_index()

    merged_df = pd.merge(tracks_df, spots_areaAvg, on='TRACK_ID', how='right')

    # Rename the column
    merged_df = merged_df.rename(columns={'AREA': 'AREA_AVERAGED'})

    #print(merged_df)
    # Export the data into a CSV
    #merged_df.to_csv(output_fp, index=False)
    return merged_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that merges spots table into tracks table (one per operation)."
    )
    parser.add_argument('--csvlist', required=True, type=str, help="[spot table fp, tracks csv fp]")
    args = parser.parse_args()

# print(tc.cyan("\n\nEnter your folder containing spots + tracks files.\nEach file should be named [cell line number]_XXXX_[\"tracks\" or \"spots\"][integer].csv"))
# while True:
#     csv_folder = input(tc.yellow("\nInput folder: "))
#     if os.path.isdir(csv_folder):
#         break
#     else:
#         print(tc.red(f"ERROR {csv_folder} was not recognized as a folder"))

# csv_fps = get_csv_fps(csv_folder)

# Sort and display input CSVs 
# print(tc.cyan("\nFilepaths to merge:"))
# sorted_fps = sort_filepaths(csv_fps)
# for index, filepaths in enumerate(sorted_fps):
#     spots_fp, tracks_fp, output_fp = filepaths
#     spotname = os.path.basename(spots_fp)
#     trackname = os.path.basename(tracks_fp)
#     outputname = os.path.basename(output_fp)
    #print(f"{index + 1}. {spotname} + {trackname} --> {outputname}")

# Confirm CSV inputs
# confirmation = input(tc.yellow("Press Y to confirm, or any other key to exit: "))
# if confirmation.lower() != "y":
#     print(tc.red("User exit the script.\n"))

# Run merge and generate output CSVs
# for number, set in enumerate(sorted_fps):
    # spots_fp, tracks_fp, output_fp = set
    # merged_df = create_merged_df(spots_fp, tracks_fp)
    # merged_df.to_csv(output_fp, index=False)
    # print(tc.cyan(f"{number + 1}. Completed merge: {os.path.basename(output_fp)}"))


# Grab the CSV list string and replace the quotation marks
csv_file_string = args.csvlist
csv_file_string.replace("\"", "")
spots_fp, tracks_fp = csv_file_string.split(",")
output_path = spots_fp.replace("_spottable_auto", "_merged_auto")

if not os.path.isfile(spots_fp):
    print(f"ERROR Track-Spot_Merger_Auto.py not a valid filepath: {spots_fp}")
    exit(1)
if not os.path.isfile(tracks_fp):
    print(f"ERROR Track-Spot_Merger_Auto.py not a valid filepath: {tracks_fp}")
    exit(1)

merged_df = create_merged_df(spots_fp, tracks_fp)
merged_df.to_csv(output_path, index=False)

if not os.path.isfile(output_path):
    print(f"ERROR Track-Spot_Merger_Auto.py not a valid filepath: {output_path}")
    exit(1)
print(f"\tTrack-Spot_Merger_Auto.py Completed merge: {output_path}")
exit(0)

