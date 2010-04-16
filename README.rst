``ptemplate`` --- lightweight, data-driven templating
*****************************************************

ptemplate is a lightweight templating engine for Python, heavily
inspired by Google's ctemplate language. Like ctemplate, ptemplate
strongly separates the application's logic and presentation. At its
heart, ptemplate is an extension of Python's advanced string
formatting facility -- it extends the interpreter's built-in
formatters to provide a fast, expressive, content-agnostic templating
system.


Installing ``ptemplate``
========================

You can install the latest stable version of ``ptemplate`` using
**pip**:

   $ pip install ptemplate

Mirrors of the project's repository are hosted at github.com and
bitbucket.org -- feel free to clone and issue pull requests at either
service. For git users:

   $ git clone http://github.com/wcmaier/ptemplate.git

And for Mercurial users:

   $ hg clone http://bitbucket.org/lt_kije/ptemplate/

Both github and bitbucket provide feeds of changes to the project; for
example:

   http://github.com/wcmaier/ptemplate/commits/master.atom

If you'd like to contribute an improvement to ``ptemplate``, please
consider using either of the above services. Otherwise, send an email
to willmaier@ml1.net.


A quick tour of ``ptemplate``'s features
========================================

Simple extension of Python's advanced string formatting API (**PEP
3101**):

   >>> from ptemplate.formatter import Formatter
   >>> formatter = Formatter()
   >>> template = """normal variable substitution: {var}"""
   >>> formatter.format(template, var="foo")
   'normal variable substitution: foo'

   >>> template = """{#section}this is {something} {/section}"""
   >>> data = {"section": [{"something": "fast"}, {"something": "easy"}, {"something": "simple"}]}
   >>> formatter.format(template, **data)
   'this is fast this is easy this is simple '

   >>> template = """{%this is a comment}"""
   >>> formatter.format(template, **{})
   ''

Content filtering system (eg HTML sanitization):

   >>> import cgi
   >>> from ptemplate.template import Template
   >>> templater = Template()
   >>> templater.converters["h"] = cgi.escape

   >>> data = {"content": """<p>some HTML from the wild</p>"""}
   >>> templater.template = """something dangerous: {content!h}"""
   >>> templater.render(data)
   'something dangerous: &lt;p&gt;some HTML from the wild&lt;/p&gt;'

   >>> data = {"section": [{"example": "<p>paragraph</p>"},{"example": "no html here"}]}
   >>> templater.template = """you can sanitize entire sections, too ({#section!h}{example} {/section})"""
   >>> templater.render(data)
   'you can sanitize entire sections, too (&lt;p&gt;paragraph&lt;/p&gt; no html here )'

Basic compatibility with Google's :

   >>> from ptemplate.ctemplate import CTemplate
   >>> template = """Google is {{#section}}{{something}}, {{/section}}"""
   >>> templater = CTemplate(template=template)
   >>> data = {"section": [{"something": "not evil"},{"something": "a company"}]}
   >>> templater.render(data)
   'Google is not evil, a company, '


Basic usage
===========

Despite its simple syntax, templates processed by ``ptemplate`` can
still produce very complex documents. Unlike most template systems,
``ptemplate`` encourages you to keep application logic where it
belongs -- in your application. Expansion of the template is
controlled solely by the structure of your data. This keeps the
templating engine itself simple and fast and makes writing and
debugging your templates even easier. For more on the philosophy
behind data-driven templating systems, see "How To Use the Google
Template System".

All of the ``ptemplate`` interfaces take a single data dictionary and
use it to expand a simple string template. The data dictionary's keys
are plain strings; its values are either strings or lists of other
data dictionaries. Other objects may be used as values, but they will
be converted to strings before being inserted into the template.
String values are substituted for variables in the template. List
values control the number of iterations (and scope) of section
variables.

Templates are composed of plain text with (optional) variable and
section markers. ``ptemplate`` markers must all be valid field names
as described in **PEP 3101** and begin and end with '{' and '}',
respectively. Special fields denoting comments and the beginning and
end of sections are marked with a single-character indicator ('!',
'#', '/'). Comment fields are ignored completely. Sections are
expanded once for each data dictionary found in evaluation scope.

Variable expansion proceeds from the innermost context to the
outermost; if no match is found, an empty string is substituted
instead. Variables defined within a section will first attempt to
match keys in that section's dictionary. If no match is found, the
dictionary in which the section is defined will be searched for a
match. This process continues until all dictionaries (or "scopes") are
exhausted.

For example, this deeply nested data dictionary produces the
following:

   >>> from ptemplate.template import Template
   >>> templater = Template()

   >>> data = {
   ...     "outer": [
   ...         {"foo": "foo",
   ...         "middle": [
   ...             {"foo": "bar",
   ...             "inner": [
   ...                 {"foo": "baz"},
   ...             ]},
   ...         ]},
   ...     ]}
   >>> template = """{#outer}outer: {foo} {#middle}middle: {foo} {#inner}inner: {foo} {/inner}{/middle}{/outer}"""
   >>> templater.template = template
   >>> templater.render(data)
   'outer: foo middle: bar inner: baz '

At each level, a new value for "foo" is defined. If the innermost
value is removed, though, the next-highest value is used:

   >>> data["outer"][0]["middle"][0]["inner"][0].pop("foo")
   'baz'
   >>> templater.render(data)
   'outer: foo middle: bar inner: bar '


ctemplate support
=================

Since ``ptemplate`` and Google's ctemplate are so similar internally,
it's fairly easy to process ctemplate templates with ``ptemplate``. In
fact, with a very naive preprocessor, ``ptemplate.ctemplate`` can pass
many of Google's ctemplate unittests. To expand ctemplate(-like)
templates, use ``ptemplate.ctemplate.CTemplate`` instead of
``ptemplate.template.Template``.

Note: ``ptemplate.ctemplate.CTemplate`` does not provide full ctemplate
  compatibility. See the class documentation for specific exceptions.


API
===

You have access to the templating system at three levels. First, you
can interact directly with ``ptemplate.formatter.Formatter``, which
offers an interface very similar to Python's advanced string
formatting (``string.Formatter``, **PEP 3101**). Second, you can work
with (or subclass) ``ptemplate.template.Template``, a thin wrapper
around the formatter that also adds a Buffet-style API. Lastly, you
can use ``ptemplate.ctemplate.CTemplate``. ``CTemplate`` extends
``Template`` with a preprocessor that supports a subset of Google's
ctemplate system. ``ctemplate`` also provides a nice example for
subclassing and extending the basic ``template``.

For a typical use case, ``ptemplate.template`` is probably most useful
as it provides a familiar API. ``ptemplate.ctemplate`` should (with,
perhaps, a few changes to the preprocessor) support many simple
templates written for Google's ctemplate system. For smaller projects
(or doing things like formatting error messages),
``ptemplate.formatter`` may be sufficient on its own.


``ptemplate.formatter`` -- extended string formatter
----------------------------------------------------

This module extends the advanced string formatter (**PEP 3101**)
available in Python versions greater than 2.5. In addition to regular
variable substitution and formatting, ``Formatter`` supports sections
and in-template comments.

class class ptemplate.formatter.Formatter

   Bases: ``string.Formatter``

   A string formatter.

   ``Formatter`` extends the advanced string formatter described in
   **PEP 3101** and implemented in Python versions greater than 2.5.
   It provides hooks that simplify token conversion (``converters``)
   and recognize special template variables (``markers``). Since it
   uses ``str._formatter_parser()`` (implemented in C in the standard
   interpreter) to parse the input string, it should also perform
   relatively well.

   convert_field(value, conversion)

      Convert a field *value* according to a *conversion*
      specification.

      If *conversion* is registered in ``converters``, the *value* is
      passed to the matching converter and the output is returned.
      Otherwise, the *value* and *conversion* specification are passed
      to ``string.Formatter.convert_field()``.

   converters

      A dictionary of converter functions keyed by conversion strings.

      If a token's conversion string matches a key in this dictionary,
      ``convert_field()`` will use the converter instead of the usual
      string conversion.

      Note: Keys in this dictionary must be one character in length (to
        match ``str._formatter_parser()``'s expectations for format
        flags).

   formatsection(tokens, data, scopes=[])

      Format a section of a token stream according to *data*.

      ``formatsection()`` builds a formatted string from the iterable
      *tokens*. If it encounters a section in the stream, it creates a
      new stream and passes the section (and everything in it) to
      another invocation of ``formatsection()``, adding its output to
      the formatted string. This continues recursively until there are
      no more sections and the stream of tokens is finished. Then, the
      formatted result is returned.

      When a section is completed, its output will be passed to
      ``convert_field()`` and ``format_field()`` if the
      ``Section.conversion`` or ``Section.format`` attributes were
      defined, respectively.

   get_value(field, args, scopes)

      Look up the value of *field* in *scopes*.

      *scopes* is a list of data dictionaries associated with each
      successive parent of the current section. ``get_value()``
      searches for a key matching *field* in each of these
      dictionaries, in order. If no match is found, an empty string is
      returned. Otherwise, the key's value (a list of data
      dictionaries or a string) is returned.

   markerlen

      The length of a marker indicator.

   markers

      A dictionary mapping marker indicators to marker type names.

      The extended syntax supported by ``Formatter`` is composed of
      markers within normal template variables. Markers registered
      here can trigger extended behavior in ``_vformat()``.

   tokenize(string)

      Tokenize a template *string*.

      ``tokenize()`` parses *string* using
      ``string.Formatter.parse()`` (which in turn relies on
      ``str._formatter_parser()``) and yields ``Token`` instances
      using the parsed data.

   vformat(string, args, kwargs)

      Format *string* according to data in *args* and *kwargs*.

      Unlike ``string.Formatter.vformat()``, this method does not
      track (or complain about) unused arguments.

class class ptemplate.formatter.Section

   Bases: ``tuple``

   A template section.

   Constructor arguments should be passed as keywords and include:

   *name* is the name of the section (not including the section
   marker).

   *tokens* is a list of ``Token`` instances that belong in the
   section.

   *data* is a template data dictionary applicable to the section.

   *scopes* is a list of data dictionaries that should be searched
   successively when resolving variables in the section.

   *conversion* is a conversion string. If not None, it will be passed
   with the output of the section to ``Formatter.convert_field()``.

   *format* is a format string. If not None, it will be passed with
   the output of the section to ``Formatter.format_field()``.

   conversion

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

   data

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

   format

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

   name

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

   scopes

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

   tokens

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

class class ptemplate.formatter.Token

   Bases: ``tuple``

   A template token.

   Constructor arguments should be passed as keywords and include:

   *text* is the literal text preceding the token.

   *field* is the name of the field (or None), not including the
   marker indicator.

   *fieldname* is the full name of the field (or None), including the
   marker indicator.

   *marker* is a marker type registered in ``Formatter.markers``.

   *spec* is a format string passed with the token's contents to
   ``Formatter.format_field()``.

   *conversion* is a conversion string passed with the token's
   contents to ``Formatter.convert_field()``.

   conversion

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

   field

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

   fieldname

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

   marker

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

   spec

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])

   text

      itemgetter(item, ...) --> itemgetter object

      Return a callable object that fetches the given item(s) from its
      operand. After, f=itemgetter(2), the call f(r) returns r[2].
      After, g=itemgetter(2,5,3), the call g(r) returns (r[2], r[5],
      r[3])


``ptemplate.template`` -- advanced string templating
----------------------------------------------------

``ptemplate.template`` provides a ``Template``, a thin interface on
top ``ptemplate.formatter`` that is more useful for typical templating
tasks.

class class ptemplate.template.Template(extra_vars_func=None, options=None, template='')

   Bases: ``object``

   A templater.

   ``Template`` wraps ``ptemplate.formatter.Formatter`` with a
   -compatible . In addition to the standard Buffet arguments
   (*extra_vars_func*, *options*), the constructor accepts a
   *template* string. This string is the template that will be
   rendered later (by a call to ``render()``).

   converters

      A dictionary of object converters.

      These converters will be passed to the template's
      ``ptemplate.formatter.Formatter`` instance.

   load_template(templatename)

      Find a template specified in Python 'dot' notation.

      Required by Buffet; not supported.

   preprocessor

      Template preprocessor callable.

      This callable should accept the template string as its sole
      argument. Its output should be another template string. Use this
      facility to translate foreign template syntaxes into something
      ``ptemplate.formatter.Formatter`` can understand.

   render(data, format='html', fragment=False, template=None)

      Render the template using *data*.

      The *format*, *fragment* and *template* arguments are ignored.
      Instead, ``Template`` uses ``template`` as the template, passing
      it to ``preprocessor`` if necessary. It then expands the
      template (using ``formatter``) and returns the result as a
      string.

   transform(info, template)

      Render the output to Elements.

      Required by Buffet; not supported.


``ptemplate.ctemplate`` -- ctemplate-like interface
---------------------------------------------------

This module implements a templating interface similar Google's
ctemplate with a few important exceptions:

* templates may not change the field delimiter

* modifiers are marked with '!'

* comments are marked with '%'

* the templater does not strip whitespace (except by modifiers)

* includes are not supported

* pragmas/macros are not supported

* separator sections are not supported

Like ctemplate, ``CTemplate`` expands a string template to match the
structure of a dictionary (using ``ptemplate.template.Template``).
Data dictionaries may contain either lists of other data dictionaries
or single values (string, integer, float, etc). Plain variables are
substituted according to the usual Python string formatting rules (see
**PEP 3101**). Sections (fields preceded by '#') are expanded once for
each data dictionary contained in the corresponding list.

class class ptemplate.ctemplate.CTemplate(extra_vars_func=None, options=None, template='')

   Bases: ``ptemplate.template.Template``

   A (somewhat) ctemplate-compatible templater.

   Incompatibilities with Google's ctemplate are documented in
   ``ptemplate.ctemplate``. Construction of a ``CTemplate`` instance
   is the same as with ``ptemplate.template.Template``.

   globals

      A global data dictionary.

      Template variables that don't match keys in the main data
      dictionary may match global keys as a last resort. By default,
      ``globals`` contains BI_NEWLINE and BI_SPACE, which match the
      space and newline characters, respectively (as in ctemplate).

   preprocessor(input)

      Convert Google's ctemplate syntax.

      Since ctemplate and ``ptemplate.template`` are quite similar
      internally, a simple translation can make a document (mostly)
      legible. At the moment, the preprocessor only converts the
      marker indicators ('{{' and '}}') and comment character ('!').

   render(data, format='html', fragment=False, template=None)

      Render the template.

      Here, ``CTemplate`` adds the ``globals`` dictionary to the
      *data* dictionary before calling
      ``ptemplate.template.Template.render()``.


Developing ``ptemplate``
========================


Syncing with github and bitbucket
---------------------------------

Even though all development of ``ptemplate`` occurs in a Mercurial
repository, it's useful to provide a git mirror on Github, the very
popular hosting service. This mirror (as well as the Mercurial mirror
on bitbucket) is kept in sync using Mercurial hooks and hg-git. First,
a local mirror is created of the main Mercurial repository:

   $ hg clone -U . .mirror

The mirror clone does not need to have a working directory, so the
*-U* flag is passed to the clone subcommand. Then, the main
repository's default path is set to point to the local mirror:

   $ cat <<EOF >| .hg/hgrc
   [paths]
   default = .mirror
   EOF

Finally, the mirror is configured to push to the hosting services
every time it receives a new changegroup (ie, when we push from the
master to the mirror):

   $ cat <<EOF >| .mirror/.hg/hgrc
   [paths]
   github = git+ssh://git@github.com/wcmaier/ptemplate.git
   bitbucket = ssh://hg@bitbucket.org/lt_kije/ptemplate

   [hooks]
   changegroup.updatemaster = hg bookmark -f -r default master
   changegroup.bitbucket = hg push bitbucket
   changegroup.github = hg push github
   EOF

Now, when new changesets are pushed to the mirror, it will update the
'master' bookmark and push to Github and bitbucket. It is important to
update the master bookmark before attempting to push to a git
repository because Mercurial bookmarks (which hg-git uses to compare
against the git master revision) are not updated when the mirror
repository receives a push.


Running the tests
-----------------

``ptemplate`` ships with a number of unit tests that help ensure that
the code runs correctly. The tests live in the ``tests`` package and
can be run by ``setup.py``:

   $ python setup.py test

All new code in ``ptemplate`` should be accompanied by unit and/or
functional tests. Note that many of the unit tests included here are
ported from Google's ctemplate (and run against the
``ptemplate.ctemplate`` interface). Ideally, ``ptemplate`` should pass
as many of ctemplate's tests as possible.

You can get a sense for how completely the unit tests exercise
``ptemplate`` by running the coverage tool:

   $ coverage run --branch setup.py test

``coverage`` tracks the code statements and branches that the test
suite touches and can generate a report listing the lines of code that
are missed:

   $ coverage report -m --omit "tests,/home/will/lib,lib/cli/ext,setup"

It's useful to omit the third party code directory (``ext``) as well
as the path to the Python standard library as well as ``setup.py`` and
the tests themselves.


Running the benchmark
---------------------

The ``ptemplate`` repository contains a port of the Genshi benchmark
suite. To run the benchmarks:

   $ cd tests/bench
   $ python basic.py | grep -v "not installed" | sort -n -k1.40bn
   $ python bigtable.py | grep -v "not installed" | sort -k1.40bn

You can also run benchmarks against selected template engines by
passing the engine name (ie "ptemplate", "ctemplate") as an argument
to the benchmark script.

As of 2010.04.15, the benchmark produced the following results (sorted
by ''bigtable.py''):

+-----------------+---------+-----------------+-------------------------+---------------------------------+
| Engine Name     | Version | basic.py (ms)   | bigtable.py (ms)        | Notes                           |
+=================+=========+=================+=========================+=================================+
| Mako            | 0.3.2   | 0.71            | 190.21                  |                                 |
+-----------------+---------+-----------------+-------------------------+---------------------------------+
| Genshi_text     | 0.5.1   | 2.65            | 554.41                  |                                 |
+-----------------+---------+-----------------+-------------------------+---------------------------------+
| Ptemplate       | 0.1     | 3.42            | 1188.61                 |                                 |
+-----------------+---------+-----------------+-------------------------+---------------------------------+
| Ctemplate       | 0.1     | 3.64            | 1296.58                 |                                 |
+-----------------+---------+-----------------+-------------------------+---------------------------------+
| Genshi          | 0.5.1   | 7.75            | 1228.97                 | template                        |
+-----------------+---------+-----------------+-------------------------+---------------------------------+
| Genshi          | 0.5.1   | n/a             | 1566.21                 | tag builder                     |
+-----------------+---------+-----------------+-------------------------+---------------------------------+
| Django          | 1.1.1   | 6.29            | 1872.76                 |                                 |
+-----------------+---------+-----------------+-------------------------+---------------------------------+
| Genshi          | 0.5.1   | n/a             | 1996.71                 | template + tag builder          |
+-----------------+---------+-----------------+-------------------------+---------------------------------+
| Kid             | 0.9.6   | 15.34           | 3508.88                 |                                 |
+-----------------+---------+-----------------+-------------------------+---------------------------------+

The test system was:

* AMD Athlon(tm) 64 Processor 3200+ ("AuthenticAMD" 686-class, 512KB
  L2 cache)

* 1 GB RAM

* OpenBSD 4.7-current

* Python 2.6.3
