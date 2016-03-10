def nexline(f):
    return float(next(f, '-inf'))


def is_end(line):
    return line == float('-inf')


def write_new_line(new_f, source_f, line):
    new_f.write("{}\n".format(line))
    source_line = nexline(source_f)
    return source_line


with open('a.txt') as fa, open('b.txt') as fb, open('new.txt', 'w') as fn:
    line_a, line_b = nexline(fa), nexline(fb)
    while not is_end(line_a) or not is_end(line_b):
        if not is_end(line_a) and line_a < line_b:
            line_a = write_new_line(fn, fa, line_a)
        else:
            line_b = write_new_line(fn, fb, line_b)


class MergeAndSortFiles(object):
    def __init__(files, new_file='new.text'):
        self.files = files
        self.new_file = new_file

    def open_files(self):
        self.files = [open(filename, 'r') for filename in self.files]
        self.new_file = open(self.new_file, 'r')

    def nextline(self, index):
        iterator = self.files[index]
        default = '-inf'
        result = next(iterator, default)
        return float(result)

    def all_end(self, lines):
        f_lines = filter(self.is_end, lines)
        return all(f_lines)

    def merge_and_sort(self):
        lines = map(lambda i, _: self.nextline(i), enumerate(self.files))
        target = min(lines)
        while not all_end(lines):
            for index, line in enumerate(lines):
                if not is_end(line) and line < target:
                    self.write_new_line_in_file(line)
                    lines[index] = self.nextline(self.files[index])

    def write_new_line_in_file(new_line):
        self.new_file.write("{}\n".format(new_line))
        source_line = self.nextline(source_file)
        return source_line

    def close_files(self):
        self.files = [f.close() for f in self.files]
        self.new_file.close()

    @staticmethod
    def is_end(line):
        '''is_end'''
        return line == float('-inf')
