FROM python:3.6.3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD example.py /app

# Checkout and install Harmonic PE:
RUN git clone https://github.com/benblamey/HarmonicPE.git;cd /app/HarmonicPE;git checkout master;pip install .

# Make port 80 available
EXPOSE 80

CMD ["python", "example.py"]
