# vim:set ft=dockerfile ts=1 sw=1 ai et:
FROM fedora:26

COPY requirements.txt /srv/docker-leash/
RUN dnf makecache \
    && dnf install -y \
        gcc \
        redhat-rpm-config \
        python-devel \
    && dnf clean all \
    && pip install -r /srv/docker-leash/requirements.txt

COPY . /srv/docker-leash

WORKDIR /srv/docker-leash
CMD ["gunicorn", "--workers=5", "--bind=0.0.0.0:80", "--chdir=/srv/docker-leash", "app.leash_server:app"]
