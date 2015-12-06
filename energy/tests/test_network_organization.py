# coding: utf8
from django.test import TestCase
from energy.models import NetworkOrganization

__author__ = 'Demyanov Kirill'


class NetworkOrganizationTest(TestCase):
    def test_create_model(self):
        model = NetworkOrganization(title=u'Test')
        self.assertEqual(str(model), model.title)
