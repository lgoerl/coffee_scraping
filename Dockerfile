FROM python:3.7-slim

ENV DAGSTER_HOME=/opt/dagster/dagster_home/
ENV DAGSTER_APP=/opt/dagster/app
ENV DEST_INSTALL=/opt/dagster/app

RUN mkdir -p ${DAGSTER_HOME} ${DAGSTER_APP} ${DEST_INSTALL}

RUN pip install --upgrade pip && \
    pip install pipenv


# Install custom plugins and custom libraries
COPY Pipfile* ${DEST_INSTALL}/
RUN pipenv install --system --keep-outdated

COPY repo.py workspace.yaml ${DAGSTER_APP}
COPY dagster.yaml %{DAGSTER_HOME}

WORKDIR ${DAGSTER_APP}

EXPOSE 3000

ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]