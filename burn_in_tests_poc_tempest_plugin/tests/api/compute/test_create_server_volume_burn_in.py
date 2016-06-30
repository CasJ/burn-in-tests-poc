'''
Created on Jun 29, 2016

@author: ad_cjmarti2
'''
from unittest.suite import TestSuite

from tempest.api.compute import base
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest import config
from tempest import test


CONF = config.CONF


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(CreateServerVolumeBurnIn
                  ("test_create_server_burn_in"))
    suite.addTest(CreateServerVolumeBurnIn
                  ("test_create_volume_burn_in"))
    suite.addTest(CreateServerVolumeBurnIn
                  ("test_attach_volume_to_server_burn_in"))
    return suite


class CreateServerVolumeBurnIn(base.BaseV2ComputeTest):

    @classmethod
    def resource_setup(cls):
        cls.set_validation_resources()
        super(CreateServerVolumeBurnIn, cls).resource_setup()
        cls.device = CONF.compute.volume_device_name
        cls.volumes = []

    @classmethod
    def resource_cleanup(cls):
        cls._delete_volume()
        super(CreateServerVolumeBurnIn, cls).resource_cleanup()

    @classmethod
    def _delete_volume(cls):
        # Delete the created volume
        if cls.volumes:
            cls.volumes_client.delete_volume(cls.volumes[0]['id'])
            cls.volumes_client.wait_for_resource_deletion(cls.volumes[0]['id'])

    def _detach(self, server_id, volume_id):
        if self.attachment:
            self.servers_client.detach_volume(server_id, volume_id)
            waiters.wait_for_volume_status(self.volumes_client,
                                           volume_id, 'available')

    @test.attr(type='burn-in')
    def test_create_server_burn_in(self):
        server = self.create_test_server(validatable=True,
                                         wait_until='ACTIVE')
        self.assertTrue(server['id'])

    @test.attr(type='burn-in')
    def test_create_volume_burn_in(self):
        name = data_utils.rand_name('volume')
        volume = self.volumes_client.create_volume(
            size=CONF.volume.volume_size, display_name=name)['volume']
        self.volumes.append(volume)
        self.assertEqual(name, volume['display_name'])
        waiters.wait_for_volume_status(self.volumes_client,
                                       volume['id'], 'available')

    @test.attr(type='burn-in')
    def test_attach_volume_to_server_burn_in(self):
        self.attachment = self.servers_client.attach_volume(
            self.servers[0]['id'],
            volumeId=self.volumes[0]['id'],
            device='/dev/%s' % self.device)['volumeAttachment']
        waiters.wait_for_volume_status(self.volumes_client,
                                       self.volumes[0]['id'], 'in-use')
        self.addCleanup(self._detach, self.servers[0]['id'],
                        self.volumes[0]['id'])
