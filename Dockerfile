# HIO requires python 3.
FROM python:3.6.3

# Set the working directory to /app
WORKDIR /app

# Checkout and install Harmonic PE:
RUN git clone https://github.com/HASTE-project/HarmonicPE.git;cd /app/HarmonicPE;git checkout daemon_features;pip install .

# Make port 80 available (required for the listening daemon)
EXPOSE 80



# Add the example sript (change this to your own:)
ADD example.py /app

# Add lookbusy and install
ADD lookbusy/lookbusy-1.4 /app/lookbusy

WORKDIR /app/lookbusy
RUN ./configure; make; make install

# Add arguments for lookbusy
ARG cpulevel=20
ARG busytime=60

ENV CPU_LEVEL=${cpulevel}
ENV BUSY_TIME=${busytime}

# Run your script on startup, to start the daemon:
WORKDIR /app

CMD ["python", "example.py"]
