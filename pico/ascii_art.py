import sys


def load_art_lines(fname):
    ret = []  # (parsedLine, lineNumber, originalLine)
    pos = 0
    with open(fname) as f:
        for g in f:
            org = g[:-1]
            pos += 1
            i = g.find('#')
            if i >= 0:
                g = g[:i]
            g = g.strip()
            if g:
                ret.append((g, pos, org))
    return ret


# Default character-to-index mapping. Override this with a ~MAP
color_map = {
    '.': 0,
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9
}


def decode_image(col):
    ret = []
    for row in col:
        for c in row:
            ret.append(color_map[c])
    return ret


def make_images(lines):

    ret = {}
    current_group = None
    pos = 0
    while pos < len(lines):
        line = lines[pos]
        if line[0].startswith('~MAP'):
            mappings = line[0][5:].strip().split(' ')
            for mapping in mappings:
                k, v = mapping.split('=')
                color_map[k.strip()] = int(v.strip())
        elif line[0].startswith('~GROUP'):
            info = line[0][7:].strip()
            i = info.index(' ')
            group_name = info[:i]
            dims = info[i+1:].split('x')
            group_width = int(dims[0].strip())
            group_height = int(dims[1].strip())
            current_group = {'width': group_width, 'height': group_height, 'images': []}
            ret[group_name] = current_group
        else:
            current_group['images'].append(line)

        pos += 1

    for value in ret.values():
        w = value['width']
        h = value['height']
        lines = value['images']
        num_rows = len(lines)//h
        if len(lines) % h:
            raise Exception(f'Not enough rows in {value}')
        extracted = []
        for i in range(num_rows):
            pic_set = lines[i*h:(i+1)*h]
            data = pic_set[0][0].replace(' ', '')
            num_cols = len(data)//w
            if len(data) % w:
                raise Exception(f'Not enough columns in {pic_set}')
            columns = []
            for i in range(num_cols):
                columns.append([])
            for row in pic_set:
                data = row[0].replace(' ', '')
                if len(data) != num_cols*w:
                    raise Exception(f'Column is missing characters {row}')
                for i in range(num_cols):
                    columns[i].append(data[i*w:(i+1)*w])
            for col in columns:
                extracted.append(decode_image(col))
        value['images'] = extracted

    return ret


if __name__ == '__main__':
    lines = load_art_lines(sys.argv[1])
    img = make_images(lines)
    print(img)
