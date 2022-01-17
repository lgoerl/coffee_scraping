FROM python:3.8-slim

RUN export $(grep -v '^#' .env | xargs)
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
ARG DAGSTER_APP=/opt/dagster/app
ARG DEST_INSTALL=/opt/dagster/app

RUN mkdir -p ${DAGSTER_HOME} ${DAGSTER_APP} ${DEST_INSTALL}
WORKDIR ${DEST_INSTALL}

RUN pip install \
    dagster \
    dagster-graphql \
    dagit \
    dagster-postgres \
    dagster-docker

WORKDIR ${DAGSTER_APP}