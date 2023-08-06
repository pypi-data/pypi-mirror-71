
EvoCov
======

GPlib extension to learn the kernel function.

Setup evocov
------------

- Create and activate virtualenv (for python2) or
  venv (for python3)

.. code-block:: bash

  # for python3
  python3 -m venv .env
  # or for python2
  python2 -m virtualenv .env

  source .env/bin/activate

- Upgrade pip

.. code-block:: bash

  python -m pip install --upgrade pip

- Install EvoCov package

.. code-block:: bash

  python -m pip install evocov


Use EvoCov
----------------------

- Import EvoCov and GPlib to use it in your python script.

.. code-block:: python

  import gplib
  import evocov

- Initialize the GP with None covariance function.

.. code-block:: python

    gp = gplib.GP(
        mean_function=gplib.mea.Fixed(),
        covariance_function=gplib.cov.WhiteNoise()
    )

- Configure the fitting method.

.. code-block:: python

    lml = gplib.me.LML()
    bic = gplib.me.BIC()

    fitting_method = evocov.fit.Random(
        obj_fun=bic.fold_measure,
        max_fun_call=25000,
        nested_fit_method=gplib.fit.MultiStart(
            obj_fun=lml.fold_measure,
            max_fun_call=250,
            nested_fit_method=gplib.fit.LocalSearch(
                obj_fun=lml.fold_measure,
                method="Powell",
                max_fun_call=100
            )
        )
    )


- Fit the kernel and the hyperparameters to the training set.

.. code-block:: python

    validation = gplib.dm.Full()

    log = fitting_method.fit(gp, validation.get_folds(
        train_set
    ))

- There are more examples in examples/ directory. Check them out!

Develop EvoCov
--------------

-  Download the repository using git

.. code-block:: bash

  git clone https://gitlab.com/ibaidev/evocov.git
  cd evocov
  git config user.email 'MAIL'
  git config user.name 'NAME'
  git config credential.helper 'cache --timeout=300'
  git config push.default simple

-  Update API documentation

.. code-block:: bash

  source ./.env/bin/activate
  pip install Sphinx
  cd docs/
  sphinx-apidoc -f -o ./ ../evocov
