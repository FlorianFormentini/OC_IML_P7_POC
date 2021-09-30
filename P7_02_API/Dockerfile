FROM python:3.8.10
ADD . /HeraProject
WORKDIR /HeraProject
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","manage.py", "run"]