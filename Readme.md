# HarmonicPE (Processing Engine)

Listening daemon, for running inside containers on processing nodes, as part of the [HarmonicIO processing framework](https://github.com/benblamey/HarmonicIO)

Forked from https://github.com/beirbear/HarmonicIO and https://github.com/Hakanwie/HIOContainer

**To create your own container, don't fork this repository - make your own copy of the Dockerfile and use this repository as a library, as explained below:**

## Example

See `example.py` for how to import and use this listening daemon module. 

To run your code within this version of the HarmonicIO framework, it must be built and published inside a Docker container.

Create your own Dockerfile in your own repository, using the included one as an example, and publish like this:
```
docker build -t "benblamey/hio-example:latest" . && docker push benblamey/hio-example:latest
```

(Don't fork this repository unless you would like to develop the daemon module itself)

Then, start the container inside a HIO worker node, as described at https://github.com/HASTE-project/HarmonicIO - and send a task from a client.
