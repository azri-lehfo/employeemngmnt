import threading
import logging

logger = logging.getLogger(__name__)


class CurrentUserMiddleware:
    """
    Middleware to load the user accessing the current thread into a local
    memory.
    """
    __users = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request = self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        """
        Store User into current thead when processing a request.
        """
        logger.debug(
            f"Request user is authenticated? {request.user.is_authenticated}"
        )

        if request.user.is_authenticated:
            logger.debug(f"Setting request.user, {request.user}")
            self.__class__.set_user(request.user)

        return request

    def process_response(self, get_response):
        """
        Delete User from current thread when the request is complete.
        """
        self.__class__.clear_user()
        return get_response

    def process_exception(self, request, exception):
        """
        If there is an exception, clear the current User.
        """
        self.__class__.clear_user()

    @classmethod
    def get_user(cls, default=None):
        """
        Retrieve User from the current thread.
        """
        user = cls.__users.get(threading.current_thread(), default)
        return user

    @classmethod
    def set_user(cls, user):
        """
        Store User into the current thread.
        """
        cls.__users[threading.current_thread()] = user

    @classmethod
    def clear_user(cls):
        """
        Clear User from the current thread.
        """
        cls.__users.pop(threading.current_thread(), None)

    @classmethod
    def clear_all_users(cls):
        """
        Clear all Users from the current thread.
        """
        cls.__users = {}


def get_current_user():
    """
    Return the current User from the CurrentUserMiddleware
    """
    return CurrentUserMiddleware.get_user()
