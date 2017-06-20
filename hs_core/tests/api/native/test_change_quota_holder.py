from unittest import TestCase

from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied

from hs_core.hydroshare import resource
from hs_core.testing import MockIRODSTestCaseMixin
from hs_core import hydroshare
from hs_access_control.models import PrivilegeCodes


class TestChangeQuotaHolder(MockIRODSTestCaseMixin, TestCase):
    def setUp(self):
        super(TestChangeQuotaHolder, self).setUp()

        self.hs_group, _ = Group.objects.get_or_create(name='Hydroshare Author')
        # create a user
        self.user1 = hydroshare.create_account(
            'test_user1@email.com',
            username='owner1',
            first_name='owner1_first_name',
            last_name='owner1_last_name',
            superuser=False,
            groups=[self.hs_group]
        )

        self.user2 = hydroshare.create_account(
            'test_user2@email.com',
            username='owner2',
            first_name='owner2_first_name',
            last_name='owner2_last_name',
            superuser=False,
            groups=[self.hs_group]
        )

    def test_change_quota_holder(self):
        res = resource.create_resource(
            'GenericResource',
            self.user1,
            'My Test Resource'
            )

        self.assertTrue(res.creator == self.user1)
        self.assertTrue(res.get_quota_holder() == self.user1)
        self.assertFalse(res.raccess.public)
        self.assertFalse(res.raccess.discoverable)

        with self.assertRaises(PermissionDenied):
            res.set_quota_holder(self.user1, self.user2)

        # test to make sure one owner can transfer quota holder to another owner
        self.user1.uaccess.share_resource_with_user(res, self.user2, PrivilegeCodes.OWNER)
        res.set_quota_holder(self.user1, self.user2)
        self.assertTrue(res.get_quota_holder() == self.user2)
        self.assertFalse(res.get_quota_holder() == self.user1)

        # test to make sure quota holder cannot be removed from ownership
        with self.assertRaises(PermissionDenied):
            self.user1.uaccess.unshare_resource_with_user(res, self.user2)

        if res:
            res.delete()
