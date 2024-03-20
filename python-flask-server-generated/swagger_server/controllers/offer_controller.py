import connexion
import six

from swagger_server.models.offer_array import OfferArray  # noqa: E501
from swagger_server.models.offers_for_meter import OffersForMeter  # noqa: E501
from swagger_server import util


def get_all_offers():  # noqa: E501
    """Returns all available offers.

    Returns offers. # noqa: E501


    :rtype: OfferArray
    """
    return 'do some magic!'


def get_offer_by_offers_for_meter_id(id_offersformeter):  # noqa: E501
    """Finds offer by IDs.

    Returns a single offer (my offer). # noqa: E501

    :param id_offersformeter: 
    :type id_offersformeter: int

    :rtype: OffersForMeter
    """
    return 'do some magic!'


def update_offer(id_offersformeter):  # noqa: E501
    """Updates an existing offer adding a new row to a history table.

    Update an existing offer by offersformeter ID. Update an existent offer in the account. Add a new row in the OffersForMeter table. # noqa: E501

    :param id_offersformeter: 
    :type id_offersformeter: int

    :rtype: OffersForMeter
    """
    return 'do some magic!'
