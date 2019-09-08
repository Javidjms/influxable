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
