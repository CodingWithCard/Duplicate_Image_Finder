import os
import hashlib
import tkinter as tk
from tkinter import filedialog

def get_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def scan_directory(directory):
    images = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.png', '.jpg')):
                images.append(os.path.join(root, file))
    return images

def find_duplicates(directory):
    hashes = {}
    duplicates = []
    images = scan_directory(directory)
    for image in images:
        image_hash = get_hash(image)
        if image_hash in hashes:
            duplicates.append(image)
        else:
            hashes[image_hash] = image
    duplicate_folder = os.path.join(directory, 'duplicates')
    if not os.path.exists(duplicate_folder):
        os.makedirs(duplicate_folder)
    for duplicate in duplicates:
        os.rename(duplicate, os.path.join(duplicate_folder, os.path.basename(duplicate)))
    return len(duplicates)

root = tk.Tk()
root.withdraw()

while True:
    directory = filedialog.askdirectory()
    if not directory:
        print('No directory selected. Please try again')
        continue
    num_duplicates = find_duplicates(directory)
    print(f'Found {num_duplicates} duplicates. They have been moved to the "duplicates" folder in the selected directory.')
    break
