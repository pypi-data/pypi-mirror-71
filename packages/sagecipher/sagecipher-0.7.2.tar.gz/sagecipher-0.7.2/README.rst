sagecipher
==========

| |PyPI|
| |Codecov|
| |Build Status|

**sagecipher** (**s**sh **age**nt **cipher**) provides an AES
cipher, whose key is obtained by signing nonce data via SSH agent. This
is illustrated below.

|Cipher illustration|

This can be used in turn by the ``keyring`` library, and by
``ansible-vault`` to encrypt/decrypt files or secrets via the users'
local or forwarded ssh-agent session.

Contents
--------

-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `Using the keyring backend <#keyring>`__
-  `Using with ansible-vault <#ansible>`__
-  `Using sagecipher directly in Python <#using-in-python>`__
-  `Using the sagecipher CLI tool <#cli>`__

Installation
------------

.. code:: sh

    pip install sagecipher

Usage 
------

Before using, ``ssh-agent`` must be running with at least one ssh-key
available for producing cipher key material:

.. code:: sh

    $ source <(ssh-agent)
    Agent pid 3710

    $ ssh-add
    Enter passphrase for /home/somebody/.ssh/id_rsa:
    Identity added: /home/somebody/.ssh/id_rsa (/home/somebody/.ssh/id_rsa)

Using the keyring backend 
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

    $ sagecipher list-keys  # paramiko does not yet expose key comments, unfortunately..
    [ssh-rsa] e8:19:fe:c5:0a:b4:57:5d:96:27:b3:e3:ec:ba:24:3c
    [ssh-rsa] 38:c5:94:45:ca:01:65:d1:d0:c5:ee:5e:cd:b3:94:39

    $ export PYTHON_KEYRING_BACKEND=sagecipher.keyring.Keyring

    $ keyring set svc user1
    Password for 'user' in 'svc': 
    Please select from the following keys...
    [1] ssh-rsa e8:19:fe:c5:0a:b4:57:5d:96:27:b3:e3:ec:ba:24:3c
    [2] ssh-rsa 38:c5:94:45:ca:01:65:d1:d0:c5:ee:5e:cd:b3:94:39
    Selection (1..2): 1

    $ keyring get svc user1
    password1

    the ssh key can be pre-selected in the
    ``KEYRING_PROPERTY_SSH_KEY_FINGERPRINT`` env var

.. code:: sh

    $ export KEYRING_PROPERTY_SSH_KEY_FINGERPRINT=e8:19:fe:c5:0a:b4:57:5d:96:27:b3:e3:ec:ba:24:3c

    $ keyring get svc user2
    password2

    $ python
    Python 3.6.8 (default, Jan 14 2019, 11:02:34) 
    [GCC 8.0.1 20180414 (experimental) [trunk revision 259383]] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import keyring
    >>> keyring.get_password('svc', 'user1')
    'password1'
    >>> keyring.get_password('svc', 'user2')
    'password2'

Using with ansible-vault 
~~~~~~~~~~~~~~~~~~~~~~~~~

| In this example we create a secret key in the keyring for use with
  ``ansible-vault``.
| This process will work with any keyring backend, but it's assumed we
  are up and
| running with the ``sagecipher`` keyring backend per the previous
  section.

| For more information, see:
| `https://docs.ansible.com/ansible/latest/user\_guide/vault.html <>`__

#. Set up environment variables

Replace the key fingerprint below with your own.

.. code: sh
    export PYTHON_KEYRING_BACKEND=sagecipher.keyring.Keyring
    export KEYRING_PROPERTY_SSH_KEY_FINGERPRINT=e8:19:fe:c5:0a:b4:57:5d:96:27:b3:e3:ec:ba:24:3c
    export ANSIBLE_VAULT_PASSWORD_FILE=~/vault-pass.sh

#. Generate a random key for ansible-vault and store in the keyring

.. code: sh
    keyring set ansible-vault key < <(dd if=/dev/urandom bs=32 count=1 | base64)

#. Create the vault password script to retrieve the vault key

.. code:: sh
    $ cat < ~/vault-pass.sh
    #!/bin/sh
    keyring get ansible-vault key
    EOF

    $ chmod +x vault-pass.sh

#. Test it out with ``ansible-vault``

.. code:: sh
    $ ansible-vault encrypt\_string "secret\_password" --name "secret\_attribute" > secrets.yml
    $ ansible localhost -m debug -a var="secret\_attribute" -e "@secrets.yml"

    localhost \| SUCCESS => {
      "secret\_attribute": "secret\_password"
    }

Using sagecipher directly in Python 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from sagecipher import Cipher
    >>>
    >>> # Encrypts using the first SSH key available from SSH agent...
    >>> enc_text = Cipher.encrypt_string("hello, world")
    >>> text = Cipher.decrypt_string(enc_text)
    >>> text
    "hello, world"

Using the sagecipher CLI tool 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check ``sagecipher --help`` for usage. By default, the 'decrypt'
operation will create a FIFO file, and then start a loop to decrypt out
to the FIFO whenever it is opened.

The FIFO is created with mode 600 by default, and if the permissions are
altered or the parent shell is terminated then the sagecipher background
session will end.

.. code:: sh

    $ sagecipher encrypt - encfile
    Please select from the following keys...
    [1] ssh-rsa e8:19:fe:c5:0a:b4:57:5d:96:27:b3:e3:ec:ba:24:3c
    [2] ssh-rsa 38:c5:94:45:ca:01:65:d1:d0:c5:ee:5e:cd:b3:94:39
    Selection (1..2): 1
    Reading from STDIN...

    secret sauce
    (CTRL-D)

    $ sagecipher decrypt encfile
    secret sauce
    $ mkfifo decfile
    $ sagecipher decrypt encfile decfile &
    [1] 16753
    $ cat decfile  # decfile is just a FIFO
    secret sauce
    $

.. |PyPI| image:: https://img.shields.io/pypi/v/sagecipher.svg
   :target: https://pypi.python.org/pypi/sagecipher
.. |Codecov| image:: https://img.shields.io/codecov/c/github/p-sherratt/sagecipher/master.svg
   :target: https://codecov.io/gh/p-sherratt/sagecipher
.. |Build Status| image:: https://travis-ci.org/p-sherratt/sagecipher.svg?branch=master
   :target: https://travis-ci.org/p-sherratt/sagecipher
.. |Cipher illustration| image:: docs/sagecipher.png

