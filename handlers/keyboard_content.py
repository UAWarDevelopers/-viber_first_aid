class KeyBoardContent:
    def __init__(self, options_by_hierarchy):
        self.message_types = 'keyboard'
        self.buttons = []
        self.__create_buttons(options_by_hierarchy)

    def __create_buttons(self, options_by_hierarchy):
        options_by_hierarchy = dict(options_by_hierarchy)

        columns = 3
        rows = 1
        options_num = len(options_by_hierarchy)
        for idx, (key, val) in enumerate(options_by_hierarchy.items()):
            if idx == options_num - 1 and idx % 2 == 0:
                columns = 6
            btn = Button(columns, rows, text=val, action_body=key)
            self.buttons.append(btn)
        self.buttons.append(
            Button(columns=6, rows=1, text="Повернутися до меню", action_body="Старт"))

    def get_dict_repr(self):
        return {"Type": self.message_types,
                "Buttons": [btn.get_dict_repr() for btn in self.buttons]}


class Button:
    def __init__(self, columns, rows, text, action_body):
        self.Columns = columns
        self.Rows = rows
        self.ActionType = "reply"
        self.ActionBody = action_body
        self.Text = text

    def get_dict_repr(self):
        return self.__dict__
