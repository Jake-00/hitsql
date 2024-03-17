FROM python:3.11.8-slim-bullseye
ENV PYTHONUNBUFFERED 1

RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/
EXPOSE 8000
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /backend/
RUN python manage.py migrate
# CMD python manage.py runcrons 
CMD bash -c "gunicorn -w 2 -b 0.0.0.0:8000 tutorial.wsgi:application"