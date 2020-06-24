from py4web import action, URL, request
from yatl.helpers import XML
from py4web.utils.url_signer import URLSigner
from py4web.core import Fixture

class ThumbRater(Fixture):

    THUMBRATER = '<thumbrater url="{url}" callback_url="{callback_url}"></thumbrater>'

    def __init__(self, url, session, signer=None, db=None, auth=None):
        self.url = url + '/get'
        self.callback_url = url + '/set'
        self.signer = signer or URLSigner(session)
        # Creates an action (an entry point for URL calls),
        # mapped to the api method, that can be used to request pages
        # for the table.
        self.__prerequisites__ = [session]
        args = list(filter(None, [session, db, auth, self.signer.verify()]))
        f = action.uses(*args)(self.get_rating)
        action(self.url + "/<id>", method=["GET"])(f)
        f = action.uses(*args)(self.set_rating)
        action(self.callback_url + "/<id>", method=["GET"])(f)

    def __call__(self, id=None):
        """This method returns the element that can be included in the page.
        @param id: id of the file uploaded.  This can be useful if there are
        multiple instances of this form on the page."""
        return XML(ThumbRater.THUMBRATER.format(
            url=URL(self.url, id, signer=self.signer),
            callback_url=URL(self.callback_url, id, signer=self.signer)))
    #
    # def get_thumbs(self, id=None):
    #     """Gets the number of thumbs for a given id. """
    #     # This is a test implementation; it should be over-ridden.
    #     # 0 means no thumbs set.
    #     return dict(rating=0)
    #
    # def set_thumbs(self, id=None):
    #     """Sets the number of thumbs."""
    #     # This is a test implementation that should be over-ridden.
    #     print("Number of thumbs set to:", id, int(request.params.rating))
    #     return "ok"
