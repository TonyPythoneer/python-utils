class MergeAndSortFiles(object):
    def __init__(self, files, new_file='new.txt'):
        self.files = files
        self.new_file = new_file

    def open_files(self):
        self.files = [open(filename, 'r') for filename in self.files]
        self.new_file = open(self.new_file, 'w')

    def nextline(self, index):
        iterator = self.files[index]
        default = '-inf'
        result = next(iterator, default)
        return float(result)

    def all_end(self, lines):
        f_lines = map(lambda l: self.is_end(l), lines)
        return all(f_lines)

    def merge_and_sort(self):
        lines = [self.nextline(i) for i, _ in enumerate(self.files)]
        target = min(lines)
        while not self.all_end(lines):
            print target, lines
            for index, line in enumerate(lines):
                if self.is_not_end(line) and line == target:
                    self.write_new_line_in_file(target)
                    lines[index] = self.nextline(index)

                    rest_lines = filter(self.is_not_end, lines)
                    if rest_lines:
                        target = min(rest_lines)

    def write_new_line_in_file(self, new_line):
        self.new_file.write("{}\n".format(new_line))

    def close_files(self):
        self.files = [f.close() for f in self.files]
        self.new_file.close()

    @staticmethod
    def is_end(line):
        '''is_end'''
        return line == float('-inf')

    @staticmethod
    def is_not_end(line):
        '''is_not_end'''
        return line != float('-inf')


if __name__ == '__main__':
    action = MergeAndSortFiles(files=['a.txt', 'b.txt', 'c.txt'])
    action.open_files()
    action.merge_and_sort()
    action.close_files()
