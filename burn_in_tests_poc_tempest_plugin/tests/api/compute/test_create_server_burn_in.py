'''
Created on Jun 17, 2016

@author: castulo, jlwhite
'''
from tempest.api.compute import base
from tempest import test


class CreateServerBurnIn(base.BaseV2ComputeTest):


    @test.attr(type='burn-in')
    def test_create_server_burn_in(self):
        server = self.create_test_server(wait_until='ACTIVE')
        self.assertTrue(server)
