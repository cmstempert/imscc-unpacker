import os
import re


def xml2txt_exam(path, file, root):
    #print('testing for exam')
    doc = root.findall('.//')

    file_check = False
    is_exam = False
    attribs = []
    texts = []
    image_list = []

    for elem in doc:
        attribs.append(elem.attrib)
        texts.append(elem.text)

    for i, item in enumerate(texts):
        if is_exam == True:
            break
        if (item == 'qmd_assessmenttype') and (texts[i + 1] == 'Examination'):
            is_exam = True
#            print(f'{file} is an exam')

    if is_exam == False:
        return file_check, image_list

    assess_text = []
    cleaned_assess_text = []

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

    for item in assess_text:
        if 'src=' in item:
            image = item.split('src="')
            image = image[1].split('"')
            image = image[0].split('/')
            image = image[2].strip()
            cleaned_assess_text.append('\n' + 'Insert image here: ' + image)
            image_list.append(image)

        cleaned = item.replace('<strong>', ' ')
        cleaned = cleaned.replace('</strong>', ' ')
        cleaned = re.sub('<[^>]+>', '', cleaned)
        cleaned = re.sub(r'\n+', '\n', cleaned)
        if cleaned[0] != '\n':
            cleaned = '\n' + cleaned
        cleaned_assess_text.append(cleaned)

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

#path = 'C:\\MyProgramFiles\\Projects\\imscc_unpacker\\Pincin\\ccres0000001'
#file = 'ccres0000001.xml'
#tree = ET.parse(os.path.join(path, file))
#root = tree.getroot()

#file_check, image_list = xml2txt_exam(path, file, root)
#print(f'File check: {file_check}')
#print(f'Image list: {image_list}')