FROM python:3.9.6-alpine

WORKDIR /booking

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r /booking/requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /booking/entrypoint.sh
RUN chmod +x /booking/entrypoint.sh

COPY . .

ENTRYPOINT ["/booking/entrypoint.sh"]
