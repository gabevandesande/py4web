"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import uuid

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from yatl.helpers import A
from . common import db, session, T, cache, auth, signed_url


url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', auth.user, db, session, url_signer)
def view_contacts():
    rows = db(db.contact.user_email==auth.current_user.get('email')).select()
    for row in rows:
        phones=db(db.phone_number.contact_id==row.id).select()
        nicestring=''
        for phone in phones:
            nicestring = nicestring + phone.phone_number + " (" + phone.type + "), "
        row['phone_number'] = nicestring[:-2]
    return dict(rows=rows, url_signer=url_signer)

@action('add_contact', method=['GET', 'POST'])
@action.uses('contact_form.html', session, db)
def add_contact():
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        redirect(URL('index'))
    return dict(form=form)

@action('edit_contact/<contact_id>', method=['GET', 'POST'])
@action.uses('contact_form.html', session, db)
def edit_contact(contact_id=None):
    """Note that in the above declaration, the contact_id argument must match
    the <contact_id> argument of the @action."""
    # We read the contact.
    p = db.contact[contact_id]
    if p is None or p.user_email != auth.current_user.get('email'):
        # Nothing to edit.  This should happen only if you tamper manually with the URL.
        redirect(URL('index'))
    form = Form(db.contact, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        redirect(URL('index'))
    return dict(form=form)

@action('delete_contact/<contact_id>', method=['GET', 'POST'])
@action.uses('contact_form.html', session, db, signed_url.verify())
def delete_contact(contact_id=None):
    p = db.contact[contact_id]
    # Make sure user is authorized to delete
    if p is not None and p.user_email == auth.current_user.get('email'):
        db(db.contact.id == contact_id).delete()
    redirect(URL('index'))

# Phone Numbers Controller

@action('phone_index/<contact_id>')
@action.uses('phone_index.html', auth.user, db, session, url_signer)
def view_numbers(contact_id=None):
    rows = db(db.phone_number.contact_id==contact_id).select()
    first_name = db(db.contact.id==contact_id).select(db.contact.first_name)
    last_name = db(db.contact.id==contact_id).select(db.contact.last_name)
    return dict(rows=rows, contact_id=contact_id, url_signer=url_signer, first_name=first_name, last_name=last_name)

@action('add_phone_number/<contact_id>', method=['GET', 'POST'])
@action.uses('phone_number_form.html', session, db)
def add_phone_number(contact_id=None):
    form = Form([Field('number'), Field('type')], csrf_session=session,
            formstyle=FormStyleBulma)
    if form.accepted:
        db.phone_number.insert(contact_id=contact_id, phone_number=form.vars['number'], type=form.vars['type'])
        # We always want POST requests to be redirected as GETs.
        redirect(URL('index'))
    return dict(form=form)

@action('edit_phone_number/<number_id>', method=['GET', 'POST'])
@action.uses('phone_number_form.html', session, db)
def edit_contact(number_id=None):
    """Note that in the above declaration, the contact_id argument must match
    the <contact_id> argument of the @action."""
    # We read the contact.
    p = db.phone_number[number_id]
    c = db.contact[p.contact_id]
    if p is None or c.user_email != auth.current_user.get('email'):
        # Nothing to edit.  This should happen only if you tamper manually with the URL.
        redirect(URL('index'))
    form = Form(db.phone_number, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        redirect(URL('index'))
    return dict(form=form)

@action('delete_phone_number/<number_id>', method=['GET', 'POST'])
@action.uses('phone_number_form.html', session, db, signed_url.verify())
def delete_contact(number_id=None):
    p = db.phone_number[number_id]
    c = db.contact[p.contact_id]
    # Make sure user is authorized to delete
    if p is not None and c.user_email == auth.current_user.get('email'):
        db(db.phone_number.id == number_id).delete()
    redirect(URL('index'))
