class Flag:
    def __init__(self, name, value, required):
        if not isinstance(name, str):
            raise Exception('name must be string')
        elif not isinstance(value, str) and value != None:
            raise Exception('value must be string')
        elif not isinstance(required, bool):
            raise Exception('required must be bool')
        self.name = name
        self.value = value
        self.required = required

    def __str__(self):
        result = ""
        if self.required:
            result += "*"
        else:
            result += " "
        if self.value == None:
            result += self.name
        else:
            result += self.name + " = " + self.value
        return result
