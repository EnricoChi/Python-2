from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class GuiClient(Widget):
    def send(self):
        text = self.ids.message_input.text
        self.ids.message_input.clear_widgets()
        self.ids.message_view.insert_text(text+'\n')


class GuiApp(App):
    def build(self):
        return GuiClient()


if __name__ == '__main__':
    GuiApp().run()
