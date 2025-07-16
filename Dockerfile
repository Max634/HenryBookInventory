# Dockerfile
FROM python:3.9-alpine3.13
LABEL maintainer="henrybookstore.com"

ENV PYTHONUNBUFFERED=1

# 1) Copy only requirements first (cache pip install)
COPY requirements.txt /requirements.txt
COPY ./scripts /scripts

# 2) Install PostgreSQL client & C build deps, create venv, install psycopg2 and your deps, then clean up
RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
      build-base postgresql-dev musl-dev linux-headers python3-dev && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install psycopg2-binary && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


# 3) Ensure our venv bin is first in PATH
ENV PATH="/scripts:/py/bin:$PATH"

# 4) Copy application code and set as workdir
WORKDIR /app
COPY app /app

EXPOSE 8000

# 5) Create and switch to a non-root user
USER app

CMD ["run.sh"]