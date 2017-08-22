minisparql
==========

**minisparql** is a faux SPARQL server
that only supports request with `?query=…` in the URL (no `POST`)
with queries of the form
`SELECT (REGEX("…", "…") AS ?matches) {}`.
It can be used as SPARQL endpoint for the [WikibaseQualityConstraints] extension
when it’s not possible to run a real SPARQL server
(e. g. due to lack of resources).

Installation
------------

Run the following commands as root:

```sh
make install
systemctl daemon-reload
systemctl enable --now minisparql.socket
```

You can run the inverse steps (`disable`, `daemon-reload`, `uninstall`)
to undo the installation.

The Makefile respects `$(DESTDIR)`, but not `$(prefix)`,
because the full path to the installed Python file
is also hard-coded into the `minisparql@.service` unit file.

Usage
-----

Add the following to your `LocalSettings.php`:

```php
$wgWBQualityConstraintsSparqlEndpoint = 'http://localhost:9998/';
```

You might also want to increase the default `$wgWBQualityConstraintsTypeCheckMaxEntities`,
because this server does not support the queries needed to check types in SPARQL.

Background
----------

To check the “format” constraint,
the constraints extension needs to check arbitrary input against arbitrary regular expressions.
To avoid denial-of-service attacks (e. g. via catastrophic backtracking),
the regexes are not checked in PHP directly
but instead delegated to the configured SPARQL service,
since the regex flavors are fairly similar
(though not identical).

When lack of resources or other limitations
make it impossible to run a real SPARQL server (e. g. Blazegraph),
this server can be used to supply the same regex-checking functionality.
Since a new instance is started for every request
(`Accept=true` in `minisparql.socket`)
and the service is resource-limited
(`LimitCPU=1s` in `minisparql@.service`),
it should not be possible to exhaust server resources via expensive regexes.

License
-------

The content of this repository is released under the AGPL3+
as provided in the LICENSE file that accompanied this code.

By submitting a “pull request” or otherwise contributing to
this repository, you agree to license your contribution under
the license mentioned above.

[WikibaseQualityConstraints]: https://github.com/wikimedia/mediawiki-extensions-WikibaseQualityConstraints
