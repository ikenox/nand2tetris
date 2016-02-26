from const import IdentifierKind


class SymbolTable:
    def __init__(self):
        self.static_table = {}
        self.field_table = {}
        self.arg_table = {}
        self.var_table = {}

    def define(self, name, identifier_type, kind):
        class Identifier:
            def __init__(self, identifier_type, kind, index):
                self.type = identifier_type
                self.kind = kind
                self.index = index

        if kind == IdentifierKind.STATIC:
            self.static_table[name] = Identifier(identifier_type, kind, self.var_count(kind))
        elif kind == IdentifierKind.FIELD:
            self.field_table[name] = Identifier(identifier_type, kind, self.var_count(kind))
        elif kind == IdentifierKind.ARG:
            self.arg_table[name] = Identifier(identifier_type, kind, self.var_count(kind))
        elif kind == IdentifierKind.VAR:
            self.var_table[name] = Identifier(identifier_type, kind, self.var_count(kind))
        else:
            raise Exception('Unknown kind')

    def start_subroutine(self):
        self.arg_table = {}
        self.var_table = {}

    def var_count(self, kind):
        if kind == IdentifierKind.STATIC:
            return len(self.static_table)
        elif kind == IdentifierKind.FIELD:
            return len(self.field_table)
        elif kind == IdentifierKind.ARG:
            return len(self.arg_table)
        elif kind == IdentifierKind.VAR:
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

    def _find_by_name(self, name):
        if name in self.static_table:
            return self.static_table[name]
        elif name in self.field_table:
            return self.field_table[name]
        elif name in self.arg_table:
            return self.arg_table[name]
        elif name in self.var_table:
            return self.var_table[name]
        else:
            return None
