from rest_framework import status

from hs_core.hydroshare import resource

from .base import HSRESTTestCase


class TestCustomScimetaEndpoint(HSRESTTestCase):
    def setUp(self):
        super(TestCustomScimetaEndpoint, self).setUp()

        self.rtype = 'GenericResource'
        self.title = 'My Test resource'
        res = resource.create_resource(self.rtype,
                                       self.user,
                                       self.title)

        self.pid = res.short_id
        self.resources_to_delete.append(self.pid)

    def test_set_custom_metadata_multiple(self):
        set_metadata = "/hsapi/resource/%s/scimeta/custom/" % self.pid

        response = self.client.post(set_metadata, {
            "foo": "bar",
            "foo2": "bar2"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_custom_metadata_single(self):
        set_metadata = "/hsapi/resource/%s/scimeta/custom/" % self.pid
        response = self.client.post(set_metadata, {
            "foo": "bar"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
