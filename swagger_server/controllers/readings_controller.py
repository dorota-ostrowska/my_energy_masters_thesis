import connexion
import six

from swagger_server.models.reading_array import ReadingArray  # noqa: E501
from swagger_server import util


def get_readings_by_meter_id(id_meter):  # noqa: E501
    """Returns data to create consumption charts.

    Returns readings by meter ID. # noqa: E501

    :param id_meter: Readings (all table) filtered by meter ID to return.
    :type id_meter: int

    :rtype: ReadingArray
    """
    return 'do some magic!'


def get_readings_from_neighborhood_by_meter_id(id_meter):  # noqa: E501
    """Returns data of consumption in the client&#x27;s area to compare consumptions.

    Returns readings from neighborhood by meter ID (zip code). # noqa: E501

    :param id_meter: Readings (all table) filtered by meter ID to return.
    :type id_meter: int

    :rtype: ReadingArray
    """
    return 'do some magic!'
