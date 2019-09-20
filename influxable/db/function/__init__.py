def _generate_function(identifier):
    class Function:
        def __init__(self, field='*'):
            self.field = field

        def evaluate(self):
            if hasattr(self.field, 'evaluate'):
                field = self.field.evaluate()
            else:
                field = self.field
            return '{}({})'.format(identifier, field)
    return Function


def _generate_function_with_param(identifier):
    class Function:
        def __init__(self, n, *fields):
            self.n = n
            self.fields = fields

        def evaluate(self):
            fields = ', '.join(self.fields)
            return '{}({}, {})'.format(identifier, fields, self.n)
    return Function
