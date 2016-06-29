'''
Created on Jun 17, 2016

@author: castulo, jlwhite
'''
import testtools
from unittest.suite import TestSuite

from tempest.api.compute import base
from tempest.common.utils.linux import remote_client
from tempest import config
from tempest import test

from burn_in_tests_poc_tempest_plugin.common import ping

CONF = config.CONF


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(CreateServerBurnIn("test_create_server_burn_in"))
    suite.addTest(CreateServerBurnIn("test_can_ping_created_server"))
    return suite

class CreateServerBurnIn(base.BaseV2ComputeTest):


    @classmethod
    def resource_setup(cls):
        cls.set_validation_resources()
        super(CreateServerBurnIn, cls).resource_setup()
        cls.server = None

    @test.attr(type='burn-in')
    def test_create_server_burn_in(self):
        self.server = self.create_test_server(validatable=True,
                                         wait_until='ACTIVE')
        self.assertTrue(self.server['id'])

    @test.attr(type='burn-in')
    @testtools.skipUnless(CONF.validation.run_validation,
                          'Instance validation tests are disabled.')
    def test_can_ping_created_server(self):
        server = (self.servers_client.show_server(self.servers[0]['id'])
                  ['server'])
        server_ip = self.get_server_ip(server)
        # ping the server until it becomes reachable or times out
        ping.ping_until_reachable(server_ip)
        # Try connecting to the server through SSH
        linux_client = remote_client.RemoteClient(
            server_ip,
            self.image_ssh_user,
            self.image_ssh_password,
            self.validation_resources['keypair']['private_key'],
            server=server,
            servers_client=self.servers_client)
        self.assertTrue(linux_client.validate_authentication())
