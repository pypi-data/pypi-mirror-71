============
 nti.ntiids
============

.. image:: https://travis-ci.org/NextThought/nti.ntiids.svg?branch=master
   :target: https://travis-ci.org/NextThought/nti.ntiids

.. image:: https://coveralls.io/repos/github/NextThought/nti.ntiids/badge.svg?branch=master
   :target: https://coveralls.io/github/NextThought/nti.ntiids?branch=master

.. image:: https://readthedocs.org/projects/ntintiids/badge/?version=latest
   :target: https://ntintiids.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

This package provides support for semantic URIs for objects using the
`tag URI scheme <https://en.wikipedia.org/wiki/Tag_URI_scheme>`_.
These tag URIs are used to look up objects in an application, usually
independent of their traversal path. These URIs, structured in a
particular way, are called NTIIDs. When represented as strings, they
use the Python text (unicode) type.

In the ``specific`` part of the URI, each NTIID includes a type. A
type is essentially a namespace in which the rest of the specific part
is to be interpreted. A set of known types are defined in
``nti.ntiids.ntiids``, as are functions to parse and generate NTIIDs.

The set of types is extensible through ``zope.component``
registrations for important interfaces like
``nti.ntiids.interfaces.INTIIDResolver``, which is registered by name
for specific types of NTIIDs. No resolvers are provided by this package.


The package ``nti.ntiids.oids`` integrates with
``nti.externalization`` and serves as the hook used for external
identifiers. These are derived from persistent ZODB object identifiers
("oid") with support for multiple databases (a multi-ZODB).
