import os
import shutil
from datetime import datetime

def organize_photos(source_folder, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate over files in the source folder
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            try:
                # Get the creation date of the file
                creation_time = os.path.getctime(file_path)
                date_time = datetime.utcfromtimestamp(creation_time)

                # Create destination folder based on year and month
                year_folder = os.path.join(destination_folder, str(date_time.year))
                month_folder = os.path.join(year_folder, str(date_time.month))

                # Create year and month folders if they don't exist
                if not os.path.exists(year_folder):
                    os.makedirs(year_folder)
                if not os.path.exists(month_folder):
                    os.makedirs(month_folder)

                # Move the file to the destination folder
                shutil.move(file_path, os.path.join(month_folder, filename))

            except Exception as e:
                print(f"Error processing {filename}: {e}")

# user inputs for source and destination folders
source_folder_path = input("Enter the path of the source folder: ")
destination_folder_path = input("Enter the path of the destination folder: ")

# function with the provided paths
organize_photos(source_folder_path, destination_folder_path)
