==========
CHANGE LOG
==========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_ and this project adheres to `Semantic Versioning`_.


0.2.0 – 2020-06-15
==================

Added
-----

* New metric `zypper_needs_rebooting` exports wether the system requires a reboot according to ``zypper needs-rebooting``.
* New metric `zypper_product_end_of_live` exports end of life of products as reported by ``zypper lifecycle``.
* New metric `zypper_service_needs_restart` exported for each service reported by `zypper ps -sss`.
* Python 3.8 is now supported

Removed
-------

* Python 2 is no longer supported


0.1.0 – 2017-12-31
==================

Added
-----

* Dump metrics on available patches on standard output


_`Keep a Changelog`: http://keepachangelog.com/en/1.0.0/
_`Semantic Versioning`: http://semver.org/spec/v2.0.0.html
