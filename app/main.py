import requests
import shutil
from zipfile import ZipFile
from config import load_cofing
from pathlib import Path




def create_download_directory(directory:Path):
    """
    Create the download directory if it doesn't exist.

    Parameters:
        directory (Path): The directory to create.
    """
    if not directory.exists():
        directory.mkdir()




def extract_file_name(url:str)->str:
    """
    Extract the file name from the URL.

    Parameters:
        url (str): The URL of the file.

    Returns:
        str: The extracted file name.
    """
    return url.split('/')[3]




def download_file(url:str, directory:Path, name_zip:str)-> Path:
    """
    Download the file from the given URL to the specified directory.

    Parameters:
        url (str): The URL of the file to download.
        directory (Path): The directory where the file will be saved.
        name_zip (str): The name of the file.

    Returns:
        Path: The path to the downloaded file.
    """
    file_path = directory / name_zip 
    headers = {"Accept-Encoding": "gzip, deflate"}
    response = requests.get(url, stream=True, headers=headers)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    return file_path




def extract_zip(archive_path:Path, directory:Path)-> Path:
    """
    Extract the contents of the ZIP archive to the specified directory.

    Parameters:
        archive_path (Path): The path to the ZIP archive.
        directory (Path): The directory where the files will be extracted.

    Returns:
        Path: The path to the extracted files.
    """
    archive_name = archive_path.stem
    with ZipFile(archive_path, 'r') as zip_object:
        zip_object.extractall(directory / archive_name)
    return directory / archive_name




def delete_archives(archive_path:Path, directory:Path):
    """
    Delete the ZIP archive and its extracted directory.

    Parameters:
        archive_path (Path): The path to the ZIP archive.
        directory (Path): The directory where the archive and extracted files are located.
    """
    archive_path.unlink()
    extracted_directory = directory / archive_path.stem
    shutil.rmtree(extracted_directory)




def move_files(file_path:Path, destination_directory:Path):
    """
    Move files to the destination directory.

    Parameters:
        file_path (Path): The path to the files to be moved.
        destination_directory (Path): The destination directory.
    """
    for file in file_path.glob("*.*"):
        shutil.move(file, destination_directory)




if __name__ == '__main__':
    # Load configuration
    config = load_cofing()
    # Current directory
    directory_path = Path.cwd() / config.get('name_directory')
    # create directory exists
    create_download_directory(directory_path)
    print("Starting to download files...")
    # Iterate over download URLs
    for url in config.get('download_uris'):
        file_name = extract_file_name(url)
        print(f"Downloading file: {file_name}")
        try:
            archive_path = download_file(url, directory_path, file_name)
        except requests.exceptions.HTTPError as err:
            print(err)
            continue
        extracted_files_path = extract_zip(archive_path, directory_path)
        move_files(extracted_files_path, directory_path)
        delete_archives(archive_path, directory_path)
    print("Download complete.")





