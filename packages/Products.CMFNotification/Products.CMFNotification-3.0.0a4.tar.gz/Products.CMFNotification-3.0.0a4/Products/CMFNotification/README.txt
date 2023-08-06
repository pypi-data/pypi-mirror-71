.. -*- coding: utf-8 -*-

===============
CMFNotification
===============

CMFNotification is a Plone product that allows users to be notified
when various events occur in the portal:

- when an item is created or copy-pasted;

- when an item is modified;

- when a workflow transition occurs.

Other notifications might be implemented but, for now, only the three
above can be safely used. (In other words, do not trust the
configuration form, which includes for example fields for discussion
notification, although it is **not** implemented.)

CMFNotification is configured with rules:

- rules to decide who should be notified;

- rules to decide what mail template to use.

Besides these rules, CMFNotification handles extra subscription to any
portal item. This allows authenticated users to subscribe to an item
and receive notification, if the notification policy does not already
include him/her in the list of notified users. These extra
subscription may be recursive: if so, an user which has subscribed to
a folder is notified for any event which occurs on the folder and any
of its items (including its subfolders, etc.).

CMFNotification also contains a menu to allow admins to unsubscribe
users from any content in the site. This menu accessible in "site setup"
and gives a list of the users in alphabetical order, with the path to
each object they are subscribed to.


Dependencies
============

This version of CMFNotification runs on Plone 3.3 and Plone 4. It
should also run on Plone 3.0 to 3.3 (automated tests are not run on
those versions). However, it does not run on Plone 1.x and 2.x.

Despite the name, this product may not work in a pure CMF
portal. Minor changes may be needed. I thought about having an
implementation which works for pure CMF portals, hence the
name. However, use-cases rules and I did not have any pure CMF
use-case... This may or may not happen in the future.

**Important note:** please note that the standard Secure MailHost
(which is shipped with Plone) and its base product (MailHost) are not
intended to send a lot of emails. It is highly suggested to install
`MaildropHost`_ if you are about to do so.

.. _MaildropHost: http://www.dataflake.org/software/maildrophost


Installation and configuration
==============================

See ``doc/install.txt``.


Troubleshooting and bug report
==============================

See ``doc/how-to-troubleshoot.txt``. Patches are welcome.


Documentation
=============

Documentation is located in the ``doc`` folder. Start by
``doc/index.txt``. It is also mirrored on `CMFNotification home page`_
on `plone.org`_.

.. _CMFNotification home page: http://plone.org/products/cmfnotification/documentation

.. _plone.org: http://plone.org


Credits
=======

This product has been partially sponsored by `Pilot Systems`_.

The following people have developed, given help or tested this
product:

- Damien Baty (damien DOT baty AT gmail DOT com):
  original author, tests, documentation, maintenance;

- Kurt Bendl: better uninstallation;

- Jan-Carel Brand: eggification;

- Alex Garel: "labels" feature;

- Gaël Le Mignot (gael AT pilotsystems DOT net - Pilot Systems): bug
  fixes;

- Gaël Pasgrimaud: bug fixes, insightful comments and default mail
  templates in the early days.

- Izak Burger: Let the notification mechanism be a named utility.

Translations:

- Gunter Vasold (gunter DOT vasold AT fh-joanneum DOT at - FH
  Joanneum): translation in German;

- Júlio Monteiro (monteiro AT lab DOT pro DOT br): translation in
  Brazilian Portuguese;

- Leonardo caballero: translation in Spanish;

- Victor Fernandez de Alba: translation in Catalan.

.. _Pilot Systems: http://www.pilotsystems.net


License
=======

This product is licensed under GNU GPL. See 'LICENSE.txt' for further
informations.
