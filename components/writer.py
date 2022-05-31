class ConsoleWriter:

    def __init__(self, text):
        self.text = text

    def writer(self):
        print(self.text)


class FileWriter:

    def __init__(self, text, name):
        self.text = text
        self.file_name = name + '_log'

    def writer(self):
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'{self.text}\n')
