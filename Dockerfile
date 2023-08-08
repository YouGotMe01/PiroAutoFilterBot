
FROM python:3.8-slim-buster

# Update and upgrade the system packages
RUN apt update && apt upgrade -y

# Install git
RUN apt install -y git

# Copy requirements.txt file to the container
COPY requirements.txt /requirements.txt

# Change the working directory to root
WORKDIR /

# Upgrade pip and install the required packages
RUN pip3 install -U pip && pip3 install -U -r requirements.txt

# Change the working directory to PiroAutoFilterBot
WORKDIR /PiroAutoFilterBot

# Copy the project files to the container
COPY . .

# Expose port 8000
EXPOSE 8000

# Start the bot.py application
CMD ["python3", "bot.py"]
