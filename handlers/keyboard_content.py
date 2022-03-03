import json


class KeyBoardContent:
    def __init__(self, options):
        self.Type = 'keyboard'
        self.Buttons = []
        self.__create_buttons(options)

    def __create_buttons(self, btn_options):
        columns = 3
        rows = 2
        for i in range(len(btn_options)):
            btn = Button(columns, rows, btn_options[i])
            self.Buttons.append(btn)

    def get_json(self):
        return json.dumps(self, cls=ComplexEncoder)

    def jsonable(self):
        return self.__dict__


class Button:
    def __init__(self, columns, rows, text):
        self.Columns = columns
        self.Rows = rows
        self.ActionType = "reply"
        self.ActionBody = text
        self.Text = text

    def jsonable(self):
        return self.__dict__


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()
        else:
            raise TypeError(
                'Object of type %s with value of %s is not JSON serializable',
                type(obj), repr(obj))
