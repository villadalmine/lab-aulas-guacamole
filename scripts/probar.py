#!/usr/bin/env python3
"""Prueba local de login y túneles Guacamole; no imprime claves/tokens."""
import base64
import hashlib
import json
import os
import socket
import ssl
import struct
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

BASE = os.environ.get('LAB_URL', 'http://127.0.0.1:18080/guacamole')
TLS = ssl.create_default_context(cafile=os.environ.get('LAB_CA_FILE'))
env = dict(line.split('=', 1) for line in Path('.env').read_text().splitlines()
           if line and not line.startswith('#') and '=' in line)

def api(path, method='GET', body=None, token=None):
    headers = {}
    if token:
        headers['Guacamole-Token'] = token
    if isinstance(body, dict):
        body = json.dumps(body).encode()
        headers['Content-Type'] = 'application/json'
    elif isinstance(body, str):
        body = body.encode()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20, context=TLS) as response:
        raw = response.read()
        return json.loads(raw) if raw else None

def instruction(op, *args):
    return (','.join(str(len(str(x))) + '.' + str(x) for x in (op, *args)) + ';').encode()

class WS:
    def __init__(self, path):
        url = urllib.parse.urlsplit(BASE)
        if url.scheme not in ('http', 'https'):
            raise RuntimeError('URL debe ser http o https')
        self.s = socket.create_connection((url.hostname, url.port or (443 if url.scheme == 'https' else 80)), timeout=15)
        if url.scheme == 'https':
            self.s = TLS.wrap_socket(self.s, server_hostname=url.hostname)
        self.s.settimeout(10)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (f'GET {url.path}{path} HTTP/1.1\r\nHost: {url.netloc}\r\n'
               f'Upgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n'
               'Sec-WebSocket-Version: 13\r\nSec-WebSocket-Protocol: guacamole\r\n\r\n')
        self.s.sendall(req.encode())
        data = b''
        while b'\r\n\r\n' not in data:
            data += self.s.recv(1)
        expected = base64.b64encode(hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest())
        if b' 101 ' not in data or expected.lower() not in data.lower():
            raise RuntimeError('WebSocket no aceptado')

    def send(self, payload, opcode=1):
        mask = os.urandom(4)
        n = len(payload)
        size = bytes([0x80 | opcode, 0x80 | n]) if n < 126 else bytes([0x80 | opcode, 0x80 | 126]) + struct.pack('!H', n)
        self.s.sendall(size + mask + bytes(x ^ mask[i % 4] for i, x in enumerate(payload)))

    def readn(self, n):
        data = b''
        while len(data) < n:
            block = self.s.recv(n - len(data))
            if not block:
                raise RuntimeError('Túnel cerrado')
            data += block
        return data

    def recv(self):
        a, b = self.readn(2)
        n = b & 127
        if n == 126:
            n = struct.unpack('!H', self.readn(2))[0]
        elif n == 127:
            n = struct.unpack('!Q', self.readn(8))[0]
        mask = self.readn(4) if b & 128 else None
        data = self.readn(n)
        if mask:
            data = bytes(x ^ mask[i % 4] for i, x in enumerate(data))
        if a & 15 == 8:
            raise RuntimeError('Servidor cerró el WebSocket')
        if a & 15 == 9:
            self.send(data, 10)
            return b''
        return data

def main():
    auth = api('/api/tokens', 'POST', urllib.parse.urlencode({'username': 'guacadmin', 'password': 'guacadmin'}))
    token = auth['authToken']
    ds = auth['dataSource']
    results = {'login': True, 'ssh_tunnel': False, 'rdp_tunnel': False}
    run_id = uuid.uuid4().hex[:8]
    for protocol, port in [('ssh', '22'), ('rdp', '3389')]:
        params = {'hostname': 'escritorio', 'port': port, 'username': 'alumno', 'password': env['DESKTOP_PASSWORD']}
        if protocol == 'rdp':
            params.update({'security': 'rdp', 'ignore-cert': 'true', 'enable-wallpaper': 'false'})
        conn = api(f'/api/session/data/{ds}/connections', 'POST',
                   {'parentIdentifier': 'ROOT', 'name': 'Prueba-' + protocol + '-' + run_id, 'protocol': protocol,
                    'parameters': params, 'attributes': {}}, token)
        query = urllib.parse.urlencode({'token': token, 'GUAC_DATA_SOURCE': ds, 'GUAC_ID': conn['identifier'],
                                       'GUAC_TYPE': 'c', 'GUAC_WIDTH': '1024', 'GUAC_HEIGHT': '768', 'GUAC_DPI': '96'})
        ws = WS('/websocket-tunnel?' + query)
        received = b''
        deadline = time.monotonic() + 35
        connected = False
        while time.monotonic() < deadline:
            data = ws.recv()
            received += data
            # El servidor emite sync al entregar un frame; devolverlo evita bloquear el flujo.
            import re
            for stamp in re.findall(rb'4\.sync,\d+\.([0-9]+);', data):
                ws.send(instruction('sync', stamp.decode()))
            if b'5.error,' in received:
                break
            if b'4.size,' in received and (b'3.png,' in received or b'3.img,' in received or b'4.rect,' in received):
                connected = True
                break
        results[protocol + '_tunnel'] = connected
        if connected and protocol == 'ssh':
            # El primer dibujo puede preceder a la autenticación SSH.
            def pump(seconds):
                import re
                until = time.monotonic() + seconds
                ws.s.settimeout(0.5)
                while time.monotonic() < until:
                    try:
                        frame = ws.recv()
                    except socket.timeout:
                        continue
                    for stamp in re.findall(rb'4\.sync,\d+\.([0-9]+);', frame):
                        ws.send(instruction('sync', stamp.decode()))
            pump(4)
            for char in 'touch /tmp/guac-ssh-ok':
                ws.send(instruction('key', ord(char), 1))
                ws.send(instruction('key', ord(char), 0))
            ws.send(instruction('key', 65293, 1))
            ws.send(instruction('key', 65293, 0))
            pump(3)
        ws.send(b'', 8)
        ws.s.close()
        api(f"/api/session/data/{ds}/connections/{conn['identifier']}", 'DELETE', token=token)
    api('/api/tokens/' + urllib.parse.quote(token, safe=''), 'DELETE')
    Path('resultado-prueba.json').write_text(json.dumps(results, indent=2))
    print(json.dumps(results))
    return 0 if all(results.values()) else 1

if __name__ == '__main__':
    raise SystemExit(main())
