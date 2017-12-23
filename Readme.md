# HarmonicPE (Processing Engine)

Listening daemon, for running inside containers on processing nodes, as part of the [HarmonicIO processing framework](https://github.com/benblamey/HarmonicIO)

Forked from https://github.com/beirbear/HarmonicIO

## Example

See `example.py`

## Building and Running the example container:

Building containers for Harmonic IO. Build the container from the HIOContainer folder with: 

```
$ docker build -t "hio-example" .
$ docker tag hio-example benblamey/hio-example:latest
$ docker push benblamey/hio-example:latest
```

Then, start the container inside a worker node, as described at https://github.com/benblamey/HarmonicIO .

