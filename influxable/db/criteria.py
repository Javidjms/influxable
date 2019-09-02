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
