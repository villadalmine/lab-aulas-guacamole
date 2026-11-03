# 0. Preparar el host

Demo orientativa: Linux amd64, 4 CPU, 6–8 GB RAM disponibles y 20 GB de disco. No es una garantía para una clase completa. Dimensionar con una prueba piloto; navegadores/IDE pueden consumir mucho más.

Instalar Git, Python3, Docker Engine y Compose v2 según la distribución. En Ubuntu 24.04 de laboratorio se pueden usar `sudo apt-get update` y `sudo apt-get install docker.io docker-compose-v2 git python3`. Verificar `docker version`, `docker compose version`, `docker info`. Si necesitás sudo, usarlo de manera consistente; el grupo docker da control prácticamente equivalente a root.

Fedora Atomic/Sericea: Toolbox no trae un daemon Docker por ser un contenedor. Usar motor del host, un runtime rootless probado o una VM Linux dedicada. No desactivar SELinux/AppArmor para resolver fallos.

| Servicio | Publicación de demostración |
|---|---|
| Guacamole | 127.0.0.1:18080 |
| Grafana | 127.0.0.1:13000 |
| Prometheus | 127.0.0.1:19090 |
| OliveTin | 127.0.0.1:1337 |
| Caddy | 127.0.0.1:18443 |
| HAProxy | 127.0.0.1:19443 |
| Postgres, guacd, SSH, RDP | Sin publicación al host |

Para un escritorio presupuestar inicialmente 1–2 GB y 1–2 vCPU. Un contenedor comparte el kernel: útil para GUI/terminal sencilla. Para systemd, sudo, kernel, Docker de alumno, LVM o redes, elegir VM. La demo no implementa aislamiento de un campus.
