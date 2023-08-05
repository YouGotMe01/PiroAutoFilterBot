
FROM python:3.8-slim-buster

# Update and upgrade the base image
RUN apt update && apt upgrade -y 

# Install git
RUN apt install git -y

# Copy requirements.txt to the root of the container
COPY requirements.txt /requirements.txt

# Set the working directory
WORKDIR /

# Upgrade pip and install requirements
RUN pip3 install -U pip && pip3 install -U -r requirements.txt

# Set the working directory
WORKDIR /PiroAutoFilterBot

# Copy the current directory to the container
COPY . .

# Expose port 8080
EXPOSE 8080

# Set the command to run the bot.py file
CMD ["python3", "bot.py"]
