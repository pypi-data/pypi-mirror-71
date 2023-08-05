Spike
=====

Spike is a Telegram client with an Ncurses terminal user interface
capable of handling text messages, currently in state of development.

Use
~~~

Launch the program with the ``spike-telegram`` command. To send a
message, just select and enter the desired chat, type the message and
press enter.

These are the keybindings:

=========== =======================
Key         Action
=========== =======================
Arrow up    Switch to upper chat
Arrow down  Switch to lower chat
Arrow right Enter the selected chat
Arrow left  Leave current chat
Page up     Scroll up the dialog
Page down   Scroll down the dialog
Enter       Send message
Ctrl+q      Quit program
=========== =======================

NOTE: if you experience any problems closing the program with Ctrl+q,
executing ``stty -ixon`` before Spike might solve it.

Configuration
~~~~~~~~~~~~~

A configuration file will be created in ``~your_user/.config/spikerc``.
There you can set your Telegram credentials and other options such us
desktop notifications or privacy settings.

Installation
~~~~~~~~~~~~

First of all, you must get an ``api_id`` and ``api_hash`` in
https://my.telegram.org/. Go to ‘API development tools’ and fill out the
form. Once you install Spike, write those keys in the configuration
file, plus your phone number.

Arch Linux installation
^^^^^^^^^^^^^^^^^^^^^^^

-  Clone this repository
-  Go to ``distro-packages/archlinux/python-telegram``. There you will
   find the PKGBUILD to install ``python-telegram``, the main Spike
   dependency
-  Install it with ``makepkg -csi --asdeps``
-  Go to ``../spike-telegram``
-  Install Spike with ``makepkg -csi`` NOTE: This package has
   ``libnotify`` and ``python-emoji`` (AUR) as dependencies. If you wish
   to disable notifications or emoji support in the Spike configuration
   file, you can remove the dependencies from the PKGBUILD before
   installing it
-  Run Spike to generate a template of the configuration file and fill
   it with your Telegram credentials and preferences

Gentoo Linux installation
^^^^^^^^^^^^^^^^^^^^^^^^^

-  Clone this repository
-  Go to ``distro-packages/gentoo``
-  Copy the ``dev-python`` and ``net-im`` folders to your local
   repository (You can find how to create one in
   https://wiki.gentoo.org/wiki/Handbook:AMD64/Portage/CustomTree#Defining_a_custom_repository
   )
-  Run ``emerge -pv spike-telegram`` and add the relevant keywords and
   use flags to your Portage configuration
-  Install Spike with ``emerge -av spike-telegram``
-  Run Spike to generate a template of the configuration file and fill
   it with your Telegram credentials and preferences

Other distributions
^^^^^^^^^^^^^^^^^^^

-  Install ``pip``, the Python Package Manager
-  Install Spike with ``pip install spike-telegram``
-  Run Spike to generate a template of the configuration file and fill
   it with your Telegram credentials and preferences
