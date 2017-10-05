# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class KeystoneRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:keystone-admin}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')
        if self.auth_data_complete():
            conv.set_state('{relation_name}.available')
        else:
            conv.remove_state('{relation_name}.available')

    @hook('{requires:keystone-admin}-relation-{broken,departed}')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')
        conv.remove_state('{relation_name}.connected')

    def credentials(self):
        """
        Returns a dict of keystone admin credentials

        keystone provides:
            {u'service_password': u'XXXXXXXX',
             u'service_port': u'5000',
             u'private-address': u'10.XX.XX.XXX',
             u'service_hostname': u'10.XX.XX.XXX',
             u'service_username': u'admin',
             u'service_tenant_name': u'Admin',
             u'service_region': u'RegionOne'}
       keystone v3 also provides
            {api_version: "3"
            service_project_domain_name: admin_domain
            service_project_name: admin
            service_protocol: http
            service_region: RegionOne
            service_user_domain_name: admin_domain}
        """
        convs = self.conversations()
        if len(convs) > 0:
            conv = convs[0]
            id_admin_data = {
                'service_hostname': conv.get_remote('service_hostname'),
                'service_port': conv.get_remote('service_port'),
                'service_username': conv.get_remote('service_username'),
                'service_password': conv.get_remote('service_password'),
                'service_tenant_name': conv.get_remote('service_tenant_name'),
                'service_region': conv.get_remote('service_region'),
            }
            if conv.get_remote('api_version', u'2') > u'2':
                id_admin_data['api_version'] = (
                    conv.get_remote('api_version', u'2'))
                id_admin_data['service_user_domain_name'] = (
                    conv.get_remote('service_user_domain_name'))
                id_admin_data['service_project_domain_name'] = (
                    conv.get_remote('service_project_domain_name'))
                id_admin_data['service_project_name'] = (
                    conv.get_remote('service_project_name'))
                id_admin_data['service_protocol'] = (
                    conv.get_remote('service_protocol'))
            return id_admin_data
        else:
            return {}

    def auth_data_complete(self):
        data = self.credentials()
        if all(data.values()):
            return True
        return False
