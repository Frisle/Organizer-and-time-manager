import sys

class OutputReader:
    def __init__(self):
        self.stdout = sys.stdout
        self.captured_output = []

    def start_reading(self):
        sys.stdout = self

    def stop_reading(self):
        sys.stdout = self.stdout

    def write(self, text):
        self.captured_output.append(text)
        self.stdout.write(text)

    def flush(self):
        self.stdout.flush()







