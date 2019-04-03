FROM python:3.6-alpine
WORKDIR /work
ADD requirements.txt /work
RUN apk update && \
  apk add libpq && \
  apk add --no-cache --virtual .build gcc postgresql-dev musl-dev && \
  pip install -r requirements.txt && \
  apk del .build
ADD ./ /work
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
