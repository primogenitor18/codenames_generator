FROM python:3.12.4-slim

WORKDIR /app
COPY ./ ./
RUN apt update \
  && pip install --upgrade pip \
  && pip install -U pip setuptools \
  && pip install -r requirements.txt \
  && pip cache purge
CMD ["fastapi", "run", "--workers=5"]
