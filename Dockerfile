FROM python:3.12 AS builder
COPY requirements.txt .

RUN pip install --user -r requirements.txt


FROM python:3.12-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY ./app ./app
COPY __main__.py .
ENV PATH=/root/.local:$PATH

CMD ["python","-u","./__main__.py"]