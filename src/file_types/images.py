import os
from handlers.file_handler import move_files

def handle_images(image_paths, image_files, file_path_list, file_list):
    flist = [x for i in image_files for x in i]

    flist2 = []
    ipath = []
    olist = []
    dlist = []
    orig = []
    dest = []

    for i, file in enumerate(flist):
        if file not in flist2:
            flist2.append(file)
            ipath.append(image_paths[i])

    zip1 = zip(ipath, flist2)

    for path, file in zip1:
        dlist.append(os.path.join(path, file))

    zipped = zip(file_path_list, file_list)

    for p2, f2 in zipped:
        for file in flist2:
            if file == f2:
                olist.append(os.path.join(p2, file))

    for item in olist:
        for thing in dlist:
            origin = item.rsplit('/', 1)
            destination = thing.rsplit('/', 1)
            if origin[1] == destination[1]:
                orig.append(item)
                dest.append(thing)

#    print(orig)
#    print(dest)

    move_files(orig, dest)

    return image_paths, image_files, file_path_list, file_list