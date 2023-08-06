.. highlight:: shell

Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/ljvmiranda921/seagull/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it. Those that are
tagged with "first-timers-only" is suitable for those getting started in open-source software.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Seagull could always use more documentation, whether as part of the
official Seagull docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/ljvmiranda921/seagull/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `seagull` for local development.

1. Fork the `seagull` repo on GitHub.
2. Clone your fork locally::

    git clone git@github.com:your_name_here/seagull.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    cd seagull/
    make venv  # Creates a virtual environment
    make dev  # Installs development requirements

   For windows users, you can do the following::


    cd seagull
    python -m venv venv
    venv\Scripts\activate
    pip install pip-tools
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

4. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox. In addition, ensure that your code is formatted using `black <https://github.com/python/black>`_::

    flake8 seagull tests
    black seagull tests
    pytest-v

   To get flake8, black, and tox, just pip install them into your virtualenv. If you wish,
   you can add pre-commit hooks for both flake8 and black to make all formatting easier.

6. Commit your changes and push your branch to GitHub::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.5, and above. Check
   https://dev.azure.com/ljvmiranda/ljvmiranda/_build/latest?definitionId=3&branchName=master
   and make sure that the tests pass for all supported Python versions.

Contributing examples
---------------------

When contributing notebooks, just ensure the following:

1. **All notebooks have clear outputs.** You can click the `Restart and Clear
   Output` in the toolbar or use a tool like `nbstripout`. Sphinx does the job
   of executing them before deployment.
2. **Each cell has an execution timeout of 3 minutes.** Take note of that when
   setting very long iterations. Please note in the PR if the example really
   reqiures long iterations so the limit can be relaxed properly.
3. **Ensure that the environment can be reproduced easily.** Highly-complex
   configuration might not be accepted. If the notebook only relies on Seagull,
   the better.

