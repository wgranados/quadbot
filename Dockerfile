FROM python:3.5-jessie

ARG PLATFORM
# For running docker build by CI
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/plugins
RUN mkdir -p /usr/src/app/clients/pokemon
RUN mkdir -p /usr/src/app/clients/discord
RUN mkdir -p /usr/src/app/utils
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
COPY setup.py /usr/src/app/
COPY details.yaml /usr/src/app/
COPY __init__.py /usr/src/app/
COPY serve.py /usr/src/app/
COPY plugins/* /usr/src/app/plugins/
COPY utils/* /usr/src/app/utils/
COPY clients/pokemon/* /usr/src/app/clients/pokemon/
COPY clients/discord/* /usr/src/app/clients/discord/
RUN echo "#!/bin/sh" >> run.sh \
  # && echo "while true; do echo \"test\"; sleep 2; done " >> run.sh\
  && echo "python3 -u serve.py ${PLATFORM}" >> run.sh \
  && chmod +x run.sh

ENTRYPOINT [ "/usr/src/app/run.sh" ]