FROM python:3.8
WORKDIR .

COPY requirements.txt .
RUN pip install --no-cache-dir -U -r  requirements.txt

COPY app/ .
EXPOSE 5000

CMD ["python","main.py"]