.. _quickstart:

Quick Start
============
Describe some stuff and make a reference to a
:class:`vxi11.Link <vxi11.vxi11_user.Link>` class.  Some
other comments and reference to another
:class:`vxi11.Client <vxi11.vxi11_user.Client>` class.

****************************************************
Very simple example showing connection and ID? query
****************************************************
This is a simple example for ...
This very simple example creates a connection to a device (assumed to be a scope
of some type in this case) and queries the standard `*IDN?` instruction.

.. code-block:: python

  import vxi11
  
  scope = vxi11.Client('192.168.100.127').open_link()
  print('Scope ID: ', scope.query('*IDN?'))


*************************
Instrument Specialization
*************************
For some instruments, a specialization of the
:class:`vxi11.Link <vxi11.vxi11_user.Link>` class has already been created to
simplify access to the instrument by implementing repetitive commands and
responses for certain functionality.

This example demonstrates specialization by connecting to a Tektronix TDS5000B
oscilliscope.

.. code-block:: python

  import vxi11
  from matplotlib import pyplot as plt

  # the 192.168.100.130 IP address *must* be for an Tektronix TDS5000B
  # oscilliscope.
  scope = vxi11.Client('192.168.100.130').open_link()
  # The getCurve function exists for the TDS5000B Link specialization
  x,y = scope.getCurve()
  plt.plot(x,y)
  plt.show()
