# 7. Operación de una clase

PostgreSQL guarda cuentas/conexiones; `home_alumno` guarda entregas. Grafana, Prometheus y Caddy tienen volúmenes propios. Recrear un contenedor no elimina un volumen. `docker compose down` conserva datos; la opción `-v` elimina volúmenes y no es una reparación estándar.

## Backup

```bash
mkdir -p backups
umask 077
docker compose exec -T postgres pg_dump -U guacamole -d guacamole > backups/guacamole.sql
test -s backups/guacamole.sql
```

El dump incluye configuración y credenciales almacenadas: mantener privado y fuera deGit. Conservar `.env` y los HOME según política de retención. Probar restauración en otro proyecto con volúmenes distintos, nunca sobre la base activa para ensayar.

Antes: estimar recursos, preparar cuentas/conexiones y probar como alumno. Durante: observar RAM/CPU/disco/latencia; atender un escritorio sin reiniciar toda la infraestructura. Después: recoger entregas y respaldar antes de resetear o destruir. Avisar qué se conserva.

| Síntoma | Diagnóstico inicial |
|---|---|
| Portal502 | Proxy, red y logsGuacamole |
| Login falla pero portal200 | Esquema/Postgres/env; cuenta del portal no es cuentaSQL |
| RDP negro | LogsXRDP/sesman, Xsession, usuario y redguacd→destino |
| SSH no conecta | IP/puerto/usuario/clave; localhost no es otraVM |
| Corte regular de sesión | WebSocket y timeout proxy/túnel |
| Grafana vacío | Datasource, job y probe_success; esperar un scrape |
| Clave de.env modificada | No cambia contraseñas de bases ya inicializadas |
| Incus creación bloqueada | Operaciones/proyectos y salud del host; no relanzar en bucle ni reiniciar en clase |

Para20alumnos automatizar inventario, cuentas, cuotas y redes después de validar uno. Un contenedor de escritorio no reemplaza una VM para sudo/Docker/kernel/LVM.
