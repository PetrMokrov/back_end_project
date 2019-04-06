FROM python:3.6-alpine
WORKDIR /work
ADD ./ /work
RUN pip install -r /work/requirements.txt
CMD ["python", "-u", "receive.py"]
