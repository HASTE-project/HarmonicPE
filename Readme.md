# HarmonicPE (Processing Engine)

Listening daemon, for running inside containers on processing nodes, as part of the [HarmonicIO processing framework](https://github.com/benblamey/HarmonicIO)

Forked from https://github.com/beirbear/HarmonicIO and https://github.com/Hakanwie/HIOContainer

## Example

See `example.py`

To run the code within this version of the HarmonicIO framework, it must be built into a Docker container: 

```
$ docker build -t "hio-example" .
$ docker tag hio-example benblamey/hio-example:latest
$ docker push benblamey/hio-example
```
(change `benblamey`) to your own Dockerhub account.

Then, start the container inside a worker node, as described at https://github.com/benblamey/HarmonicIO - and send a task from a client.
