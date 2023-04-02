Desk Phone Utility
==================

This little utility allows to remotely control a snom VoIP desk phone. It was tested
in particular with a snom D717.

The primary application of the utility is using to open ``tel`` URIs from the browser.

The documentation can be found at
`fjung.com/desk_phone_utility <https://fjung.com/desk_phone_utility>`_, the source code at
`github.com/fxjung/desk_phone_utility <https://github.com/fxjung/desk_phone_utility>`_.

Licensed as Free Software under the :download:`MIT License <../../LICENSE>`.

Installation/Setup
------------------

User Install
^^^^^^^^^^^^

.. code-block:: bash

    git clone https://github.com/fxjung/desk_phone_utility.git
    cd desk_phone_utility
    pip install -e .


Developer Install
^^^^^^^^^^^^^^^^^

.. code-block:: bash

    git clone git@github.com:fxjung/desk_phone_utility.git
    cd desk_phone_utility
    pip install -e .[dev,doc]
    pre-commit install
    make -C docs html

After building the docs they are located in ``docs/build/html/index.html``.

Basic Usage
-----------

First, set up the snom http password:

.. code-block:: bash

    desk_phone_utility set-password

Afterwards, you can test it by trying to call a number of your choice, e.g.

.. code-block:: bash

    desk_phone_utility "tel:+49 800 3301000"

Finally, for example in Mozilla Firefox, if you encounter a ``tel:`` link and get the
prompt for the application to open the link with, select ``desk_phone_utility``.
If you don’t know where it is located, just run

.. code-block:: bash

    which desk_phone_utility

to find out.

Configuration
-------------

desk_phone_utility can be configured through a toml config file located at
``~/.config/desk_phone_utility/config.toml``. A file containing example values gets
automatically created during first launch. Alternatively, the example file can be
downloaded :download:`here <../../src/desk_phone_utility/data/example_config.toml>`.

