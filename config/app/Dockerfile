FROM arnulfosolis/python:latest

MAINTAINER Arnulfo Solis <arnulfojr94@gmail.com>

# Copy project
COPY . /app

# define the python path to our project
ENV PYTHONPATH "/app/src"

# add the bin folder to the PATH
ENV PATH="/app/bin:$PATH"

WORKDIR /app

# install requirements
RUN pip install -r requirements.txt

WORKDIR /app/src

# define default entrypoint
ENTRYPOINT []

# define default script
CMD ["gunicorn", "-c", "/app/config/app/config.py", "init:application"]

