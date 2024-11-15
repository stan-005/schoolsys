FROM python:3.11.5-slim

COPY requirements.txt /schoolsys/requirements.txtrec
COPY . /schoolsys
WORKDIR /schoolsys

RUN pip install --upgrade pip
RUN pip install flask

ENTRYPOINT ["python", "run.py"]