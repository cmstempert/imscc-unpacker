import os
import xml.etree.ElementTree as ET
from lxml import etree, html
from handlers.file_handler import list_orig_files, move_files


def handle_resource_files(directory):
    resource_files = []
    resource_links = []

    file_path_list, file_list, html_path_list, html_file_list, xml_path_list, xml_file_list = list_orig_files(directory)
    zipped = zip(html_file_list, html_path_list)

    for file, path in zipped:
        with open(os.path.join(path, file)) as of:
            parser = etree.HTMLParser()
            tree = etree.parse(of, parser)
            result = etree.tostring(tree.getroot(), method='html')
            string_doc = html.fromstring(result)

            links = list(string_doc.iterlinks())

        for element, attribute, link, pos in links:
            resource_files.append(file)
            resource_links.append(link)

    res_orig_path = []
    res_dest_path = []

    for link in resource_links:
        file = link.split('/')
        res_orig_path.append(os.path.join(directory, file[1], file[2]))

    for file in resource_files:
        for i, item in enumerate(html_file_list):
            if file == item:
                res_dest_path.append(html_path_list[i])

    move_files(res_orig_path, res_dest_path)

    return