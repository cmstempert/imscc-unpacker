import os


def xml2txt_text(path, file, root):
    text_loaded = False
    file_check = False

    try:
        title = root.find('./title').text
        text = root.find('./text').text
        text_loaded = True
    except AttributeError:
        pass

    if text_loaded is False:
        try:
            text = root.find('./text').text
        except AttributeError:
            file_check = False
            return file_check

    text = text.replace('<p>', '\n')
    text = text.replace('<[^>]+>', '')

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