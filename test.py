import os
import time
import mechanicalsoup
import sys

def read_and_increment_log_file():
    # Get the directory of the script
    script_directory = os.path.dirname(__file__)
    log_file_path = os.path.join(script_directory, "log.txt")

    if os.path.isfile(log_file_path):
        with open(log_file_path, 'r') as log_file:
            try:
                current_value = int(log_file.readline())
            except ValueError:
                current_value = 0

        current_value += 1

        with open(log_file_path, 'w') as log_file:
            log_file.write(str(current_value))

        return current_value

    else:
        with open(log_file_path, 'w') as log_file:
            log_file.write("1")
        return 1

def get_text_files_in_folder(folder_path):
    text_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            text_files.append(filename)
    return text_files

def submit_links_from_file(file_path):
    # Create a new browser instance
    browser = mechanicalsoup.StatefulBrowser()

    # List of websites to submit links
    websites = [
        'https://real.discount/contact/'
    ]

    # Iterate over each website
    for website in websites:
        # Open the website's submission page
        browser.open(website)

        # Read the links from the file
        with open(file_path, 'r') as file:
            links = file.read().splitlines()

        # Iterate over the links and submit them
        for link in links:
            # Fill in the form fields with the link, name, and email
            if website == 'https://real.discount/contact/':
                print('------------Current website: real.discount------------')
                browser.select_form('form[action="/contact/"]')
                browser["urls"] = link

            # Submit the form
            
            response = browser.submit_selected()
            print(response)
                
                # Check if the submission was successful
            if response.ok:
                print('Link submitted successfully:', link)
            else:
                print('Failed to submit the link:', link)

            time.sleep(3)


    print('All links submitted!')

# Get the directory of the script
script_directory = os.path.dirname(__file__)

# Folder containing text files (within the same directory as the script)
folder_name = 'DATA'  # Replace 'your_folder_name' with the actual folder name
folder_path = os.path.join(script_directory, folder_name)

# Read and increment the log file to determine which file to process
file_index = read_and_increment_log_file()

# Get a list of text files in the folder
text_files = get_text_files_in_folder(folder_path)

# Check if the file index is valid
if 1 <= file_index <= len(text_files):
    file_name = text_files[file_index - 2]
    file_path = os.path.join(folder_path, file_name)
    print("Processing", file_path)
    submit_links_from_file(file_path)
else:
    print("File index out of range.")

# You can optionally delete the processed file here if needed
# os.remove(file_path)
