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
    scope = scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.

    auto_accessors = ['service_hostname', 'service_password',
                      'service_port', 'service_region',
                      'service_tenant_name', 'service_username']

    @hook('{requires:keystone}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')
        if self.auth_data_complete()
            conv.set_state('{relation_name}.available')
        else:
            conv.remove_state('{relation_name}.available')

    @hook('{requires:keystone}-relation-{broken,departed}')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')
        conv.remove_state('{relation_name}.connected')

    def credentials(self):
        """
        Returns a dict of keystone admin credentials
        """
        return {
            'service_hostname': self.service_hostname(),
            'service_port': self.service_port(),
            'service_username': self.service_username(),
            'service_password': self.service_password(),
            'service_tenant_name': self.service_tenant_name()
        }

    def auth_data_complete(self):
        data = self.credentials()
        if all(data.values()):
            return True
        return False
