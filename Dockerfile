FROM python:3.8
WORKDIR .

COPY requirements.txt .
RUN pip install --no-cache-dir -U -r  requirements.txt

RUN apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y \
&& apt-get -y install apt-utils gcc libpq-dev libsndfile-dev 

COPY app/ .
EXPOSE 5000

CMD ["python","main.py"]