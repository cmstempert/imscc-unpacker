import os
import sys
import file_types as ft
from handlers import file_handler, xml_handler


def name_cleaner(name):
    clean_name = name.strip().replace(':', '').replace('(', '').replace(')', '').replace(',', '') \
        .replace('/', '-').replace(' ', '_').replace('?', '')

    return clean_name

def main():
    cwd = input("Please input full directory path: ")
    os.chdir(cwd)

    imscc_list = file_handler.list_imscc_files(cwd)
    imscc_names, unpacked_directories = file_handler.unpack_imscc_files(imscc_list, cwd)

    for directory in unpacked_directories:
        identifier_list, id_ref_list, txt_list = ft.manifest.parse_xml_strings(directory)

        clean_txt_list = []
        for name in txt_list:
            clean_name = name_cleaner(name)
            clean_txt_list.append(clean_name)

        folder_path_list = ft.manifest.parse_folder_structure(directory)
        joined_paths = file_handler.set_file_paths(directory, folder_path_list)

        file_path_list, file_list, html_path_list, html_file_list, xml_path_list, xml_file_list = file_handler.list_orig_files(directory)

        mk_dir_list = zip(id_ref_list, joined_paths)
        file_handler.create_new_directories(mk_dir_list)

        ft.ccres.handle_ccres_files(directory, file_path_list, file_list, id_ref_list, folder_path_list)
        ft.resource.handle_resource_files(directory)

        unconverted_xml = xml_handler.convert_xml_files(directory)
        if len(unconverted_xml) > 0:
            print(unconverted_xml)

        try:
            file_handler.cleanup_directory(directory)
        except OSError:
            print("issue with directory: ", directory)

        file_handler.rename_files(directory, identifier_list, id_ref_list, clean_txt_list)

        file_handler.zip_files(directory)

if __name__ == "__main__":
    main()
