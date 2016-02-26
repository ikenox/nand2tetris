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

        if identifier_type in IdentifierKind.STATIC:
            self.static_table[name] = Identifier(identifier_type, kind, self.var_count(kind))
        elif identifier_type in IdentifierKind.FIELD:
            self.field_table[name] = Identifier(identifier_type, kind, self.var_count(kind))
        elif identifier_type in IdentifierKind.ARG:
            self.arg_table[name] = Identifier(identifier_type, kind, self.var_count(kind))
        elif identifier_type in IdentifierKind.VAR:
            self.var_table[name] = Identifier(identifier_type, kind, self.var_count(kind))

    def start_subroutine(self):
        self.static_table = {}
        self.field_table = {}

    def var_count(self, kind):
        if kind in IdentifierKind.STATIC:
            return len(self.static_table)
        elif kind in IdentifierKind.FIELD:
            return len(self.field_table)
        elif kind in IdentifierKind.ARG:
            return len(self.arg_table)
        elif kind in IdentifierKind.VAR:
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
        if self.static_table in name:
            return self.static_table[name]
        elif self.field_table in name:
            return self.field_table[name]
        elif self.arg_table in name:
            return self.arg_table[name]
        elif self.var_table in name:
            return self.var_table[name]
        else:
            return None
