'''
Python script to find duplicate files.
'''
import os, sys
import hashlib

def find_dup(parent_folder):
    # Dups in format {hash:[names]}
    dups = {}
    for dir_name, subdirs, file_list in os.walk(parent_folder):
        print(f'Scanning {dir_name}...')
        for filename in file_list:
            path = os.path.join(dir_name, filename)  # Get the path to the file
            file_hash = hashfile(path)  # Calculate hash
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups


# Joins two dictionaries
def join_dicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def print_results(dict):
    results = list(filter(lambda x: len(x) > 1, dict.values()))
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        print('___________________')
        for result in results:
            for subresult in result:
                print('\t\t%s' % subresult)
            print('___________________')
    else:
        print('No duplicate files found.')


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1:
        dups = {}
        folders = sys.argv[1:]
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                join_dicts(dups, find_dup(i))
            else:
                print('%s is not a valid path, please verify' % i)
                sys.exit()
        print_results(dups)
    else:
        print('Usage: python dup_finder.py folder or python dup_finder.py folder1 folder2 folder3')
        print('Scan all here with: "python dup_finder.py ."')
