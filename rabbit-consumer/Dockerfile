FROM python:3.6-alpine
WORKDIR /work
ADD receive.py /work
ADD requirements.txt /work
RUN pip install -r /work/requirements.txt
CMD ["python", "-u", "receive.py"]
