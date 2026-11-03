# Retomar desde Fedora u otra PC

Repo previsto: `villadalmine/lab-aulas-guacamole`. Copia de trabajo: NAS `Laboratorios/lab-aulas-guacamole`, fuera de Nextcloud. No copiar claves privadas ni datos de alumnos a Git.

Repositorio publicado: https://github.com/villadalmine/lab-aulas-guacamole

```bash
git clone https://github.com/villadalmine/lab-aulas-guacamole.git
cd lab-aulas-guacamole
cat AGENTS.md docs/HITOS.md docs/PRUEBAS.md
```

Mensaje para el siguiente agente: «Continuar este repositorio siguiendo AGENTS.md y la skill `skills/lab-aulas/SKILL.md`. Leer HITOS, PRUEBAS y CONTINUIDAD. Retomar el primer hito pendiente con evidencia real. Trabajar en NAS/GitHub, sin Nextcloud y sin tocar infraestructura de clases. No publicar secretos ni declarar probado Incus si su creación sigue bloqueada».

1. Clonar GitHub en Linux o abrir la copia del NAS. Preferir checkout local para Docker: bind mounts sobre SMB pueden fallar por permisos/rendimiento.
2. Leer AGENTS.md, README, HITOS.md y PRUEBAS.md.
3. Revisar `git status`; generar `.env` local con preparar.sh.
4. Retomar el primer hito pendiente, registrar resultados y no declarar probadas etapas solo por configuración.

Skill: `skills/lab-aulas/SKILL.md`, consultable o instalable por el agente; no se modifica configuración global automáticamente.

## Recursos propios de prueba

Incus: intento de proyecto `docente-guia-20261103` bloqueado. Se detuvieron solo los dos clientes propios; no se reinició daemon ni se tocaron VMs ajenas. Comprobar si apareció tarde antes de reintentar.

Docker rootless temporal en Fedora: `~/.local/share/lab-aulas-runtime`. Motor/socket propios, independientes del Podman y Toolbox existentes. Estado final y retirada se registran en PRUEBAS.md. No limpiar otros contenedores ni Nextcloud.

En la misma Fedora, para consultar el runtime preparado (si sigue activo):

```bash
export PATH="$HOME/.local/share/lab-aulas-runtime/bin:$PATH"
export DOCKER_HOST=unix:///run/user/$(id -u)/lab-aulas-docker.sock
export DOCKER_CONFIG="$HOME/.local/share/lab-aulas-runtime/docker-config"
cd "$(readlink -f "$HOME")/.local/share/lab-aulas-runtime/work"
systemctl --user status lab-aulas-dockerd-v2 --no-pager
docker compose --profile escritorio ps
```

En Fedora Atomic usar la ruta real `/var/home/...` como `data-root` del motor: en esta prueba `/home/...` era un symlink y runc lo rechazó. El `.env` de prueba se queda local; jamás copiarlo al NAS público ni a GitHub. Un motor detenido no significa que se hayan eliminado imágenes o volúmenes.

Al terminar guardar evidencia y publicar en GitHub sin `.env`. Detener solo recursos propios; volumenes y backups se retiran con decisión explícita. La baja del usuario Windows es una tarea separada.

## Punto de corte de la entrega

La demo queda activa para revisión. El motor temporal no tiene instalación ni autoarranque permanente: tras reiniciar Fedora, comprobar la unidad antes de asumir que sigue disponible. El túnel temporal de Windows termina al cerrar esa PC; desde Fedora se usan directamente los puertos localhost del README.

Para detener únicamente esta demo, con el entorno del runtime anterior seleccionado:

```bash
docker compose -f compose.yaml -f compose.observabilidad.yaml \
  -f compose.olivetin.yaml -f compose.caddy.yaml -f compose.haproxy.yaml \
  --profile escritorio stop
systemctl --user stop lab-aulas-dockerd-v2
```

Esto conserva imágenes, .env y volúmenes para retomar. No ejecutar prune ni borrar directorios de otros motores. El paquete del NAS/GitHub contiene la guía, skill, diagramas y evidencia; las claves y los volúmenes del runtime no se suben.
