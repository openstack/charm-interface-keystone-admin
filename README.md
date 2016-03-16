# keystone-admin interface

Use this interface to use keystone credentials in your charm layers.

## Purpose

By relating you charm layer (keystone-admin:identity-admin) with
keystone service, keystone's API endpoint as well as username, password
and region name will be shared.

## How to use in your layers

The event handler for `identity-admin.connected` is called when a relation
is established between your charm layer and keystone.

In case there are no unset shared data (ie: service_password), a new event
handler will be set: `identity-admin.available`.

This object provides a method,

credentials()

returing a dict of:

            {u'service_password': u'XXXXXXXX',
             u'service_port': u'5000',
             u'service_hostname': u'10.XX.XX.XXX',
             u'service_username': u'admin',
             u'service_tenant_name': u'Admin',
             u'service_region': u'RegionOne'}


metadata.yaml
```
requires:
  identity-admin:
    interface: keystone-admin
```

layer.yaml,
```
includes: ['layer:basic', 'interface:keystone-admin']
```

charm layer example,
```
@when('identity-admin.available')
def setup_openstack_plugin(kst_data):
    creds = kst_data.credentials()
    if data_changed('identity-admin.config', creds):
        settings = {'keystone_vip': creds['service_hostname'],
                    'keystone_port': creds['service_port'],
                    'username': creds['service_username'],
                    'password': creds['service_password'],
                    'tenant_name': creds['service_tenant_name'],
        }
```

## Example deployment

```
$ juju deploy your-awesome-charm
$ juju deploy keystone --config keystone-creds.yaml
$ juju deploy mysql
$ juju add-relation keystone mysql
$ juju add-relation your-awesome-charm keystone
```

where `keystone-creds.yaml` has the necessary configuration settings for your
awesome charm to connect to keystone.

