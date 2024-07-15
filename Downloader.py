import requests
from tqdm import tqdm
import os

def download(url, filename=None, chunk_size=8192):
    """
    Downloads a file from a URL with a progress bar, optimized for large files.

    Args:
        url (str): The URL of the file to download.
        filename (str, optional): The filename to save the file as. If None, the filename will be extracted from the URL. Defaults to None.
        chunk_size (int, optional): The chunk size in bytes for streaming the download. Defaults to 8192.
    """

    if filename is None:
        filename = url.split('/')[-1]

    # Check if file already exists and resume if possible
    existing_size = 0
    if os.path.exists(filename):
        existing_size = os.path.getsize(filename)
        headers = {'Range': f'bytes={existing_size}-'}
    else:
        headers = {}

    response = requests.get(url, stream=True, headers=headers)
    response.raise_for_status()  # Raise an exception for bad responses

    total_size_in_bytes = existing_size + int(response.headers.get('content-length', 0))

    with open(filename, "ab" if existing_size else "wb") as handle:
        with tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, initial=existing_size, desc=filename) as pbar:
            for data in response.iter_content(chunk_size):
                handle.write(data)
                pbar.update(len(data))
