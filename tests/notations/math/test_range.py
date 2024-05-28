import datetime

import pytest
from zodchy import codex, operators


@pytest.mark.parametrize(
    "data,left_class,right_class,left_value,right_value",
    [
        # int values
        ('amount=(1,3)', operators.GT, operators.LT, 1, 3),
        ('amount=[1,3)', operators.GE, operators.LT, 1, 3),
        ('amount=(1,3]', operators.GT, operators.LE, 1, 3),
        ('amount=[1,3]', operators.GE, operators.LE, 1, 3),
        # float values
        ('price=(1.1,3.2)', operators.GT, operators.LT, 1.1, 3.2),
        ('price=[1.1,3.2)', operators.GE, operators.LT, 1.1, 3.2),
        ('price=(1.1,3.2]', operators.GT, operators.LE, 1.1, 3.2),
        ('price=[1.1,3.2]', operators.GE, operators.LE, 1.1, 3.2),
        # date values
        (
            'birthday=(2024-04-04,2024-05-04)',
            operators.GT,
            operators.LT,
            datetime.date(2024, 4, 4),
            datetime.date(2024, 5, 4),
        ),
        (
            'birthday=(2024-04-04,2024-05-04]',
            operators.GT,
            operators.LE,
            datetime.date(2024, 4, 4),
            datetime.date(2024, 5, 4),
        ),
        (
            'birthday=[2024-04-04,2024-05-04)',
            operators.GE,
            operators.LT,
            datetime.date(2024, 4, 4),
            datetime.date(2024, 5, 4),
        ),
        (
            'birthday=[2024-04-04,2024-05-04]',
            operators.GE,
            operators.LE,
            datetime.date(2024, 4, 4),
            datetime.date(2024, 5, 4),
        ),
        # datetime values
        (
            'created_at=(2024-04-04T11:04:02,2024-05-04T11:04:02)',
            operators.GT,
            operators.LT,
            datetime.datetime(2024, 4, 4, 11, 4, 2),
            datetime.datetime(2024, 5, 4, 11, 4, 2),
        ),
        (
            'created_at=(2024-04-04T11:04:02,2024-05-04T11:04:02]',
            operators.GT,
            operators.LE,
            datetime.datetime(2024, 4, 4, 11, 4, 2),
            datetime.datetime(2024, 5, 4, 11, 4, 2),
        ),
        (
            'created_at=[2024-04-04T11:04:02,2024-05-04T11:04:02)',
            operators.GE,
            operators.LT,
            datetime.datetime(2024, 4, 4, 11, 4, 2),
            datetime.datetime(2024, 5, 4, 11, 4, 2),
        ),
        (
            'created_at=[2024-04-04T11:04:02,2024-05-04T11:04:02]',
            operators.GE,
            operators.LE,
            datetime.datetime(2024, 4, 4, 11, 4, 2),
            datetime.datetime(2024, 5, 4, 11, 4, 2),
        ),
    ]
)
def test_closed_interval(
    parser,
    types_map,
    data: str,
    left_class: codex.query.FilterBit,
    right_class: codex.query.FilterBit,
    left_value: int | float | datetime.datetime | datetime.date,
    right_value: int | float | datetime.datetime | datetime.date,
):
    result = next(parser(data, types_map), None)
    range_param = result[1]
    assert isinstance(range_param, operators.RANGE)
    left_instance, right_instance = range_param.value
    assert isinstance(left_instance, left_class)
    assert isinstance(right_instance, right_class)
    assert left_instance.value == left_value
    assert right_instance.value == right_value


@pytest.mark.parametrize(
    "data,left_bound,right_bound",
    [
        # int values
        ('amount=(1,)', operators.GT(1), None),
        ('amount=[1,)', operators.GE(1), None),
        ('amount=(,3)', None, operators.LT(3)),
        ('amount=(,3]', None, operators.LE(3)),
        # float values
        ('price=(1.1,)', operators.GT(1.1), None),
        ('price=[1.1,)', operators.GE(1.1), None),
        ('price=(,3.2)', None, operators.LT(3.2)),
        ('price=(,3.2]', None, operators.LE(3.2)),
        # date values
        (
            'birthday=(2024-04-04,)',
            operators.GT(datetime.date(2024, 4, 4)),
            None,
        ),
        (
            'birthday=[2024-04-04,)',
            operators.GE(datetime.date(2024, 4, 4)),
            None,
        ),
        (
            'birthday=(,2024-04-04)',
            None,
            operators.LT(datetime.date(2024, 4, 4)),
        ),
        (
            'birthday=(,2024-04-04]',
            None,
            operators.LE(datetime.date(2024, 4, 4)),
        ),
        # datetime values
        (
            'created_at=(2024-04-04T11:04:02,)',
            operators.GT(datetime.datetime(2024, 4, 4, 11, 4, 2)),
            None,
        ),
        (
            'created_at=[2024-04-04T11:04:02,)',
            operators.GE(datetime.datetime(2024, 4, 4, 11, 4, 2)),
            None,
        ),
        (
            'created_at=(,2024-05-04T11:04:02)',
            None,
            operators.LT(datetime.datetime(2024, 5, 4, 11, 4, 2)),
        ),
        (
            'created_at=(,2024-05-04T11:04:02]',
            None,
            operators.LE(datetime.datetime(2024, 5, 4, 11, 4, 2)),
        ),
    ]
)
def test_opened_interval(
    parser,
    types_map,
    data: str,
    left_bound: codex.query.FilterBit,
    right_bound: codex.query.FilterBit,
):
    result = next(parser(data, types_map), None)
    range_param = result[1]
    assert isinstance(range_param, operators.RANGE)
    left_instance, right_instance = range_param.value
    assert left_instance == left_bound
    assert right_instance == right_bound
