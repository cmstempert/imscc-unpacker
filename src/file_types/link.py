import os
import xml.etree.ElementTree as ET


def xml2text_links(path, file, root):
    file_check = False

    try:
        title = root[0].text

        url_string = ET.tostring(root[1])
        url_string = url_string.decode('utf-8')
        url_string = url_string.split('"')

        i = 0
        while i < len(url_string):
            if url_string[i].strip().lower() == 'href=':
                url = url_string[i + 1]
            i += 1
    except AttributeError:
        return file_check

    text = 'External link: ' + url

    filename = file.split('.')
    filename = filename[0] + '.txt'

    with open(os.path.join(path, filename), 'x') as f:
        try:
            f.write(title + '\n')
            f.write(text)
            f.close()
        except AttributeError:
            f.write(text)
            f.close()

    file_check = os.path.exists(os.path.join(path, filename))

    return file_check