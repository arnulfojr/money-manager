FROM arnulfosolis/python:latest

MAINTAINER Arnulfo Solis <arnulfojr94@gmail.com>

# Copy project
COPY . /app

# define the python path to our project
ENV PYTHONPATH "/app/src"

# add the bin folder to the PATH
ENV PATH="/app/bin:$PATH"

# define default entrypoint
ENTRYPOINT ["python"]

# define default script
CMD ["init.py"]

