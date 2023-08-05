Microsoft Azure Kusto Library for Python
========================================

Overview
--------

.. code-block:: python

    from azure.kusto.data import KustoClient, KustoConnectionStringBuilder

    cluster = "<insert here your cluster name>"
    client_id = "<insert here your AAD application id>"
    client_secret = "<insert here your AAD application key>"
    authority_id = "<insert here your AAD tenet id>"

    # Callback to get auth code for device authentication
    def cb(code):
        print(f"Your authentication code is {code}")

    kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(cluster)
    client = KustoClient(kcsb, cb)

    db = "Samples"
    query = "StormEvents | take 10"

    response = client.execute(db, query)
    for row in response.primary_results[0]:
        print(row[0], " ", row["EventType"])


This package is a fork of `Azure Kusto Data <https://pypi.org/project/azure-kusto-data/>`_, adapted to enable device authentication in situations where the Kusto Data Client is used on the backend.
There are minor changes from the original package and project, which can be seen in this package's repository.

---------

*Kusto Python Client* Library provides the capability to query Kusto clusters using Python.
It is Python 3.x compatible and supports
all data types through familiar Python DB API interface.

It's possible to use the library, for instance, from `Jupyter Notebooks
<http://jupyter.org/>`_.
which are attached to Spark clusters,
including, but not exclusively, `Azure Databricks
<https://azure.microsoft.com/en-us/services/databricks/>`_. instances.

* `How to install the package <https://github.com/Azure/azure-kusto-python#install>`_.

* `Kusto query sample <https://github.com/Azure/azure-kusto-python/blob/master/azure-kusto-data/tests/sample.py>`_.

* `GitHub Repository <https://github.com/Azure/azure-kusto-python/tree/master/azure-kusto-data>`_.
