# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.meter import Meter  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRankingController(BaseTestCase):
    """RankingController integration test stubs"""

    def test_add_points_by_meter_id(self):
        """Test case for add_points_by_meter_id

        Adds points to a user account.
        """
        body = Meter()
        data = dict(id_meter=56,
                    ranking_points=56)
        response = self.client.open(
            '/api/v3/ranking/{id_meter}'.format(id_meter='id_meter_example'),
            method='PUT',
            data=json.dumps(body),
            data=data,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_points_by_meter_id(self):
        """Test case for get_points_by_meter_id

        Gets points of a user.
        """
        response = self.client.open(
            '/api/v3/ranking/{id_meter}'.format(id_meter='id_meter_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
