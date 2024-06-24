import os
import re


def xml2txt_assessment(path, file, root, file_path_list, file_list):
    file_check = False
    doc = root.findall('.//')

    attribs = []
    texts = []
    assess_text = []
    cleaned_assess_text = []
    image_list = []

    for elem in doc:
        attribs.append(elem.attrib)
        texts.append(elem.text)
    
    try:
        title = attribs[0]['title']
    except KeyError:
        return file_check, image_list

    zipped = zip(attribs, texts)

    for attrib, text in zipped:
        if (attrib.get('ident') != None) and ('ccres' not in attrib.get('ident')) \
                and ('root' not in attrib.get('ident')) and ('rcardinality' in attrib):
            assess_text.append(attrib.get('ident'))
        elif 'texttype' in attrib:
            assess_text.append(text)

    for count, thing in enumerate(assess_text):
        try:
            num = int(thing)
            assess_text.remove(assess_text[count])
            assess_text.insert(count - 1, str(num))
        except:
            pass

#    cleaned_assess_text.append('tagged as assessment')

    for item in assess_text:
        cleaned = item.replace('<strong>', ' ')
        cleaned = cleaned.replace('</strong>', ' ')
        cleaned = re.sub('<[^>]+>', '', cleaned)
        cleaned = '\n' + cleaned
        cleaned_assess_text.append(cleaned)

        if '<img src=' in item:
            cleaned_count = item.count('/') - 1
            image = item.split('/', cleaned_count)
            image = image[2]
            image = image.split('"')
            image = image[0].strip()
            cleaned_assess_text.append('\nInsert image here: ' + image)
            image_list.append(image)

    text = ''.join(cleaned_assess_text)

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

    return file_check, image_list