import datetime
import uuid

import pytest

from zodchy_notations.query import math


@pytest.fixture(scope='module')
def parser():
    return math.Parser()


@pytest.fixture(scope='module')
def types_map():
    return dict(
        item_id=uuid.UUID,
        amount=int,
        created_at=datetime.datetime,
        birthday=datetime.date,
        price=float,
        annotation=str,
        name=str,
        is_active=bool
    )
