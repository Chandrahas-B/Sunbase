FROM python:3.9.17-slim-bullseye


COPY . app/

WORKDIR /app

RUN apt update
RUN apt-get install libgomp1
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install openpyxl

EXPOSE 5000

CMD ["python", "main.py"]