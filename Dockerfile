FROM python:3.5-jessie

# For running docker build by CI
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY serve.py /usr/src/app/
COPY showdown.py /usr/src/app/
COPY requirements.txt /usr/src/app/
COPY plugins /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "#!/bin/sh" >> run.sh \
  && echo "python3 serve.py ${PLATFORM}" >> run.sh \
  && chmod +x run.sh

ENTRYPOINT [ "/usr/src/app/run.sh" ]