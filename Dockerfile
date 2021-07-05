FROM python:3.9

COPY . .

RUN pip install -e .

ENTRYPOINT ["python", "-m", "krpsim"]
CMD [ "python", "-m", "krpsim" ]

