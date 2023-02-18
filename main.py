def read_file(file: str) -> list:
    '''The function reads file'''
    empty = []
    with open(file, 'r', encoding='utf-8') as new_file:
        for line in new_file:
            if line.startswith('"'):
                line = line.strip('\n').strip('\t').split('\t')
                if line[-1].startswith('('):
                    line.pop(-1)
                while '' in line:
                    line.remove('')
                empty.append(line)
    return empty