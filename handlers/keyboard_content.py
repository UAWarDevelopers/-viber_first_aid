import json


class KeyBoardContent:
    def __init__(self, options):
        self.message_types = 'keyboard'
        self.buttons = []
        self.__create_buttons(options)

    def __create_buttons(self, btn_options):
        columns = 3
        rows = 2
        for i in range(len(btn_options)):
            btn = Button(columns, rows, btn_options[i])
            self.buttons.append(btn)

    def get_dict_repr(self):
        return {"Type": self.message_types,
                "Buttons": [btn.get_dict_repr() for btn in self.buttons]}


class Button:
    def __init__(self, columns, rows, text):
        self.Columns = columns
        self.Rows = rows
        self.ActionType = "reply"
        self.ActionBody = text
        self.Text = text

    def get_dict_repr(self):
        return self.__dict__
