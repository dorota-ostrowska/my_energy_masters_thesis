# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.offer_array import OfferArray  # noqa: E501
from swagger_server.models.offers_for_meter import OffersForMeter  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOfferController(BaseTestCase):
    """OfferController integration test stubs"""

    def test_get_all_offers(self):
        """Test case for get_all_offers

        Returns all available offers.
        """
        response = self.client.open(
            '/api/v3/offer/all',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_offer_by_offers_for_meter_id(self):
        """Test case for get_offer_by_offers_for_meter_id

        Finds offer by IDs.
        """
        response = self.client.open(
            '/api/v3/offer/{id_offersformeter}'.format(id_offersformeter=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_offer(self):
        """Test case for update_offer

        Updates an existing offer adding a new row to a history table.
        """
        response = self.client.open(
            '/api/v3/offer/{id_offersformeter}'.format(id_offersformeter=789),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
