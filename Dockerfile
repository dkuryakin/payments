# It's actually very important to freeze OS version as well as python version.
FROM python:3.7.7-alpine3.11

RUN apk add gcc libc-dev libffi-dev openssl-dev postgresql-dev musl-dev make

COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt && rm requirements.txt

WORKDIR /payments

COPY payments/ /payments/

EXPOSE 80

ENTRYPOINT ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "80"]