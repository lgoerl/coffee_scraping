FROM python:3.8-slim

RUN export $(grep -v '^#' .env | xargs)
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
ARG DAGSTER_APP=/opt/dagster/app
ARG DEST_INSTALL=/opt/dagster/app

RUN mkdir -p ${DAGSTER_HOME} ${DAGSTER_APP} ${DEST_INSTALL}
WORKDIR ${DEST_INSTALL}

RUN pip install --upgrade pip && \
    pip install pipenv

# Install custom plugins and custom libraries
COPY Pipfile*  setup.py src ${DEST_INSTALL}/

RUN pipenv install --system --keep-outdated
RUN python setup.py install

COPY src/dags/repo.py workspace.yaml ${DAGSTER_APP}
COPY dagster.yaml %{DAGSTER_HOME}

WORKDIR ${DAGSTER_APP}

EXPOSE 3000

ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]