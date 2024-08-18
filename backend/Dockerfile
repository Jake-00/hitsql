FROM python:3.11.8-slim-bullseye
ENV PYTHONUNBUFFERED 1

RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/
EXPOSE 8000
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \ 
    && pip install --upgrade pip \
    && pip install -r requirements.txt
COPY . /backend/
CMD bash -c "uvicorn main:app --reload --host 0.0.0.0 --port 8000"