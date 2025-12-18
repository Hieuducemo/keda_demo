FROM python:3.9

WORKDIR /app
COPY worker.py /app
RUN pip install azure-storage-queue

CMD ["python", "worker.py"]
