***********
GRAINS_VIRT
***********

**Virtualization grains for idem with grains**

INSTALLATION
============

Parts of `grains-virt` are dependant on `hub.exec.cmd.run`
which exists inside of a few kernel specific idem projects.
Install the appropriate **one** for your system to make full use of `grains-virt`:

I.E::

    pip install idem-bsd
    pip install idem-darwin
    pip install idem-linux
    pip install idem-solaris
    pip install idem-windows


DEVELOPMENT INSTALLATION
========================


Clone the `grains-virt` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/corn_virtualization.git grains-virt
    pip install -e grains-virt

EXECUTION
=========
After installation the `grains` command should now be available::

    grains virtual virtual_subtype
