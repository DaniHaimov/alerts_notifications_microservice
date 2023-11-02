# Alert and Notification Microservice

## Introduction
This app serves as a system to process and handle alerts and notifications based on predefined rules. It listens for events and triggers corresponding actions.

## Features
* **Event Handling**: Process incoming event data and execute actions based on rules.
* **Rule Management**: Allows the addition of new rules dynamically.
* **Docker Integration**: Designed to run within a Docker container for easy deployment.

## Installation
Before installation, ensure that Docker and Python are installed on your system.
1. Clone the repository or download the application files.
2. [Deploy RabbitMQ](README.md#deploy-rabbitmq) 

## Configuration
Before running the application, configure the environment variables. Create a `.env` file in the root directory and set the following variables:
```text
MESSAGE_BROKER_CONSUMER_HOST=<your_broker_host>
MESSAGE_BROKER_CONSUMER_PORT=<your_broker_port>
MESSAGE_BROKER_CONSUMER_NAME=<your_broker_name>
```

## Running the Application
### Running on your local machine
```bash
python app.py
```
### Running on docker
```bash
docker compose up
```
The service will start listening for messages on the configured message broker.

## Dependencies
* pika
* dotenv

Install dependencies using `pip`:
```bash
pip install -r requirements.txt
```

## Deploy RabbitMQ
### Local Install
```bash
  // Refresh the apt-get repository
  sudo apt-get update
  // Install RabbitMQ
  sudo apt-get install rabbitmq-server
  // Start the RabbitMQ
  sudo systemctl start rabbitmq-server
```
  
### Container Deploy
```bash
docker pull rabbitmq
docker run -d --name rabbitmq_name -p listen_port:5672 -p manage_listen_port:15672 rabbitmq:latest
```