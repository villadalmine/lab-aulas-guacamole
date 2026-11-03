#!/bin/sh
set -eu
: "${DESKTOP_PASSWORD:?Falta DESKTOP_PASSWORD}"
printf 'alumno:%s\n' "$DESKTOP_PASSWORD" | chpasswd
mkdir -p /run/sshd /run/dbus
ssh-keygen -A
# El volumen puede estar vacio en el primer arranque.
if [ ! -f /home/alumno/.xsession ]; then
  printf 'startxfce4\n' > /home/alumno/.xsession
  chown alumno:alumno /home/alumno/.xsession
fi
exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
