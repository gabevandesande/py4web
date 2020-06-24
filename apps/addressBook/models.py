"""
This file defines the database models
"""
import datetime

from . common import db, Field, auth
from pydal.validators import *

def get_time():
    return datetime.datetime.utcnow()

def get_user_email():
     return auth.current_user.get('email')

db.define_table(
    'contact',
    Field('first_name'),
    Field('last_name'),
    Field('user_email', default=get_user_email)
)

# We do not want these fields to appear in forms by default.
db.contact.id.readable = False
db.contact.user_email.readable = False

db.define_table(
    'phone_number',
    Field('contact_id', 'integer', 'reference contact'),
    Field('phone_number'),
    Field('type')
)

db.phone_number.contact_id.ondelete = 'CASCADE'
db.phone_number.contact_id.readable = False
db.phone_number.id.readable = False

db.commit()
