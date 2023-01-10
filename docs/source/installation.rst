Install
=======

Creating the Conda environment
------------------------------

1. Install `Miniconda <https://conda.io/projects/conda/en/latest/user-guide/install/linux.html>`_
2. Activate `conda` in Miniconda first using `conda activate` or `source ~/miniconda3/bin/activate`. 
3. Run the following command:

.. code-block:: bash

    conda env create -f environment.yml
   

4. Make sure that you see "extremedetection" in the output when you ask for a list of all available environments:

.. code-block:: bash

    conda env list


Activating the "extremedetection" environment
---------------------------------------------

Run the following:

.. code-block:: bash

    conda activate extremedetection
