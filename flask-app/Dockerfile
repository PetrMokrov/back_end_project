FROM python:3.6-alpine
WORKDIR /work
ADD requirements.txt /work
RUN apk update && \
  apk add libpq && \
  apk add --no-cache --virtual .build gcc postgresql-dev musl-dev && \
  pip install -r requirements.txt && \
  apk del .build
ADD rabbit-producer/rabbit-producer.py /work
ADD storage-manager/storage_manager.py /work
CMD ["python", "-u", "rabbit-producer.py"]
