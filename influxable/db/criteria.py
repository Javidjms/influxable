from enum import Enum


class WhereOperator(Enum):
    LT = 'lt'
    LTE = 'lte'
    GT = 'gt'
    GTE = 'gte'
    EQ = 'eq'
    NE = 'ne'


EVALUATED_OPERATORS = {
    WhereOperator.LT: '<',
    WhereOperator.LTE: '<=',
    WhereOperator.GT: '>',
    WhereOperator.GTE: '>=',
    WhereOperator.EQ: '=',
    WhereOperator.NE: '!=',
}

INVERTED_OPERATORS = {
    WhereOperator.LT: WhereOperator.GTE,
    WhereOperator.LTE: WhereOperator.GT,
    WhereOperator.GT: WhereOperator.LTE,
    WhereOperator.GTE: WhereOperator.LT,
    WhereOperator.EQ: WhereOperator.NE,
    WhereOperator.NE: WhereOperator.EQ,
}


class Field:
    def __init__(self, field_name):
        self.field_name = field_name

    def __lt__(self, value):
        return Criteria(self, value, WhereOperator.LT)

    def __le__(self, value):
        return Criteria(self, value, WhereOperator.LTE)

    def __eq__(self, value):
        return Criteria(self, value, WhereOperator.EQ)

    def __ne__(self, value):
        return Criteria(self, value, WhereOperator.NE)

    def __ge__(self, value):
        return Criteria(self, value, WhereOperator.GTE)

    def __gt__(self, value):
        return Criteria(self, value, WhereOperator.GT)

    def __str__(self):
        return self.field_name


class Criteria:
    def __init__(self, left_operand, right_operand, operator):
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.operator = operator

    def __invert__(self):
        inverted_operator = INVERTED_OPERATORS[self.operator]
        return Criteria(
            self.left_operand,
            self.right_operand,
            inverted_operator,
        )

    def __or__(self, criteria):
        return DisjunctionCriteria(self, criteria)
