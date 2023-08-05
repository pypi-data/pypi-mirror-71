*******
IMSVDEX
*******

API to access and modify XML files in the ``IMS Vocabulary Definition Exchange``
format::

    The IMS Vocabulary Definition Exchange (VDEX) specification defines a
    grammar  for the exchange of value lists of various classes: collections
    often denoted "vocabulary". Specifically, VDEX defines a grammar for the
    exchange of simple machine-readable lists of values, or terms, together with
    information that may aid a human being in understanding the meaning or
    applicability of the various terms. VDEX may be used to express valid data
    for use in instances of IEEE LOM, IMS Metadata, IMS Learner Information Package
    and ADL SCORM, etc, for example. In these cases, the terms are often not human
    language words or phrases but more abstract tokens. VDEX can also express
    strictly hierarchical schemes in a compact manner while allowing for more loose
    networks of relationship to be expressed if required.

[CITVDEXSITE].

.. [CITVDEXSITE] citation from IMS Global, the VDEX-specification-page_
.. _VDEX-specification-page: http://www.imsglobal.org/vdex

This module takes the VDEX-XML objects and offers an API to them.

VDEX Version 1 Final Specification is supported, except VDEX references.
