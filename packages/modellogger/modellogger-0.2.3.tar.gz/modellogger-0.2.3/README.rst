Model-logger
============

Modelloger is a Python library for storing model’s profile and rapid
inter model comparision. Powered by dash and SQLITE3, It’s compact
,light and interactive yet powerfull tool to gain usefull insights.

Documentaion :
~~~~~~~~~~~~~~

Read the detailed documentation `here`_

Installation
------------

Using pip
~~~~~~~~~

Use the package manager `pip`_ to install modelloger.

|PyPi Downloads| |PyPi Monthly Downloads| |PyPi Version|

.. code:: bash

   pip install modellogger

Usage
-----

.. code:: python

   from modellogger import ModelLogger

   #initialise a modelloger instance
   path = "c/path/to/db/databasename.db"
   mlog = ModelLogger(path)
    
   #If you are already using a db created by modelloger you can directly load it by stating it's path
   #if you are creating a new project just give location where you want to store the db followed by a name.db  

-  `Try It Now?`_ |Open In Colab|

Functionalities
---------------

Now you are ready to rock and roll. Out of the box you will have the
following functionalities:

``store_model()``
~~~~~~~~~~~~~~~~~

.. code:: python

    gboost = GradientBoostingClassifier() 
    gboost.fit(X_train,y_train) 
    mlog.store_model('my_model_name',gboost,X_train,1.0) 
    #alternatively
    mlog.store_model('my_model_name',gboost,X_train,get_score(gboost),save_pickle = True)

``view_results()``
~~~~~~~~~~~~~~~~~~

.. code:: python


   mlog.view_results(True,'my_report')

``best_model()``
~~~~~~~~~~~~~~~~~~

.. code:: python


   mlog.best_model(smaller_the_better=True)

``delete_model()``
~~~~~~~~~~~~~~~~~~

.. code:: python


   mlog.delete_model(Model_name = "Mymodel") 
   mlog.delete_model(Model_id = 1)

``model_profiles()``
~~~~~~~~~~~~~~~~~~~~

.. code:: python


   mlog.model_profiles('All')
   mlog.model_profiles(5)

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

License
-------

`apache-2.0`_

.. _here: https://github.com/SohamPathak/modellogger.github.io
.. _pip: https://pip.pypa.io/en/stable/
.. _Try It Now?: cause%20where%20is%20the%20fun%20in%20reading%20documentation%20XD
.. _apache-2.0: https://choosealicense.com/licenses/apache-2.0/

.. |PyPi Downloads| image:: https://pepy.tech/badge/modellogger
   :target: https://pepy.tech/badge/modellogger
.. |PyPi Monthly Downloads| image:: https://pepy.tech/badge/modellogger/month
   :target: https://pepy.tech/badge/modellogger/month
.. |PyPi Version| image:: https://badge.fury.io/py/modellogger.svg
   :target: https://pypi.org/project/modellogger/
.. |Open In Colab| image:: https://camo.githubusercontent.com/52feade06f2fecbf006889a904d221e6a730c194/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667
   :target: https://colab.research.google.com/github/SohamPathak/modellogger.github.io/blob/master/assets/sample/model-logger%20.ipynb