"""\
ptemplate is a lightweight templating engine for Python, heavily inspired by
Google's `ctemplate <http://google-ctemplate.googlecode.com/>`_ language.
Like ctemplate, ptemplate strongly separates the application's logic and
presentation. At its heart, ptemplate is an extension of Python's advanced
string formatting facility -- it extends the interpreter's built-in formatters
to provide a fast, expressive, content-agnostic templating system.
"""

__project__ = "ptemplate"
__version__ = "0.1"
__pkg__ = "ptemplate"
__description__ = "data-based templating"
__author__ = "Will Maier"
__author_email__ = "willmaier@ml1.net"
__url__ = "http://code.lfod.us/ptemplate"

# See http://pypi.python.org/pypi?%3Aaction=list_classifiers.
__classifiers__ = """\
Development Status :: 3 - Alpha
Environment :: Web Environment :: Buffet
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Natural Language :: English
Programming Language :: Python
Topic :: Text Processing
""".splitlines()
__keywords__ = "template text json data"

__requires__ = []

# The following is modeled after the ISC license.
__copyright__ = """\
Copyright (c) 2010 Will Maier <willmaier@ml1.net>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

__todo__ = """\
"""

from .ctemplate import *
from .formatter import *
from .template import *
