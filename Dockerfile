FROM python:3.7-stretch

COPY . /quantum_circuits

RUN pip install -r quantum_circuits/requirements.txt