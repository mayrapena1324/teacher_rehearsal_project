# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y libgtk-3-dev
# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]

