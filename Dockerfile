FROM python:3.6.4-jessie
COPY . /
RUN pip install -r requirements.txt
CMD [ "python",  "main.py" ]