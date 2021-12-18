# FROM python:3.7-alpine


# # We copy just the requirements.txt first to leverage Docker cache
# COPY ./requirements.txt /app/requirements.txt

# WORKDIR /app

# RUN pip3 install -r requirements.txt

# RUN apt install libmysqlclient-dev
# RUN pip3 install mysqlclient

# COPY . /app

# ENTRYPOINT [ "python3" ]

# CMD [ "app.py" ]


FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container 
# will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction 
# creates a directory with this name if it doesn’t exist
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install PyMySQL

# Run app.py when the container launches
COPY app.py /app
CMD python app.py