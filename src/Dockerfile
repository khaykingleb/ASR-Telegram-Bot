FROM python:3.10

RUN apt-get update \
    && apt-get install -y libsndfile1 ffmpeg \
    && pip install --upgrade pip \
    && pip install Cython \
    && pip install "nemo_toolkit[all]" \
    && pip install poetry

RUN mkdir /src

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --without dev,test,research

COPY /src /src

ENTRYPOINT ["python3", "-m", "uvicorn", "src.__main__:app", "--reload", "--port", "8000"]
