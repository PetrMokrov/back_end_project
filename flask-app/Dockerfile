FROM python:3.6-alpine
WORKDIR /work
ADD rabbit-producer/rabbit-producer.py /work 
ADD requirements.txt /work
ADD ./ /work
RUN pip install -r /work/requirements.txt
CMD ["python", "-u", "launch_app.py"]
