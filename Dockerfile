FROM python:3.5-jessie

# For running docker build by CI
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/plugins
RUN mkdir -p /usr/src/app/showdown
RUN mkdir -p /usr/src/app/utils
WORKDIR /usr/src/app

COPY setup.py /usr/src/app/
COPY details.yaml /usr/src/app/
COPY __init__.py /usr/src/app/
COPY serve.py /usr/src/app/
COPY requirements.txt /usr/src/app/
COPY plugins/* /usr/src/app/plugins/
COPY utils/* /usr/src/app/utils/
COPY showdown/* /usr/src/app/showdown/
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "#!/bin/sh" >> run.sh \
  # && echo "while true; do echo \"test\"; sleep 2; done " >> run.sh\
  && echo "python3 -u serve.py pokemon-showdown" >> run.sh \
  && chmod +x run.sh

ENTRYPOINT [ "/usr/src/app/run.sh" ]