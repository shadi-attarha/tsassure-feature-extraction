.. _quick-start-label:

Quick Start
===========

Install YourPackage
-------------------

To install YourPackage, use pip:

.. code:: shell

   pip install tsassure-feature

If you need additional features, such as integration with Dask, install it with:

.. code:: shell

   pip install tsassure-feature[dask]

See also :ref:`large-data-label`.

Dive in
-------

Before diving deep into the documentation, you can get started with this example:

We use two datasets namely 'mainSet.xlsx' and 'NormalData.xlsx' which are available [1]_ and [2]_. The first column represents the sensor values that we want to extract its meaningful features. 
The dataset contains various sensor readings, and our goal is to extract meanigful features for them. Extracting the meanigful features help to better classify data points and detect abnormal measurments.
Dataset 'NormalData.xlsx' is used to find the other correlated time-series data to the main sensor (first column) and it is part of dataset [1]_ where only normal data is avaible. 

To extract the features for dataset 'mainSet.xlsx', we need to write:

    

The `mainSet` DataFrame has the following structure:

.. code:: python

+-------------+-----------+----------+----------+
| Merge_Humi  | Merge_Temp| Humi_Wea | Temp_Wea | 
+=====+=====+=====+=====+=====+=====+=====+=====+
|    54,25    |   24,275  |   29     |  30,0024 |
+-------------+------------+--------+-----------+
|     58      |  23,9499  |   29	 |  30,0024 |
+-------------+------------+--------+-----------+
| ...  ...    | ...  ...  | ...  ..  | ...  ... |
+-------------+------------+--------+-----------+

The first column is the main column which we intend to extract meaningful features for it.
All columns in this dataframe are different sensors' readings represented in the columns `Merge_Humi`, `Merge_Temp`, `Humi_Wea`, `Temp_Wea`.



To extract features from these time series:

.. code:: python

    from tsassure_feature.feature_extractor import FeatureExtractor
    import pandas as pd
    fe = FeatureExtractor("NormalData.xlsx", "mainSet.xlsx")
    df, correlateddf = fe.extract_features()

You will get a DataFrame `df` with meanigful features. Print to see the df and then you can save it in new excel file:

.. code:: python

    df.head()
    excel_file = 'Output.xlsx'
    # Save the DataFrame to Excel
    df.to_excel(excel_file, index=False)
    


. For a complete example, see the Jupyter notebook
`TsAssure.ipynb <https://colab.research.google.com/drive/1tHabIjiNofVFtG9WGYUxxYbJQ6fKT3gX?usp=drive_link>`_.

References

.. [1] https://github.com/shadi-attarha/tsassure-feature-extraction/blob/main/mainSet.xlsx
.. [2] https://github.com/shadi-attarha/tsassure-feature-extraction/blob/main/NormalData.xlsx

