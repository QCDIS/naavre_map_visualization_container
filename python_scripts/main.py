import argparse
import json
import os
import time

import download_files
import prepare_input


def main():
    # Fetch necessary credentials
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--hostname', action='store', type=str, required=True, dest='hostname')
    arg_parser.add_argument('--username', action='store', type=str, required=True, dest='username')
    arg_parser.add_argument('--password', action='store', type=str, required=True, dest='password')
    arg_parser.add_argument('--remote_file_path', action='store', type=str, required=True, dest='remote_file_path')
    arg_parser.add_argument('--num_files', action='store', type=str, required=True, dest='num_files')
    arg_parser.add_argument('--mode', action='store', type=str, required=True, dest='mode')
    arg_parser.add_argument('--output_dir', action='store', type=str, required=True, dest='output_dir')
    args = arg_parser.parse_args()

    hostname = args.hostname
    username = args.username
    password = args.password
    remote_file_path = args.remote_file_path
    num_files_str = args.num_files
    mode = args.mode
    output_dir = args.output_dir
    # Define file paths and data types required
    geotiff_files_path = os.path.join(output_dir, 'geotiff_files')
    pngs_files_path = './pngs_files'
    json_file_path = './data.json'
    json_dict = {}
    extensions = (".tif", ".TIF", ".tiff", "TIFF")

    print('Arguments:' + '\n' + 'hostname: ' + hostname + '\n' + 'username: ' + username + '\n' + 'password: ' +
          password + '\n' + 'remote_file_path: ' + remote_file_path + '\n' + 'num_files: ' + num_files_str + '\n' +
          'mode: ' + mode + '\n' + 'output_dir: ' + output_dir + '\n')

    # Create required directories and files if they do not exist
    download_files.create_directory_if_not_exists(geotiff_files_path)
    download_files.create_directory_if_not_exists(pngs_files_path)
    download_files.create_file_if_not_exists(json_file_path)

    # Time the execution of download_files function in milliseconds
    start_time_download = time.time()
    download_files.download_using_credentials(hostname, username, password, remote_file_path, num_files_str, mode,
                                              extensions, geotiff_files_path)
    end_time_download = time.time()
    elapsed_time_download = (end_time_download - start_time_download) * 1000  # Convert to milliseconds
    print("download_files execution time: {} milliseconds".format(elapsed_time_download))

    # Time the execution of prepare_input function in milliseconds
    start_time_prepare_input = time.time()
    prepare_input.prepare_input_for_application(geotiff_files_path, pngs_files_path, json_file_path, json_dict,
                                                extensions)
    end_time_prepare_input = time.time()
    elapsed_time_prepare_input = (end_time_prepare_input - start_time_prepare_input) * 1000  # Convert to milliseconds
    print("prepare_input execution time: {} milliseconds".format(elapsed_time_prepare_input))
    # print json_file_path content to stdout with indentation
    with open(json_file_path) as json_file:
        contents = json.load(json_file)
    print(json.dumps(contents, indent=4))


if __name__ == "__main__":
    main()
