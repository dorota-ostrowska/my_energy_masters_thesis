import connexion
import six

from swagger_server.models.meter import Meter  # noqa: E501
from swagger_server import util


def add_points_by_meter_id(id_meter, body=None):  # noqa: E501
    """Adds points to a user account.

    Adds points to a user (user connected with a meter). # noqa: E501

    :param id_meter: The name that needs to be fetched. Use meter1 for testing. 
    :type id_meter: str
    :param body: Update an existent user in the store.
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Meter.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_points_by_meter_id(id_meter, id_meter2=None, ranking_points=None):  # noqa: E501
    """Adds points to a user account.

    Adds points to a user (user connected with a meter). # noqa: E501

    :param id_meter: The name that needs to be fetched. Use meter1 for testing. 
    :type id_meter: str
    :param id_meter2: 
    :type id_meter2: int
    :param ranking_points: 
    :type ranking_points: int

    :rtype: None
    """
    return 'do some magic!'


def get_points_by_meter_id(id_meter):  # noqa: E501
    """Gets points of a user.

    Gets points for a meter (user connected with a meter). # noqa: E501

    :param id_meter: The name that needs to be fetched. Use meter1 for testing. 
    :type id_meter: str

    :rtype: Meter
    """
    return 'do some magic!'
