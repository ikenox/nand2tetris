class CodeWriter():
    def __init__(self, filepath):
        self.f = open(filepath, 'w')

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.f.close()

    def write_code(self, code):
        self.f.write(code + '\n')

    def write_codes(self, codes):
        self.write_code('\n'.join(codes))
