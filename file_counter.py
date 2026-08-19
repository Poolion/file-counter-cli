# file_counter.py
import os
import re

def count_files_in_dir(directory, extension=None):
    counter = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if extension is None or re.search(r'\.' + extension + '$', file, re.IGNORECASE):
                counter += 1
    return counter

def main():
    directory = './test DIRECTORY/'
    extension = 'txt'  # Example extension
    print(f'Number of {extension} files in {directory}: {count_files_in_dir(directory, extension)}')

if __name__ == '__main__':
    main()