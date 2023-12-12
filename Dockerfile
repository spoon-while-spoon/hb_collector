FROM python:3.11.5

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY collector.py ./
COPY config.json ./

# Port, den das Programm verwendet (falls zutreffend), freigeben
# EXPOSE 8000

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./collector.py"]


