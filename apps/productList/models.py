"""
This file defines the database models
"""
import datetime

from . common import db, Field, auth
from pydal.validators import *

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#

def get_time():
    return datetime.datetime.utcnow()

db.define_table(
    'product',
    Field('product_name'),
    Field('product_quantity', 'integer',
          requires=IS_INT_IN_RANGE(0, None),
          default=0),
    Field('product_cost', 'float',
          requires=IS_FLOAT_IN_RANGE(0, None), default=0.),
    Field('mail_order', 'boolean'),
    Field('creation_date', 'datetime', default=get_time)
)

# We do not want these fields to appear in forms by default.
db.product.id.readable = False
db.product.creation_date.readable = False

db.commit()
