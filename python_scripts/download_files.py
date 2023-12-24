import os

import requests
from webdav3.client import Client


## Create necessary directories and file if not existing yet.
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")


def create_file_if_not_exists(filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")

    if not os.path.isfile(filename):
        with open(filename, "w") as file:
            file.write("")  # Write an empty string to create the file
        print(f"File '{filename}' created.")
    else:
        print(f"File '{filename}' already exists.")


def download_using_credentials(hostname, username, password, remote_file_path, num_files_str, mode, extensions,
                               geotiff_files_path):
    print('download_using_credentials: ' + hostname + ' ' + username + ' ' + password + ' ' + remote_file_path + ' ' +
          num_files_str + ' ' + mode + ' ' + str(extensions) + ' ' + geotiff_files_path)

    try:
        if mode == "webdav":
            print('mode: webdav')
            # For now only support webdav
            options = {
                'webdav_hostname': hostname,
                'webdav_login': username,
                'webdav_password': password
            }
            client = Client(options)
            check = client.check(remote_path=remote_file_path)
            print('check: ' + str(check))
            # Check if NUM_FILES is an integer

            num_files = int(num_files_str)
            print('num_files: ' + str(num_files))

            # Retrieve a list of remote files first
            print('client.list(remote_path=remote_file_path')
            remote_files = client.list(remote_path=remote_file_path)
            print('remote_files: ' + str(remote_files))

            # Filter the files in the list based on the specified extensions
            filtered_files = [file for file in remote_files if file.endswith(extensions)]
            print('filtered_files: ' + str(filtered_files))

            # If NUM_FILES is not positive or larger than the list of filtered files, download all filtered files
            if num_files <= 0 or num_files > len(filtered_files):
                num_files = len(filtered_files)

            # Download only the filtered files
            for file in filtered_files[:num_files]:
                client.download(remote_path=os.path.join(remote_file_path, file),
                                local_path=os.path.join(geotiff_files_path, file))
        elif mode == "macaroon":
            # Macaroon = password, remote_file_path = full file path (including hostname) to a single file
            # Multiple files in one directory is not supported for macaroons
            # Save the downloaded file
            macaroon_filename = remote_file_path.split('/')[-1]
            file_path = os.path.join(geotiff_files_path, macaroon_filename)
            headers = {'Authorization': f'Bearer {password}'}

            try:
                response = requests.get(remote_file_path, headers=headers)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"File downloaded and saved to: {file_path}")
                else:
                    print(f"Request failed with status code: {response.status_code}")
                    print(response.text)

            except requests.exceptions.RequestException as e:
                print(f"Error occurred during the request: {e}")
    except Exception as e:
        print('download_using_credentials failed: ' + str(e))
        raise e
