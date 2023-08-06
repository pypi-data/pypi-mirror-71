************
IDEM-WINDOWS
************
**Grains, execution modules, and state modules common to all windows systems**

INSTALLATION
============


Clone the `idem-windows` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/idem-windows.git
    pip install -e idem-windows

EXECUTION
=========
After installation the `grains` command should now be available

TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r idem_windows\requirements-test.txt
    pytest idem_windows\tests

VERTICAL APP-MERGING
====================
Instructions for extending idem-windows into another POP project:

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir idem_{windows_project_name}
    cd idem_{windows_project_name}


Use `pop-seed` to generate the structure of a project that extends `grains`, `idem`, and `states`::

    pop-seed -t v pop_{specific_windows_system} -d grains exec states

* "-t v" specifies that this is a vertically app-merged project
*  "-d grains exec states" says that we want to implement the dynamic names of "grains", "exec", and "states"

Add "idem-windows" to the requirements.txt::

    echo "idem-windows" >> requirements.txt

And that's it!  Go to town making your own unique grains, execution modules, and state modules.
Your new project automatically has access to everything in `idem_windows` through the `hub`.
Follow the conventions you see in idem_windows.

For information about running idem states and execution modules check out
https://idem.readthedocs.io

To read about the hub and learn about POP read
https://pop.readthedocs.io
