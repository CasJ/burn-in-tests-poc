'''
Created on Jun 20, 2016

@author: castulo, jlwhite
'''
from tempest.api.compute import base
from tempest import test


class DeleteServerBurnIn(base.BaseV2ComputeTest):

    @classmethod
    def resource_setup(cls):
        super(DeleteServerBurnIn, cls).resource_setup()
        cls.server = cls.create_test_server(wait_until='ACTIVE')

    @test.attr(type='burn-in')
    def test_delete_server_burn_in(self):
        self.delete_server(self.server['id'])
