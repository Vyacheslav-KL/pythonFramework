import html


class Observer:

    def update(self, subject):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for i in self.observers:
            i.update(self)


class SmsNotifier(Observer):

    def update(self, subject):
        print(f'SMS >>> New product: {html.unescape(subject.name)}')


class EmailNotifier(Observer):

    def update(self, subject):
        print(f'Email >>> New product: {html.unescape(subject.name)}')
