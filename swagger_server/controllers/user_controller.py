import connexion
import six

from swagger_server.models.client import Client  # noqa: E501
from swagger_server import util


def create_new_user(body=None):  # noqa: E501
    """Creates a user.

    This can only be done by the logged out user. # noqa: E501

    :param body: Created user object.
    :type body: dict | bytes

    :rtype: Client
    """
    if connexion.request.is_json:
        body = Client.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_new_user(id_client=None, name=None, surname=None, pesel=None, email=None, password=None):  # noqa: E501
    """Creates a user.

    This can only be done by the logged out user. # noqa: E501

    :param id_client: 
    :type id_client: int
    :param name: 
    :type name: str
    :param surname: 
    :type surname: str
    :param pesel: 
    :type pesel: str
    :param email: 
    :type email: str
    :param password: 
    :type password: str

    :rtype: Client
    """
    return 'something!!!'


def delete_user(id_client):  # noqa: E501
    """Deletes client.

    This can only be done by the logged in user. # noqa: E501

    :param id_client: 
    :type id_client: str

    :rtype: None
    """
    return 'do some magic!'


def get_user_by_client_id(id_client):  # noqa: E501
    """Gets client by client ID.

     # noqa: E501

    :param id_client: The name that needs to be fetched. Use user1 for testing. 
    :type id_client: str

    :rtype: Client
    """
    return 'do some magic!'


def login_user(username=None, password=None):  # noqa: E501
    """Logs user into the system.

     # noqa: E501

    :param username: The user name for login.
    :type username: str
    :param password: The password for login in clear text.
    :type password: str

    :rtype: str
    """
    return 'do some magic!'


def logout_user():  # noqa: E501
    """Logs out current logged in user session.

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def update_user(id_client, body=None):  # noqa: E501
    """Updates client.

    This can only be done by the logged in user. # noqa: E501

    :param id_client: 
    :type id_client: str
    :param body: Update an existent user in the store.
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Client.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_user(id_client, id_client2=None, name=None, surname=None, pesel=None, email=None, password=None):  # noqa: E501
    """Updates client.

    This can only be done by the logged in user. # noqa: E501

    :param id_client: 
    :type id_client: str
    :param id_client2: 
    :type id_client2: int
    :param name: 
    :type name: str
    :param surname: 
    :type surname: str
    :param pesel: 
    :type pesel: str
    :param email: 
    :type email: str
    :param password: 
    :type password: str

    :rtype: None
    """
    return 'do some magic!'
