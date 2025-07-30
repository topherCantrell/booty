from copy import Error

def text_to_data(s,mapping):
    """convert ascii-art image characters to color indices
    """    
    ret = bytearray(len(s))
    pos = 0
    while (pos < len(s)):
        c = s[pos]
        ret[pos] = mapping[c]     
        pos += 1   
    return ret

def resize(data, data_width, to_width):
    """resize the data to a new width, padding with zeros if necessary.

    We have two sizes of panels: 32x24 and 29x24. The difference is three 
    columns on the right side.
    """
    return data
    

def weave32x24(im):
    """map a 768 pixel image onto the three panel strips.

    Returns:
       n1, n2, and n3 for neo1, neo2, and neo3
    """

    n1 = bytearray(256)  # bottom right, but upside down
    n2 = bytearray(256)  # upper right
    n3 = bytearray(256)  # upper left
    raise NotImplementedError("Weaving for 32x24 not implemented yet")

def weave29x24(im):
    """map a 696 pixel image onto the three panel strips.

    Returns:
       n1, n2, and n3 for neo1, neo2, and neo3
    """

    n1 = bytearray(232)  # bottom right, but upside down
    n2 = bytearray(208)  # upper right
    n3 = bytearray(256)  # upper left

    # Weave the upper left panel
    y = 0
    while y < 16:
        x = 0
        while x < 16:
            n3[x*16+y] = im[y*29+x]
            n3[(x+1)*16+(15-y)] = im[y*29+x+1]
            x += 2
        y += 1
    # Now the upper right panel
    y = 0
    while y < 16:
        x = 0
        while x < 14:
            n2[x*16+y] = im[y*29+x+16]
            if x < 12:
                n2[(x+1)*16+(15-y)] = im[y*29+x+1+16]
            x += 2
        y += 1
    # Finally, the bottom panel
    y = 0
    while y < 8:
        x = 0
        while x < 30:
            n1[x*8+y] = im[(23-y)*29+(28-x)]
            if x < 28:
                n1[(x+1)*8+(7-y)] = im[(23-y)*29+(28-x-1)]
            x += 2
        y += 1
    return n1, n2, n3

def get_next_line(lines, index):
    """Remove comments and skip blank lines"""
    while True:
        if index >= len(lines):
            return None, index
        line = lines[index].strip()        
        index += 1
        i = line.find('#')
        if i != -1:
            line = line[:i].strip()
        if line:
            return line, index        

def make_movie(fname, outname, to_width):
    records = []
    with open(fname, 'r') as f:
        lines = f.read().splitlines()

        # Lines are grouped together into records -- multiple "color" or "map" or
        # lines of "frame" data. We collect all the groupings first.
        index = 0
        while True:
            line, index = get_next_line(lines, index)
            if line is None:
                break
            if line.startswith('~'):
                line = line[1:].strip().lower()
                if line.startswith('pause'):                    
                    delay = int(line[5:].strip())                    
                    rec = ['pause', delay]
                    records.append(rec)
                elif line.startswith('color'):
                    spec = line[5:].strip()
                    i = spec.find(' ')
                    cind = int(spec[:i])
                    tup = spec[i+1:].strip()
                    if tup.startswith('(') and tup.endswith(')'):
                        tup = tup[1:-1]
                    tup = tup.split(',')
                    r = int(tup[0].strip())
                    g = int(tup[1].strip())
                    b = int(tup[2].strip())
                    if records and records[-1][0] == 'color':
                        records[-1].append(cind)
                        records[-1].append((r, g, b))
                    else:
                        records.append(['color', cind, (r, g, b)])
                elif line.startswith('map'):
                    line = line[3:].strip()
                    line = line.split(' ')
                    for mapping in line:
                        mapping = mapping.split('=')
                        key = mapping[0]
                        value = int(mapping[1])
                        if records and records[-1][0] == 'map':
                            records[-1][1][key] = value
                        else:
                            records.append(['map', {key: value}])                        
                else:
                    raise Error(f'Unknown command at {index}: {line}')

            else:                
                line = line.replace(' ', '')
                line = line.replace('.', '0')
                line = line.replace('|', '')
                line = line.replace('-', '')
                if records and records[-1][0] == 'frame':
                    records[-1][2] += line
                else:
                    records.append(['frame', len(line), line])                

    # Process the records into the binary file. 

    # This is our default character mapping.
    color_palette_map = {
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
        '9': 9,
    }

    with open(outname, 'wb') as out:
        for record in records:
            if record[0] == 'pause':
                data = [2, 2, 0, record[1] & 0xFF, (record[1] >> 8) & 0xFF]
                out.write(bytearray(data))  # Pause command                
            elif record[0] == 'color':
                colors = record[1:]
                pal = []
                for i in range(0,len(colors),2):
                    pal.append(colors[i])
                    pal.append(colors[i+1][0])
                    pal.append(colors[i+1][1])
                    pal.append(colors[i+1][2])
                data = [1, len(pal)&0xFF, (len(pal) >> 8) & 0xFF] + pal
                out.write(bytearray(data))                
            elif record[0] == 'map':
                for key, value in record[1].items():
                    color_palette_map[key] = value
            elif record[0] == 'frame':
                data = resize(record[2], record[1], to_width)                
                data = text_to_data(data, color_palette_map)
                if to_width == 32:
                    data = weave32x24(data)
                else:
                    data = weave29x24(data)
                data = data[0] + data[1] + data[2]
                data = bytearray([3, len(data)&0xFF, (len(data) >> 8) & 0xFF]) + data
                out.write(bytearray(data))
            else:
                raise Error(f'Unknown record type: {record[0]}')
    

make_movie('pac.txt', 'pac.bin', to_width=29)