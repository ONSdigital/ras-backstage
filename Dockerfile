FROM python:3.6
MAINTAINER Joseph Walton <joseph.walton@ons.gov.uk>

WORKDIR /app
COPY . /app
EXPOSE 5002
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["run.py"]
