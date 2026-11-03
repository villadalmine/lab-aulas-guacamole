# Borrador para LinkedIn

¿Cómo entregar un escritorio de laboratorio a un alumno usando solo el navegador?

Preparé una guía abierta, en español, que empieza con lo mínimo: Docker Compose, Apache Guacamole, PostgreSQL y un escritorio XFCE con SSH/RDP.

Después suma Grafana y Prometheus para observar disponibilidad, OliveTin con acciones docentes de consulta, y dos caminos HTTPS: Caddy directo o HAProxy TCP/SNI delante de Caddy.

Incluye diagramas Mermaid explicados, tutorial de acceso, configuración reproducible, grabación de terminal y evidencia de las pruebas realizadas. También explica cuándo conviene pasar de un escritorio en contenedor a una VM con Incus.

La demo Docker se probó con autenticación y conexiones SSH/RDP reales. La receta de creación Incus está documentada por separado y conserva su pendiente de validación en el host de prueba. El panel OliveTin de esta versión consulta estado; no aprovisiona máquinas.

Repositorio: https://github.com/villadalmine/lab-aulas-guacamole

La idea es empezar con un alumno, entender cada componente y ampliar después, sin confundir una demo con una plataforma completa para un campus.

#Linux #Docker #Guacamole #Educación #Grafana #Incus #OpenSource

---

Borrador: no publicado automáticamente. Antes de compartir, revisar `PRUEBAS.md` y mantener las afirmaciones alineadas con esa evidencia.
