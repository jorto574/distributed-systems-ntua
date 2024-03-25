FROM ubuntu/22.04

# Set the working directory in the container
WORKDIR /usr/src/blockchat

# Command to run when the image is constructed
RUN apt install ...

# Copy files from the directory in this project to the working directory set previously
COPY <files-for-1-server> <directory-for-1-server>

# Set the port in which the application will listen to
EXPOSE 3000

# Command to run when the container starts running, i.e. python start_server.py
CMD []
