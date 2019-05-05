# Meson build aggregation experiment

An experiment to see how one could build Meson projects with complex
build definitions. Specifically:

 - Building a compiler and using it to build more code (i.e. a GCC
   multistage bootstrap build)

 - A project with native code for multiple platforms. This sample
   project has only two (x86_64 and arm), but it could have
   arbitrarily many.

To test you need to have Java and armhf cross compilers. Setting up:

```
./crossexam.py
```

Then to test the bootstrapping do:

```
cd chainbuild
ninja
ninja clean
ninja
```

Note how each subtarget is built before the next one needs it.

To test Android do:

```
cd fauxbuild
ninja
DESTDIR=/tmp/foo ninja install
```

Note how Java is built only once, but the code is built separately on
each project.
