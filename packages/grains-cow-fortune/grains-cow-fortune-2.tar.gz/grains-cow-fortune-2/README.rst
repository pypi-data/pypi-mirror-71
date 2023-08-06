=============
GRAINS_COWSAY
=============

** A simple example of a vertically app merged grains project **


INSTALLATION
============



With git::

    git clone https://gitlab.com/saltstack/pop/grains.git
    pip install -e grains

With pip::

    pip install corn_cowsay


EXECUTION
=========
After installation the `grains` command should now be available if it wasn't already


TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r grains/requirements-test.txt
    pytest grains/tests

VERTICAL APP-MERGING
====================
Instructions for extending grains like this project does

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir grains_{project}
    cd grains_{project}


Use `pop-seed` to generate the structure of a project that extends `grains`::

    pop-seed -t v pop_{kernel} -d grains

* "-t v" specifies that this is a vertically app-merged project
*  "-d grains" says that we want to implement the dynamic name of "grains"

Add "grainsv2" to the requirements.txt::

    echo "grainsv2" >> requirements.txt

Note* url based reqs aren't supported on older versions of setuptools
To pip install your vertically app-merged project install grains manually::

    pip install -e git+https://gitlab.com/saltstack/pop/grains.git#egg=grainsv2

And that's it!  Go to town extending grains
Follow the conventions you see in gitlab.com/satlstack/pop/grains
