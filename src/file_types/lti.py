import os


def xml2txt_lti(path, file, root):
    file_check = False
    prefix_map = {'blti': 'http://www.imsglobal.org/xsd/imsbasiclti_v1p0'}

    try:
        title = root.find('./blti:title', prefix_map).text
        text = 'Linked to Turnitin'
    except AttributeError:
        return file_check

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