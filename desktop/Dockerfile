FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends openssh-server xrdp xorgxrdp xfce4 xfce4-terminal dbus-x11 supervisor curl ca-certificates && rm -rf /var/lib/apt/lists/*  && useradd -m -s /bin/bash alumno && mkdir -p /run/sshd /run/dbus  && printf 'startxfce4\n' > /home/alumno/.xsession && chown alumno:alumno /home/alumno/.xsession  && printf 'allowed_users=anybody\nneeds_root_rights=no\n' > /etc/X11/Xwrapper.config  && adduser xrdp ssl-cert
COPY supervisord.conf /etc/supervisor/conf.d/lab.conf
COPY entrypoint.sh /usr/local/bin/lab-entrypoint
RUN chmod 755 /usr/local/bin/lab-entrypoint
EXPOSE 22 3389
ENTRYPOINT ["/usr/local/bin/lab-entrypoint"]
