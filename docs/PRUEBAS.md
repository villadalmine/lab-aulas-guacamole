# Evidencia y límites — 3 de noviembre de 2026

Prueba real en Fedora Linux amd64, Docker rootless 28.3.3, Compose 2.39.1 y driver fuse-overlayfs. Runtime dedicado, separado de Podman y Toolbox. Los resultados no acreditan una clase de veinte alumnos ni todos los hosts Linux.

| Comprobación | Resultado y evidencia |
|---|---|
| Arranque mínimo | PostgreSQL healthy, guacd healthy y portal HTTP 200 |
| Autenticación Guacamole | Login API y navegador correctos, versión 1.6.0 |
| SSH por Guacamole | WebSocket, instrucciones gráficas y orden `touch /tmp/guac-ssh-ok` ejecutada; archivo verificado en destino |
| RDP por Guacamole | Login RDP acreditado en guacd, instrucciones gráficas recibidas; XFCE abierto en navegador, terminal y `whoami` devolvió `alumno` |
| Permisos alumno | `alumno-demo` inicia sesión, ve solo las dos conexiones de demo y carece de systemPermissions |
| Persistencia | Archivo en HOME conservado después de recrear y reiniciar escritorio |
| Servicios tras reinicio | D-Bus, SSH, xrdp y sesman RUNNING; reconexión visual a XFCE correcta |
| Grafana 13.2.3 | API health database=ok; login docente en navegador; datasource y dashboard responden 200; panel visual muestra 1 y gráfica de latencia |
| Prometheus y Blackbox | Consulta real `probe_success` del portal devuelve 1 |
| OliveTin 3000.21.0 | Portal 200; dos llamadas StartActionAndWait: estado HTTP 200 y hora UTC, ambas salida 0 |
| Caddy 2.10.2 | Certificado localhost generado por CA interna; curl con CA validada responde 200; login y SSH/RDP por HTTPS pasan |
| HAProxy 3.2-alpine | TCP/SNI hacia Caddy, HTTPS con CA validada responde 200; login y SSH/RDP a través del proxy pasan |
| Captura reproducible | `docs/media/demo.cast`, salidas reales de scripts/grabar-demo.py; GIF derivado de ellas |
| Evidencia visual | `docs/media/escritorio-rdp.png`: terminal real con whoami; no contiene claves |

## Correcciones surgidas de la prueba

- Usar data-root real `/var/home/...` en esta Fedora Atomic: `/home` es un symlink y runc rechazaba la raíz.
- El esquema SQL necesita directorio legible por PostgreSQL: 755 para initdb y 644 para el SQL oficial sin secretos; .env mantiene acceso privado.
- Instalar dbus además de dbus-x11 para disponer de system.conf.
- Retirar PID/sockets efímeros del contenedor al arrancar para que D-Bus/XRDP reinicien correctamente. No se toca HOME.
- El cliente de prueba espera autenticación SSH y confirma sync antes de enviar teclado. Las conexiones temporales se eliminan al terminar normalmente.

## Incus: pendiente, no aprobado

Había capacidad libre, pero crear el proyecto aislado `docente-guia-20261103` quedó bloqueado; existían otras creaciones antiguas bloqueadas. Se detuvieron únicamente los clientes propios, sin reiniciar el daemon ni modificar VMs de clase. Una consulta posterior no mostró el proyecto propio. No se creó VM de prueba. La receta de docs/03-incus.md no se presenta como ejecutada con éxito. No reintentar en bucle ni usar este resultado para certificar Incus.

## Alcance y pendientes

La pila Docker mínima y sus extensiones indicadas arriba están probadas. Quedan fuera: aprovisionamiento automático de VMs o escritorios desde OliveTin, PROXYv2, certificados ACME públicos, prueba de carga multiusuario y reproducción en otro host. El portapapeles/transferencia de archivos y audio no se certifican por estas pruebas.

Se deja la demo Docker activa para la revisión solicitada por Rino, con publicaciones loopback y túnel SSH temporal desde su PC. No es un servicio de producción. Claves efímeras entregadas por chat, nunca en Git. Ver CONTINUIDAD para detener solo estos recursos y conservar datos.
