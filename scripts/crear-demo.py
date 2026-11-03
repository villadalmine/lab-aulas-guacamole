#!/usr/bin/env python3
"""Solo para la instalación nueva de demostración con guacadmin inicial."""
import urllib.parse
from probar import api, env

auth = api('/api/tokens', 'POST', urllib.parse.urlencode(
    {'username': 'guacadmin', 'password': 'guacadmin'}))
token, ds = auth['authToken'], auth['dataSource']
root = f'/api/session/data/{ds}'
try:
    existing = api(root + '/connections', token=token)
    identifiers = []
    for protocol, port, title in [('ssh', '22', 'Alumno demo - SSH'),
                                  ('rdp', '3389', 'Alumno demo - Escritorio XFCE')]:
        found = next((v['identifier'] for v in existing.values() if v['name'] == title), None)
        if found is None:
            params = {'hostname': 'escritorio', 'port': port, 'username': 'alumno',
                      'password': env['DESKTOP_PASSWORD']}
            if protocol == 'rdp':
                params.update({'security': 'rdp', 'ignore-cert': 'true'})
            conn = api(root + '/connections', 'POST',
                       {'parentIdentifier': 'ROOT', 'name': title, 'protocol': protocol,
                        'parameters': params, 'attributes': {}}, token)
            found = conn['identifier']
        identifiers.append(found)
    users = api(root + '/users', token=token)
    if 'alumno-demo' not in users:
        api(root + '/users', 'POST', {'username': 'alumno-demo',
            'password': env['DESKTOP_PASSWORD'], 'attributes': {}}, token)
    api(root + '/users/alumno-demo/permissions', 'PATCH',
        [{'op': 'add', 'path': '/connectionPermissions/' + i, 'value': 'READ'} for i in identifiers], token)
    print('Demo preparada: dos conexiones; alumno-demo tiene permiso READ.')
finally:
    api('/api/tokens/' + urllib.parse.quote(token, safe=''), 'DELETE')
