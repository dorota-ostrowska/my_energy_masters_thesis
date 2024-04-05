# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.reading_array import ReadingArray  # noqa: E501
from swagger_server.test import BaseTestCase


class TestReadingsController(BaseTestCase):
    """ReadingsController integration test stubs"""

    def test_get_readings_by_meter_id(self):
        """Test case for get_readings_by_meter_id

        Returns data to create consumption charts.
        """
        response = self.client.open(
            '/api/v3/readings/{id_meter}'.format(id_meter=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_readings_from_neighborhood_by_meter_id(self):
        """Test case for get_readings_from_neighborhood_by_meter_id

        Returns data of consumption in the client's area to compare consumptions.
        """
        response = self.client.open(
            '/api/v3/readings/neighborhood/{id_meter}'.format(id_meter=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
