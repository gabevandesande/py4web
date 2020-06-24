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

import random
import time
import uuid

from py4web import action, request, abort, redirect, URL, Field, HTTP
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from yatl.helpers import A
from . common import db, session, T, cache, auth, signed_url

url_signer = URLSigner(session)

def get_name_from_email(e):
    """Given the email of a user, returns the name."""
    u = db(db.auth_user.email == e).select().first()
    return "" if u is None else u.first_name + " " + u.last_name


# The auth.user below forces login.
@action('index')
@action.uses(auth.user, url_signer, session, db, 'index.html')
def index():
    return dict(
        # This is an example of a signed URL for the callback.
        # See the index.html template for how this is passed to the javascript.
        posts_url = URL('posts', signer=url_signer),
        delete_url = URL('delete_post', signer=url_signer),
        user_email = auth.current_user.get('email'),
        author = auth.current_user.get('first_name') + " " + auth.current_user.get('last_name')
     )


@action('posts', method="GET")
@action.uses(db, auth.user, session, url_signer.verify())
def get_posts():
    result = []
    posts = db(db.post.is_reply == None).select(orderby=~db.post.post_date).as_list()
    for post in posts:
        r = db(db.auth_user.email == post['email']).select().first()
        name = r.first_name + " " + r.last_name if r is not None else "Unknown"
        replies = db(db.post.is_reply == post['id']).select(orderby=~db.post.post_date).as_list()
        result.append(post)
        for reply in replies:
            reply['author'] = name
            result.append(reply)
        post['author'] = name

    posts = result
    # You can use tis shortcut for testing at the very beginning.
    # TODO: complete.
    return dict(posts=posts)


@action('posts',  method="POST")
@action.uses(db, auth.user)  # etc.  Put here what you need.
def save_post():
    # To help with testing.
    # TODO: optional.
    id = request.json.get('id') # Note: id can be none.
    content = request.json.get('content')
    is_reply = request.json.get('is_reply')
    db.post.update_or_insert(
        (db.post.id is not None),
        id=id,
        content=content,
        is_reply=is_reply,
    )
    # TODO: complete.
    # If id is None, this means that this is a new post that needs to be
    # inserted.  If id is not None, then this is an update.
    return dict(content=content, id=id, is_reply=is_reply)


@action('delete_post',  method="POST")
@action.uses(db, auth.user, session, url_signer.verify())
def delete_post():
    db((db.post.email == auth.current_user.get("email")) &
       (db.post.id == request.json.get('id'))).delete()
    return "ok"


@action('delete_all_posts')
@action.uses(db)
def delete_all_posts():
    """This should be removed before you use the app in production!"""
    db(db.post).delete()
    return "ok"
