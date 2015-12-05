""":mod:`jukebox.orm` --- database related
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import pkgutil
import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#: (:class:`~sqlalchemy.orm.session.Session`)
Session = sessionmaker(autocommit=True)


#: Construct a base class for declarative class definitions.
Base = declarative_base()


def load_all_modules_from_dir(dirname):
    """Load all modules from directory,

    .. seealso::

       `Loading all modules in a folder in Python`__
           stackoverflow answer shows various way to import all modules

    __ http://stackoverflow.com/a/8556471

    """
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = '%s.%s' % (dirname, package_name)
        if full_package_name not in sys.modules:
            finder = importer.find_module(package_name)
            yield finder.load_module(package_name)
