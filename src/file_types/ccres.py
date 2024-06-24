import os
from handlers.file_handler import set_file_paths, move_files


def handle_ccres_files(directory, file_path_list, file_list, id_ref_list, folder_path_list):
    res_type = []

    for path in file_path_list:
        split = path.split('/')
        res_type.append(split[-1])

    zipped = zip(res_type, file_path_list, file_list)

    ccres_origin_paths = []
    ccres_destination = []
    ccres_files_to_move = []

    for res, orig_path, file in zipped:
        if res in id_ref_list:
            ccres_origin_paths.append(os.path.join(orig_path, file))
            ccres_destination.append(folder_path_list[id_ref_list.index(res)])
            ccres_files_to_move.append(file)

    dest_paths = set_file_paths(directory, ccres_destination)
    ccres_destination_paths = []

    for i, dest in enumerate(dest_paths):
        split = dest.split('/')
        split = '/'.join(split[:-1])
        new_path = os.path.join(split, ccres_files_to_move[i])
        ccres_destination_paths.append(new_path)

    move_files(ccres_origin_paths, ccres_destination_paths)

    return