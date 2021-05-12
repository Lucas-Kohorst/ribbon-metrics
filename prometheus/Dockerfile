FROM python:3.6

ADD . /
RUN pip3 install -r requirements.txt

WORKDIR /

CMD ["python3" , "/deribit_exporter.py"]