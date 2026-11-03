# Laboratorio de aulas: Guacamole, Docker e Incus

Guía en español para entregar a cada alumno un escritorio o terminal desde el navegador. Empezá con un alumno y agregá componentes cuando hagan falta.

**Estado de pruebas:** [evidencia real](docs/PRUEBAS.md). Un portal HTTP sano no prueba una sesión remota. No se incluyen contraseñas ni infraestructura privada del autor.

Probado: pila Docker, escritorio XFCE en navegador con teclado, SSH/RDP, permisos de alumno, persistencia, Grafana/Prometheus, las dos acciones de OliveTin y proxies HTTPS. **Incus sigue pendiente**: el host de prueba bloqueó la creación del proyecto aislado; no se certifica esa receta como ejecutada.

**Empezar:** [tutorial de la primera clase, incluido el acceso del alumno](docs/01-tutorial.md).

## Acceso real desde el navegador

Capturas directas del navegador durante una sesión real: login de `alumno-demo`, selección de su máquina, apertura del escritorio XFCE y comandos ejecutados en la terminal. La secuencia se reproduce automáticamente, sin marcos ni textos añadidos sobre las pantallas.

![Login y acceso real a la máquina desde Guacamole](docs/media/acceso-real.gif)

### Grafana en vivo

Captura directa del dashboard: disponibilidad HTTP del portal y latencia observada por Prometheus.

![Dashboard real de Grafana](docs/media/browser-real/06-grafana.jpg)

<details>
<summary>Capturas originales y prueba de terminal (descarga opcional)</summary>

[Login](docs/media/browser-real/01-login.jpg) · [Conexiones del alumno](docs/media/browser-real/03-conexiones.jpg) · [Escritorio](docs/media/browser-real/04-escritorio.jpg) · [Terminal](docs/media/browser-real/05-terminal.jpg).

[Grabación asciinema de las pruebas](docs/media/demo.cast), reproducible con `asciinema play demo.cast`. Para regenerarla: `python3 scripts/grabar-demo.py`, con observabilidad activa. El GIF superior es una secuencia de capturas directas de los pasos, no un vídeo continuo.

</details>

## Certificados y panel docente

El portal mínimo usa HTTP en loopback, accesible por túnel SSH. En la etapa HTTPS, **Caddy genera el certificado de `localhost` con su CA interna** y guarda el material en su volumen. El `443` de los archivos es un puerto interno del contenedor: la demo publica `18443` para Caddy y `19443` para HAProxy, ambos solo en localhost. Con un dominio público y los requisitos de ACME cumplidos, Caddy solicita un certificado público. HAProxy TCP no genera ni termina esos certificados.

OliveTin incluye dos acciones de consulta: **Estado Guacamole HTTP** y **Hora del panel**. No crea VMs, no inicia escritorios y no tiene socket Docker/Incus. Docker no impide integrar un controlador Incus, pero esa automatización requiere autorización, inventario y acciones limitadas; no está implementada en esta demo.

```mermaid
flowchart LR
    A[Alumno: navegador] --> C[Caddy HTTPS opcional]
    C --> G[Guacamole: usuarios y permisos]
    A -. prueba local por túnel SSH .-> G
    G --> P[(PostgreSQL)]
    G --> D[guacd: pasarela]
    D -->|SSH o RDP| E[Escritorio Docker por alumno]
    D -->|SSH o RDP| V[VM en Incus]
    B[Blackbox exporter] -->|sonda HTTP| G
    M[Prometheus] --> B
    F[Grafana] --> M
    O[OliveTin docente] -->|acción fija| G
```

Guacamole autentica y conecta; **no crea VMs**. `guacd` convierte protocolos hacia máquinas existentes. PostgreSQL guarda usuarios, conexiones y permisos. Incus administra cómputo; Grafana observa; OliveTin ofrece operaciones predefinidas.

## Etapas

1. [Preparar el host](docs/00-preparacion.md).
2. Levantar el portal mínimo (abajo).
3. [Escritorios Docker y permisos](docs/02-escritorios.md).
4. [VMs con Incus](docs/03-incus.md).
5. [Grafana y Prometheus](docs/04-observabilidad.md).
6. [OliveTin](docs/05-olivetin.md).
7. [Caddy y HAProxy](docs/06-proxies.md).
8. [Operación de clase y backup](docs/07-operacion.md).

## Portal mínimo

En Linux con Docker Engine, Compose v2, Git y Python3. Comandos Bash, no PowerShell:

```bash
git clone https://github.com/villadalmine/lab-aulas-guacamole.git
cd lab-aulas-guacamole
bash scripts/preparar.sh
docker compose up -d
docker compose ps
docker compose logs --tail=80 guacamole postgres guacd
curl --fail http://127.0.0.1:18080/guacamole/ -o /dev/null
```

Esperá PostgreSQL `healthy` y el arranque de Tomcat. Abrí `http://localhost:18080/guacamole/`. Si Docker está en un servidor remoto, en **tu computadora**:

```bash
ssh -N -L 18080:127.0.0.1:18080 usuario@SERVIDOR
```

Usuario inicial **guacadmin / guacadmin**. Cambiá esa clave antes de publicar, creá un administrador propio y comprobá que la clave inicial ya no funciona. La clave de PostgreSQL no es la del portal.

El script genera claves locales distintas en `.env` y el esquema SQL oficial. PostgreSQL importa el esquema solamente al inicializar un volumen vacío. Cambiar `.env` no cambia claves ya guardadas en una base existente.

## Primer alumno

```bash
docker compose --profile escritorio up -d --build
```

En Guacamole: Configuración → Conexiones → Nueva. Para SSH: nombre `alumno01-ssh`, servidor `escritorio`, puerto `22`, usuario `alumno`, clave `DESKTOP_PASSWORD` de `.env`. Para RDP: mismo servidor/usuario, puerto `3389`; ver [modo de seguridad y prueba gráfica](docs/02-escritorios.md).

Crear cuenta Guacamole de alumno y asignarle solo su conexión. Probar también como alumno, no únicamente como administrador. No publicar 22, 3389, 4822 ni 5432 en Internet.

## Agregar componentes

```bash
docker compose -f compose.yaml -f compose.observabilidad.yaml --profile escritorio up -d --build
# Grafana localhost:13000; usuario docente, clave GRAFANA_PASSWORD.
docker compose -f compose.yaml -f compose.observabilidad.yaml -f compose.olivetin.yaml --profile escritorio up -d --build
# OliveTin localhost:1337; acceso exclusivo del docente por túnel.
docker compose -f compose.yaml -f compose.caddy.yaml --profile escritorio up -d --build
# https://localhost:18443/guacamole/ (CA interna de laboratorio).
docker compose -f compose.yaml -f compose.caddy.yaml -f compose.haproxy.yaml --profile escritorio up -d --build
# https://localhost:19443/guacamole/ (HAProxy TCP → Caddy TLS).
```

Usar el mismo conjunto de `-f` al operar cada instalación. Puertos publicados solo en loopback. Para paneles remotos agregar los respectivos `-L` al túnel SSH. TLS interno no equivale a certificado público: ver [publicación](docs/06-proxies.md).

El código y textos propios se publican bajo MIT; imágenes y programas mantienen sus licencias. Para alumnos no confiables con sudo/root, preferir VMs y segmentación. [Fuentes oficiales](docs/FUENTES.md).
