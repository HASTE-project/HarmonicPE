FROM python:3.6.3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD example.py /app

# Checkout and install specific version of Harmonic PE:
RUN git clone https://github.com/benblamey/HarmonicPE.git;cd /app/HarmonicPE;git checkout master;pip install .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launch
CMD ["python", "example.py"]