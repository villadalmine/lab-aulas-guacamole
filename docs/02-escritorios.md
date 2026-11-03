# 2. Escritorios y permisos por alumno

La imagen propia usa Ubuntu, XFCE, XRDP y OpenSSH. No requiere contenedor privilegiado, GPU ni socket Docker. El usuario `alumno` no pertenece a sudo. SSH permite comprobar una conexión real aunque falle la GUI.

En Guacamole crear SSH hacia `escritorio:22` y RDP hacia `escritorio:3389`, usuario `alumno`, clave local `DESKTOP_PASSWORD`. `localhost` dentro de guacd es guacd, no el host ni otra VM.

XRDP de laboratorio usa certificado autofirmado. Si es necesario, ignorar certificado **solo para esa conexión interna controlada**; para producción emitir un certificado confiable. Si NLA no es compatible con este XRDP, probar modo TLS o RDP. Registrar el modo realmente probado en PRUEBAS.md, sin desactivar TLS globalmente.

## Dos alumnos

No escalar la plantilla ciegamente: compartiría `home_alumno`. Copiar el servicio a `escritorio02`, volumen `home_alumno02` y variable `DESKTOP02_PASSWORD` propia. Crear otra conexión a ese nombre y otra cuenta Guacamole con acceso exclusivo. La red `aulas` compartida permite comunicación entre escritorios; para segmentar, usar redes por alumno y reglas de egress o VMs con firewall/VLAN.

## Prueba de clase

1. Crear cuenta `alumno01` sin permisos administrativos y asignarle solo su conexión.
2. Abrir ventana privada y entrar con esa cuenta.
3. En terminal ejecutar `id`, `hostname`, `date`.
4. En escritorio comprobar imagen, teclado, tamaño de pantalla y reconexión.
5. Crear archivo en HOME, reiniciar solo ese escritorio y comprobar persistencia.
6. Comprobar que no ve conexiones de otros alumnos.

Una VM externa funciona igual: usar su IP alcanzable desde guacd y credenciales del sistema operativo. No hace falta que Incus sea el hipervisor para usar Guacamole.
