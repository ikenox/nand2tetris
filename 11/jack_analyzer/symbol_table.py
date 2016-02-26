STATIC = 0
FIELD = 1
ARG = 2
VAR = 3


class Identifier:
    def __init__(self, type, kind, index):
        self.type = type
        self.kind = kind
        self.index = index


class SymbolTable:
    def __init__(self):
        self.static_table = {}
        self.field_table = {}
        self.arg_table = {}
        self.var_table = {}

    def define(self, name, type, kind):
        if type in STATIC:
            self.static_table[name] = Identifier(type, kind, len(self.static_table))
        elif type in FIELD:
            self.field_table[name] = Identifier(type, kind, len(self.field_table))
        elif type in ARG:
            self.arg_table[name] = Identifier(type, kind, len(self.arg_table))
        elif type in VAR:
            self.var_table[name] = Identifier(type, kind, len(self.var_table))

    def var_count(self, kind):
        if type in STATIC:
            return len(self.static_table)
        elif type in FIELD:
            return len(self.field_table)
        elif type in ARG:
            return len(self.arg_table)
        elif type in VAR:
            return len(self.var_table)

    def kind_of(self, name):
        identifier = self._find_by_name(name)
        if identifier:
            return identifier.kind
        else:
            return None

    def type_of(self, name):
        identifier = self._find_by_name(name)
        return identifier.type

    def index_of(self, name):
        identifier = self._find_by_name(name)
        return identifier.index

    def _find_by_name(self,name):
        if self.static_table.has_key(name):
            return self.static_table[name]
        elif self.field_table.has_key(name):
            return self.field_table[name]
        elif self.arg_table.has_key(name):
            return self.arg_table[name]
        elif self.var_table.has_key(name):
            return self.var_table[name]
        else:
            return None
