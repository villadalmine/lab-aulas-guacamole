# Retomar desde Fedora u otra PC

Repo previsto: `villadalmine/lab-aulas-guacamole`. Copia de trabajo: NAS `Laboratorios/lab-aulas-guacamole`, fuera de Nextcloud. No copiar claves privadas ni datos de alumnos a Git.

1. Clonar GitHub en Linux o abrir la copia del NAS. Preferir checkout local para Docker: bind mounts sobre SMB pueden fallar por permisos/rendimiento.
2. Leer AGENTS.md, README, HITOS.md y PRUEBAS.md.
3. Revisar `git status`; generar `.env` local con preparar.sh.
4. Retomar el primer hito pendiente, registrar resultados y no declarar probadas etapas solo por configuración.

Skill: `skills/lab-aulas/SKILL.md`, consultable o instalable por el agente; no se modifica configuración global automáticamente.

## Recursos propios de prueba

Incus: intento de proyecto `docente-guia-20261103` bloqueado. Se detuvieron solo los dos clientes propios; no se reinició daemon ni se tocaron VMs ajenas. Comprobar si apareció tarde antes de reintentar.

Docker rootless temporal en Fedora: `~/.local/share/lab-aulas-runtime`. Motor/socket propios, independientes del Podman y Toolbox existentes. Estado final y retirada se registran en PRUEBAS.md. No limpiar otros contenedores ni Nextcloud.

Al terminar guardar evidencia y publicar en GitHub sin `.env`. Detener solo recursos propios; volumenes y backups se retiran con decisión explícita. La baja del usuario Windows es una tarea separada.
