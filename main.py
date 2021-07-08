from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button


class WormApp(App):
    def build(self):
        self.button = Button()
        self.button.pos = (100,100)
        self.button.size = (200,200)
        self.button.text = "Hello, cruel world"

        self.form = Widget()
        self.form.add_widget(self.but)
        return self.form


if __name__ == '__main__':
    WormApp().run()