#!/usr/bin/env python3
"""Captura comandos reales en asciicast v2; no graba claves ni .env."""
import json
import subprocess
import time
from pathlib import Path

commands = [
    ['docker', 'compose', '--profile', 'escritorio', 'ps'],
    ['python3', 'scripts/probar.py'],
    ['curl', '--fail', '--silent', 'http://127.0.0.1:13000/api/health'],
    ['curl', '--fail', '--silent', 'http://127.0.0.1:19090/api/v1/query?query=probe_success'],
]
Path('docs/media').mkdir(parents=True, exist_ok=True)
start = time.monotonic()
with Path('docs/media/demo.cast').open('w') as f:
    f.write(json.dumps({'version': 2, 'width': 120, 'height': 30,
        'title': 'Prueba real del laboratorio docente', 'env': {'TERM': 'xterm-256color'}}) + '\n')
    for cmd in commands:
        f.write(json.dumps([round(time.monotonic() - start, 3), 'o', '$ ' + ' '.join(cmd) + '\r\n']) + '\n')
        r = subprocess.run(cmd, capture_output=True, text=True)
        output = (r.stdout + r.stderr).replace('\n', '\r\n')
        f.write(json.dumps([round(time.monotonic() - start, 3), 'o', output + f'\r\nexit={r.returncode}\r\n']) + '\n')
        if r.returncode:
            raise SystemExit(r.returncode)
    f.write(json.dumps([round(time.monotonic() - start, 3), 'o',
        '\r\nAbrir http://localhost:18080/guacamole/\r\nAlumno demo - Escritorio XFCE: conexion RDP desde el navegador.\r\n']) + '\n')
print('Captura real guardada en docs/media/demo.cast')
