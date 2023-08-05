
FROM python:3.8-slim-buster

# Update and upgrade the base image
# Needed to ensure we have the latest package versions
RUN apt-get update && apt-get upgrade -y 

# Install git
# Required to clone the git repository
RUN apt-get install git -y

# Copy requirements.txt to the root of the container
# Provides the necessary dependencies for the application
COPY requirements.txt /requirements.txt

# Set the working directory
# Changes the working directory to /
WORKDIR /

# Upgrade pip and install requirements
# Upgrades pip to the latest version and installs the packages from requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Set the working directory
# Changes the working directory to /PiroAutoFilterBot
WORKDIR /PiroAutoFilterBot

# Copy the current directory to the container
# Copies the current directory to /PiroAutoFilterBot in the container
COPY . .

# Expose port 8080
# Exposes the container's port 8080 to the outside world
EXPOSE 8080

# Set the command to run the bot.py file
# Executes the bot.py file using python3 as the command
CMD ["python3", "bot.py"]
