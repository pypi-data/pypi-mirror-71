.. image:: https://badge.fury.io/py/Torrelque.png
   :target: https://pypi.python.org/pypi/Torrelque
   :alt: PyPI
.. image:: https://readthedocs.org/projects/torrelque/badge/?version=latest
   :target: https://torrelque.readthedocs.io/en/latest/?badge=latest
   :alt: RTFD

*********
Torrelque
*********
Torrelque is a Python package that provides an asynchronous reliable Redis-backed
work queues.

.. note::

   Prior to version 0.2 Torrelque was Tornado-specific. Since version 5 Tornado
   runs on ``asyncio`` event loop by default, hence Torrelque is still compatible.

Install
=======
::

   pip install Torrelque

Quickstart
==========
Producer:

.. sourcecode:: python

   redis = aredis.StrictRedis()
   queue = torrelque.Torrelque(redis, queue='email')
   queue.schedule_sweep()

   task_data = {'addr': 'joe@doe.com', 'subj': 'hello', 'body': '...'}
   task_id = await queue.enqueue(task)
   logger.info('Email task enqueued %s', task_id)

Consumer:

.. sourcecode:: python

   redis = aredis.StrictRedis()
   queue = torrelque.Torrelque(redis, queue='email')

   while True:
       task_id, task_data = await queue.dequeue()
       try:
           await some_email_client.send(**task_data)
       except SomeEmailError:
           logger.exception('Sending error, retrying in 30 seconds')
           await queue.requeue(task_id, delay=30)
       else:
           await queue.release(task_id)


Example list
============
- `Producer-consumer <e1_>`_. Infinite producing and consuming loops.
- `Batch processing <e2_>`_. Finite number of tasks, consumers stop with a
  poison pill, bulk enqueue. This example can be used as a synthetic benchmark.
  Because there's no IO-bound workload, it'll be CPU-bound which isn't normal
  mode of operation for an asynchronous application. But it can be used to
  compare between CPython, PyPy and concurrency parameters.
- `Web application background task <e3_>`_. This tornado application allows
  to start a task and push server-sent events (SSE) to UI about its status. UI
  starts a task and waits for it to complete. When a task fails it's requeued
  with exponential back-off.


.. _e1: https://heptapod.host/saajns/torrelque/blob/branch/default/example/producer_consumer.py
.. _e2: https://heptapod.host/saajns/torrelque/blob/branch/default/example/batch_processing.py
.. _e3: https://heptapod.host/saajns/torrelque/blob/branch/default/example/wait_until_complete.py
