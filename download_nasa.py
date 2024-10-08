import csv
import os
import requests


def extract_mission_roll_frame(tsv_file):
    mission_roll_frame_data = []

    # Open the TSV file
    with open(tsv_file, newline='', encoding='utf-8') as file:
        # Read the TSV data
        tsv_reader = csv.DictReader(file, delimiter='\t')
        
        # Extract 'mission', 'roll', and 'frame' fields
        for row in tsv_reader:
            mission = row['mission']
            roll = row['roll']
            frame = row['frame'].strip()
            mission_roll_frame_data.append((mission, roll, frame))

    return mission_roll_frame_data

def download_photos(mission_roll_frame_data, save_dir):
    base_url = "https://eol.jsc.nasa.gov/DatabaseImages/ESC/large"
    
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for mission, roll, frame in mission_roll_frame_data:
        # Format the URL using mission, roll, and frame
        photo_url = f"{base_url}/{mission}/{mission}-{roll}-{frame}.JPG"
        photo_name = f"{mission}-{roll}-{frame}.JPG"
        photo_path = os.path.join(save_dir, photo_name)

        try:
            # Request the photo
            response = requests.get(photo_url, stream=True)

            # Check if the response is OK
            if response.status_code == 200:
                # Write the photo content to a file
                with open(photo_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {photo_name}")
            else:
                print(f"Failed to download: {photo_name} (HTTP {response.status_code})")

        except Exception as e:
            print(f"Error downloading {photo_name}: {e}")


tsv_files = ['australis.tsv', 'borealis.tsv']
mission_roll_frame_data = []
for file in tsv_files:
    mission_roll_frame_data.extend(extract_mission_roll_frame(file))

save_directory = 'nasa_photos'  # Specify the directory to save the images
download_photos(mission_roll_frame_data, save_directory)

