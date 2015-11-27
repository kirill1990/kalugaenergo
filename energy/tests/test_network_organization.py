# coding: utf8

__author__ = 'Demyanov Kirill'

from django.test import TestCase
from energy.models import NetworkOrganization

class NetworkOrganizationTest(TestCase):
    def test_create_model(self):
        model = NetworkOrganization(title=u'Test')
        self.assertEqual(str(model), model.title)
