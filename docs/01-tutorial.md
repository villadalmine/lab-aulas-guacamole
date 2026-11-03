# Primera clase, paso a paso

## 1. Qué vas a conseguir

Un alumno entra en Guacamole desde su navegador, inicia sesión y abre un escritorio XFCE o una terminal SSH. El alumno no instala un cliente RDP. El docente observa disponibilidad en Grafana y usa dos consultas de OliveTin. Esta demo no crea VMs automáticamente.

## 2. Preparar y arrancar

En un Linux con Docker Engine, Compose v2, Git y Python 3 instalados:

```bash
git clone https://github.com/villadalmine/lab-aulas-guacamole.git
cd lab-aulas-guacamole
bash scripts/preparar.sh
docker compose --profile escritorio up -d --build
docker compose --profile escritorio ps
```

Esperar a que PostgreSQL esté `healthy` y Guacamole termine de arrancar. Si el comando falla, leer `docker compose logs --tail=80`; no borrar volúmenes para volver a intentarlo.

## 3. Crear el alumno de demostración

Solo en esta instalación nueva, con la cuenta inicial todavía vigente:

```bash
python3 scripts/crear-demo.py
```

El script crea `Alumno demo - SSH`, `Alumno demo - Escritorio XFCE` y el usuario `alumno-demo`. Su contraseña es el valor local `DESKTOP_PASSWORD` de `.env`. No mostrar ese archivo en una grabación o clase pública. El script no cambia una contraseña de alumno ya existente.

## 4. Entrar desde el navegador

En la computadora que ejecuta Docker abrir **http://localhost:18080/guacamole/**. Si Docker está en otro servidor, crear primero el túnel SSH del README y abrir la misma URL en tu PC.

1. Entrar como `alumno-demo` con su clave local.
2. Seleccionar **Alumno demo - Escritorio XFCE**. Esperar el escritorio.
3. Abrir la terminal de XFCE y ejecutar `whoami`: debe devolver `alumno`.
4. Crear un archivo en la carpeta personal. Desconectar y volver a conectar; comprobarlo.
5. Volver a la pantalla inicial y abrir **Alumno demo - SSH**. Ejecutar `hostname` y `ls`.

`Ctrl` + `Alt` + `Shift` abre el menú de Guacamole para desconectar y acceder al portapapeles. La cuenta del portal y la cuenta Linux son identidades distintas, aunque el script use la misma clave en esta demo.

Para administrar conexiones entrar como `guacadmin / guacadmin`. Antes de exponer el portal, cambiar esa contraseña y crear cuentas propias con permisos mínimos. La prueba automática usa la cuenta inicial: ejecutarla solo en este laboratorio nuevo, nunca contra un portal de producción.

## 5. Agregar observabilidad y panel docente

```bash
docker compose -f compose.yaml -f compose.observabilidad.yaml \
  -f compose.olivetin.yaml --profile escritorio up -d
```

Grafana: **http://localhost:13000**, usuario `docente`, clave `GRAFANA_PASSWORD` de `.env`. Ir a Dashboards → **Laboratorio de aulas**. El indicador debe valer 1 después de una sonda de Prometheus. Un valor 1 comprueba HTTP, no que todos los escritorios estén bien.

OliveTin: **http://localhost:1337**. Pulsar **Estado Guacamole HTTP**: debe mostrar `HTTP 200`, salida 0. **Hora del panel** muestra UTC. No tiene contraseña en esta demo porque solo escucha en loopback; conservar el acceso docente por SSH/VPN.

Estos botones no crean VMs ni gestionan Docker. No se monta el socket Docker/Incus en OliveTin. Para un panel que prepare clases hace falta un controlador propio con inventario, autorización, cuotas y acciones limitadas. Esa integración no se presenta como implementada aquí.

## 6. Probar HTTPS

Seguir [Caddy y HAProxy](06-proxies.md). **Caddy genera los certificados**; HAProxy funciona en TCP y no los genera ni descifra TLS. La demo usa una CA interna, por lo que un navegador que no confía en ella avisará. Para alumnos remotos con dominio público usar la variante de certificado ACME descrita en esa guía.

## 7. Comprobar y guardar

```bash
python3 scripts/probar.py
# En el host de Docker, verificar la orden que envió el cliente SSH:
docker compose exec -T escritorio test -f /tmp/guac-ssh-ok
```

El script prueba login y túneles SSH/RDP, recibe instrucciones gráficas y envía una orden por SSH. No reemplaza la revisión manual del teclado, portapapeles, persistencia y permisos como alumno.

Para detener, usar `docker compose` con el mismo conjunto de archivos y `stop`. Los datos permanecen. Para retirar contenedores/redes usar `down` con el mismo conjunto; no agregar `-v` sin respaldar y decidir eliminar los datos.
