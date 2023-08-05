Urban Rivals Collection Management API (urcollectionmanager)
============================================================

A module to support reading player purchase history data and
storing it in a database.

Puchases History Use:
    #) Import `api` from `urcollectionmanager`
    #) Create a request.Session and pass it, along with
       your credentials to `session_connect_to_ur`
    #) Pass that same session (now authenticated) to
       `get_purchase_history` along with the number of
       pages to scrape.
    #) Pass the result to `convert_purchase_history`

        Optionally: Pass result to your own HTML parser.

    #) You now have a list of Purchase objects that contain
       all relevant information available from the purchase
       history page.

Missions Use:
    #) Import `api` from `urcollectionmanager`
    #) Create a request.Session and pass it, along with
       your credentials to `session_connect_to_ur`
    #) Pass that same session (now authenticated) to
       `get_missions_list` along with the mission category
       to find. An empty string returns everything.
    #) Pass the result to `convert_missions`

        Optionally: Pass result to your own HTML parser.

    #) You now have a list of Mission objects that contain
       all relevent information available from the missions
       page.

Database Use:
    #) Run `connect_and_initialize_database` if you have a
       particular database location you want to connect to.
       By default this will connect to `data/collection.sqlite`
    #) Pass a list of Purchase objects to `write_history_to_database`

        If using `convert_purchase_history`, you will need to flatten
        the list of lists

    #) Once the database has Purchase objects in it, you can
       run `get_history_from_database` to retrieve them.

    #) Similarly, you can run `write_missions_to_database` to write
       Mission objects and `get_missions_from_database` to read mission
       Mission objects from the same database as Purchases.

Dev
---
How To Use Tools:
    Poetry_
        - To run the project (preferably configure venv first)

        >>> poetry install

        - To configure your venv

        >>> python -m venv /path/to/new/virtual/environment
        >>> poetry env info

            - If `env info` does not match your path, try manually running \
              `Scripts/activate` inside that environment

        - To add a dependency (add a -D if it's only for development)

        >>> poetry add <dependency>

    Commitizen_
        >>> git add
        >>> cz c

    - More options can be found under options under Commitizen_

    PreCommit_
        Update .pre-commit-config.yaml, then run

    >>> pre-commit install
    >>> pre-commit run --all-files

    - More hook plugins can be found at PreCommitHooks_

TODO:

- Use UR-API_ to collect player data. UR-API-Example_
- Default to file output (excel or some form of that)
- Testing (pytest, Coverage-py_)
- Documentation (Sphinx_)

Not Required at this Time:

- Black_
- iSort_

.. _UR-API: https://www.urban-rivals.com/api/developer/
.. _UR-API-Example: https://github.com/Buscatrufas/UrbanRivals/blob/master/index.php
.. _Coverage-py: https://coverage.readthedocs.io/en/latest/config.html
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _AutoPEP8: https://github.com/hhatto/autopep8#usage
.. _Black: https://github.com/psf/black#version-control-integration
.. _iSort: https://github.com/pre-commit/mirrors-isort
.. _Commitizen: https://woile.github.io/commitizen/
.. _PreCommit: https://pre-commit.com/
.. _PreCommitHooks: https://pre-commit.com/hooks.html
.. _Poetry: https://python-poetry.org/docs/cli/
.. _PypiToken: https://pypi.org/help/#apitoken