---
name: lab-aulas
description: Mantener y probar este laboratorio educativo Guacamole, escritorios, Incus, Grafana, OliveTin, Caddy y HAProxy.
---
1. Leer AGENTS.md y docs/CONTINUIDAD.md.
2. Identificar etapa y comandos de README; preservar .env y volumenes.
3. Validar Compose; desplegar solo recursos aislados del laboratorio.
4. Probar autenticar en Guacamole y una sesion SSH/RDP real. Registrar por separado login, tunel y escritorio.
5. Probar /api/health de Grafana, probe_success en Prometheus y accion fija de OliveTin.
6. Para TLS probar Caddy directo y HAProxy TCP hacia Caddy, sin inventar PROXY protocol si no esta habilitado en ambos extremos.
7. Actualizar docs/HITOS.md y docs/PRUEBAS.md. No publicar secretos ni direcciones privadas del autor.
