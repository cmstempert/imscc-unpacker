import os
import shutil
import zipfile


def list_imscc_files(path):
    imscc_files = []
    # Find all files with extension .imscc
    for file in os.listdir(path):
        if file.endswith('.imscc'):
            imscc_files.append(file)
    
    return imscc_files

def unpack_imscc_files(imscc_files, path):
    imscc_names = []
    unpacked_directories = []

    for i, file in enumerate(imscc_files):
        imscc_names.append(file.split(".")[0])
        filename = imscc_names[i] + ".zip"
        os.rename(file, filename)

        zip_file = os.path.join(path, filename)

        new_dir = os.path.join(path, imscc_names[i])  # May want to account for spaces in names
        os.mkdir(new_dir)

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(new_dir)

        unpacked_directories.append(new_dir)
        os.remove(zip_file)
    
    return imscc_names, unpacked_directories

def set_file_paths(directory, folder_path_list):
    joined_paths = []
    
    for path in folder_path_list:
        joined_name = directory

        split = path.split('|')

        for item in split:
            joined_name = os.path.join(joined_name, item)
        
        joined_paths.append(joined_name)

    return joined_paths

def create_new_directories(mk_dir_list):
    for idref, path in mk_dir_list:
        if idref is None:
            os.mkdir(path)
    
    return

def list_orig_files(directory):
    file_path_list = []
    file_list = []
    html_path_list = []
    html_file_list = []
    xml_path_list = []
    xml_file_list = []

    for path, subdirs, files in os.walk(directory):
        for name in files:
            # Exclude manifest as it is not part of course contents
            if name == 'imsmanifest.xml':
                continue
            elif 'html' in name:
                html_path_list.append(path)
                html_file_list.append(name)
            elif 'xml' in name:
                xml_path_list.append(path)
                xml_file_list.append(name)

            file_path_list.append(path)
            file_list.append(name)

    return file_path_list, file_list, html_path_list, html_file_list, xml_path_list, xml_file_list

def move_files(origin, destination):
    zipped_files = zip(origin, destination)

    for orig, des in zipped_files:
#        print(f'File moved from: {orig} to {des}')
        shutil.move(orig, des)
    
    return

def cleanup_directory(directory):
    for item in os.listdir(directory):
        if ('ccres' in item) or ('resources' in item):
            os.rmdir(os.path.join(directory, item))
        elif 'manifest' in item:
            os.remove(os.path.join(directory, item))
    
    return

def list_new_files(directory):
    file_path_list = []
    file_list = []

    for path, subdirs, files in os.walk(directory):
        for name in files:
            file_path_list.append(path)
            file_list.append(name)
        for name in subdirs:
            file_path_list.append(path)
            file_list.append(name)

    return file_path_list, file_list

def rename_files(directory, identifier_list, id_ref_list, clean_txt_list):
    file_path_list, file_list = list_new_files(directory)

    new_file_structure = zip(file_path_list, file_list)
    folder_paths = []
    folder_names = []

    for path, file in new_file_structure:
        try:
            file_no_ext = file.split('.')
            extension = file_no_ext[1]
            file_no_ext = file_no_ext[0].strip()
        except IndexError:
            folder_paths.append(path)
            folder_names.append(file)
            continue

        if file_no_ext in id_ref_list:
            new_name = clean_txt_list[id_ref_list.index(file_no_ext)] + '.' + extension
            os.rename(os.path.join(path, file), os.path.join(path, new_name))
        
    folder_paths.reverse()
    folder_names.reverse()
    folder_zip = zip(folder_paths, folder_names)

    for path, file in folder_zip:
        if file in identifier_list:
            new_name = clean_txt_list[identifier_list.index(file)]
            os.rename(os.path.join(path, file), os.path.join(path, new_name))

def zip_files(directory):
    file_name = directory.rsplit('/', 1)
    print("FILE NAME: ", file_name)
    shutil.make_archive(file_name[1], 'zip', directory)
    shutil.rmtree(directory)
