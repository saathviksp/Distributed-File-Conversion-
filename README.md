# Distributed File Conversion System

A distributed file processing system built using Python and Java.

## Architecture

Client → Gateway → Worker Nodes

## Features

- Distributed worker processing
- Round-robin load balancing
- Multiple file format conversion
- Socket-based communication

## Technologies

- Python
- Java
- TCP Socket Programming
- Pillow Image Library

## How to Run

Start workers

python worker.py W1 6001  
python worker.py W2 6002  
python worker.py W3 6003  

Start gateway

javac Gateway.java  
java Gateway  

Run client

python client.py
