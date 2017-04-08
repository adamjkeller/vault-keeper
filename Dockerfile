from python:2.7-alpine

ENV CODE_DIR "/opt/vault-keeper"

RUN mkdir -p ${CODE_DIR}

ADD vault-keeper /${CODE_DIR}/
RUN pip install -r ${CODE_DIR}/requirements.txt

WORKDIR ${CODE_DIR}

ENTRYPOINT ["./vault_keeper.py"]
