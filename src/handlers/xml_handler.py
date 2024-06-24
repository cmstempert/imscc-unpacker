import os
import xml.etree.ElementTree as ET
from file_types.exam import xml2txt_exam
from file_types.assessment import xml2txt_assessment
from file_types.lti import xml2txt_lti
from file_types.text import xml2txt_text
from file_types.link import xml2text_links
from file_types.images import handle_images
from handlers.file_handler import list_orig_files


def convert_xml_files(directory):
    unconverted_xml = []
    file_path_list, file_list, html_path_list, html_file_list, xml_path_list, xml_file_list = list_orig_files(directory)

    zipped = zip(xml_path_list, xml_file_list)

    for path, file in zipped:
        image_files = []
        image_paths = []

#        print(os.path.join(path, file))
        try:
            file_check = False
            tree = ET.parse(os.path.join(path, file))
            root = tree.getroot()
        except ET.ParseError:
            try:
                with open(os.path.join(path, file), 'r') as f:
                    data = f.read()
                    data = data.replace('&ldquo', '').replace('&rdquo', '').replace('&rsquo', '').replace('&ntilde', 'n')
                with open(os.path.join(path, 'temp.xml'), 'w') as f:
                    f.write(data)
                os.remove(os.path.join(path, file))
                os.rename(os.path.join(path, 'temp.xml'), os.path.join(path, file))
                file_check = False
                tree = ET.parse(os.path.join(path, file))
                root = tree.getroot()
            except:
                unconverted_xml.append(os.path.join(path, file))
                print(f'Parse Error for {file} at {path}')
                continue

        file_check, image_list = xml2txt_exam(path, file, root)
        #print('file_check 1 for ' + file + ' is ' + str(file_check))
        if len(image_list) > 0:
            image_files.append(image_list)
            for item in image_list:
                image_paths.append(path)
        #print(f'File check assessment: {file_check}')
        #print(f'image_list assessment: {image_files}')
        #print(f'image_list assessment: {image_paths}')
        if file_check is False:
            file_check, image_list = xml2txt_assessment(path, file, root, file_path_list, file_list)
            if len(image_list) > 0:
                image_files.append(image_list)
                for item in image_list:
                    image_paths.append(path)
            #print(f'File check exam: {file_check}')
            #print(f'image_list exam: {image_files}')
            #print(f'image_list exam: {image_paths}')
            if file_check is False:
                file_check = xml2txt_lti(path, file, root)
                #print('file_check 2 for ' + file + ' is ' + str(file_check))
                if file_check is False:
                    file_check = xml2txt_text(path, file, root)
                    #print('file_check 3 for ' + file + ' is ' + str(file_check))
                    if file_check is False:
                        file_check = xml2text_links(path, file, root)
                        #print('file_check 4 for ' + file + ' is ' + str(file_check))
                        if file_check is False:
                            unconverted_xml.append(os.path.join(path, file))
                            continue

        handle_images(image_paths, image_files, file_path_list, file_list)
        os.remove(os.path.join(path, file))

    return unconverted_xml
