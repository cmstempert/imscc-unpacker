import os
import xml.etree.ElementTree as ET


def parse_xml_strings(directory):
    text_list = []
    attribute_list = []

    tree = ET.parse(os.path.join(directory, 'imsmanifest.xml'))
    root = tree.getroot()

    for element in root.findall('.//'):
        text_list.append(element.text)
        attribute_list.append(element.attrib)

    i = 0
    aligned_attrib_list = []
    aligned_text_list = []

    while i < len(attribute_list) - 1:
        if len(attribute_list[i]) != 0:
            aligned_attrib_list.append(attribute_list[i])
            aligned_text_list.append(text_list[i + 1])
        i += 1

    zipped = zip(aligned_attrib_list, aligned_text_list)
    cleaned_attr_list = []
    cleaned_txt_list = []

    for attr, txt in zipped:
        if 'identifier' in attr and attr['identifier'] != 'org' and attr['identifier'] != 'root':
            cleaned_attr_list.append(attr)
            cleaned_txt_list.append(txt)

    cleaned_zip_list = zip(cleaned_attr_list, cleaned_txt_list)

    no_name_list = []

    for item in cleaned_zip_list:
        if item[1] is not None:
            no_name_list.append(item)

    attr_list, txt_list = zip(*no_name_list)
    
    identifier_list = []
    id_ref_list = []

    for entry in attr_list:
        identifier_list.append(entry['identifier'])
        if ('identifierref' in entry) is True:
            id_ref_list.append(entry['identifierref'])
        else:
            id_ref_list.append(None)

    return identifier_list, id_ref_list, txt_list

def parse_folder_structure(directory):
    manifest = ET.parse(os.path.join(directory, 'imsmanifest.xml'))
    root = manifest.getroot()
    organization = root[1][0][0]

    folder_paths = []

    for course in organization:
        folder_paths.append(course.attrib['identifier'])
        for level_1_folder in course:
            try:
                folder_paths.append(course.attrib['identifier'] + '|' + level_1_folder.attrib['identifier'])
                for level_2_folder in level_1_folder:
                    try:
                        folder_paths.append(course.attrib['identifier'] + '|' + level_1_folder.attrib['identifier'] + '|' + level_2_folder.attrib['identifier'])
                        for level_3_folder in level_2_folder:
                            try:
                                folder_paths.append(course.attrib['identifier'] + '|' + level_1_folder.attrib['identifier'] + '|' + level_2_folder.attrib['identifier'] + '|' + level_3_folder.attrib['identifier'])
                                for level_4_folder in level_3_folder:
                                    try:
                                        folder_paths.append(course.attrib['identifier'] + '|' + level_1_folder.attrib['identifier'] + '|' + level_2_folder.attrib['identifier'] + '|' + level_3_folder.attrib['identifier'] + '|' + level_4_folder.attrib['identifier'])
                                    except KeyError:
                                        pass
                            except KeyError:
                                pass
                    except KeyError:
                        pass
            except KeyError:
                pass
    
    return folder_paths