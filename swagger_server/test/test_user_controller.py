# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.client import Client  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_create_new_user(self):
        """Test case for create_new_user

        Creates a user.
        """
        body = Client()
        data = dict(id_client=56,
                    name='name_example',
                    surname='surname_example',
                    pesel='pesel_example',
                    email='email_example',
                    password='password_example')
        response = self.client.open(
            '/api/v3/user',
            method='POST',
            data=json.dumps(body),
            data=data,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_user(self):
        """Test case for delete_user

        Deletes client.
        """
        response = self.client.open(
            '/api/v3/user/{id_client}'.format(id_client='id_client_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_by_client_id(self):
        """Test case for get_user_by_client_id

        Gets client by client ID.
        """
        response = self.client.open(
            '/api/v3/user/{id_client}'.format(id_client='id_client_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_user(self):
        """Test case for login_user

        Logs user into the system.
        """
        query_string = [('username', 'username_example'),
                        ('password', 'password_example')]
        response = self.client.open(
            '/api/v3/user/login',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout_user(self):
        """Test case for logout_user

        Logs out current logged in user session.
        """
        response = self.client.open(
            '/api/v3/user/logout',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_user(self):
        """Test case for update_user

        Updates client.
        """
        body = Client()
        data = dict(id_client=56,
                    name='name_example',
                    surname='surname_example',
                    pesel='pesel_example',
                    email='email_example',
                    password='password_example')
        response = self.client.open(
            '/api/v3/user/{id_client}'.format(id_client='id_client_example'),
            method='PUT',
            data=json.dumps(body),
            data=data,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
