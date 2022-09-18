FROM python:3.8-alpine as lambda

WORKDIR /partner-product-importer

COPY . .

RUN apk update
RUN apk add zip

RUN pip install -r lambdas/requirements-build.txt
RUN pip install -r lambdas/requirements.txt

RUN pycodestyle --exclude=.venv,.env --max-line-length 100 .

RUN python -m coverage run -m pytest tests
RUN python -m coverage report

RUN mv common lambdas/common
RUN cd lambdas && pip install -r requirements.txt -t . && zip -r function.zip .

FROM localstack/localstack

COPY --from=lambda /partner-product-importer .