======
BODGER
======

The bodger tool is a very simple wrapper that reads a config, matches grainss,
and determines what command to run, and runs it. This makes it easy to set
what commands to run for test, build, docs etc in a CI/CD pipeline. You can
kind of think of it like a platform specific Make command with a better config.

Config
======

The default config is "bodger.conf" and should be located inside of the root of
a project.

This config looks like this::

    bodger:
      test:
        kernel:Linux: pytest
      pkg:
        os:Arch: pop-build -c build.conf --pkg-tgt Arch
        os_family:RedHat: pop-build -c build.conf --pkg-tgt rhel7
      bin:
        kernel:Linux: pop-build -c build.conf

Then the system can by run by calling bodger <cmd>::

    bodger test
    bodger pkg
    bodger bin
