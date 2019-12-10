FROM python:3.7

ENV PORT 5000
EXPOSE $PORT

WORKDIR /app
ADD requirements.txt /app
RUN pip install cython
RUN pip install -r requirements.txt

ADD book-recommendation-service /app/

CMD [ "python", "book-recommendation-controller.py"]
