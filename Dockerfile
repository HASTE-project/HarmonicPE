
# HIO requires python 3.
FROM dahlo/cellprofiler:3.1.9-16.04

RUN apt update && apt install -y python3.5 python3-pip
RUN pip3 install Pillow


# Set the working directory to /app
WORKDIR /app

# Checkout and install Harmonic PE:
RUN git clone https://github.com/HASTE-project/HarmonicPE.git && cd /app/HarmonicPE && git checkout cellprofiler-PE && pip3 install -e .

# Make port 80 available (required for the listening daemon)
EXPOSE 80



# Add the example sript (change this to your own:)
ADD example.py /app

# Add arguments for lookbusy
ARG cpulevel=20
ARG busytime=10
ADD dummyload.py /app/dummyload.py

ENV CPU_LEVEL=${cpulevel}
ENV BUSY_TIME=${busytime}

# Run your script on startup, to start the daemon:
WORKDIR /app
ENTRYPOINT []
CMD ["python3.5", "example.py"]
