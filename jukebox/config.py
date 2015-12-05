""":mod:`jukebox.config` --- jukebox configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections.abc
import types
import pathlib

import toml
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm.session import Session as SQLAlchemySession
from werkzeug.utils import cached_property

from .orm import Session


__all__ = 'Config', 'JukeboxConfig', 'Session', 'config_property',


class config_property(object):
    """Property of :class:`~.Config`\ , only it checks object has
    a configuration has same name as functions name, but also caches result of
    property

    .. code-block:: python

       class SomeConfig(Config):

           @config_property
           def hello(self):
               return self.data['hello']

    """

    def __init__(self, func: types.FunctionType):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if self.func.__name__ not in obj.data:
            raise TypeError('{} missing 1 required configuration: {}'.format(
                obj.__class__.__name__, self.func.__name__
            ))
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class Config(object):
    """Configuration class, it can read configuration from source and pathlib.
    every configuration class have to inherit this class.

    .. code-block:: python

       class SomeConfig(Config):

           ....

    :param configuration: a configuration
    :type configuration: :class:`collections.abc.Mapping`

    """

    def __init__(self, configuration: collections.abc.Mapping):
        self.data = configuration

    @classmethod
    def from_source(cls, source: str):
        """Load configuration from source. ``source`` must be a TOML.

        .. seealso::

           `TOML`__
               Tom's Obvious, Minimal Language.

        __ https://github.com/toml-lang/toml

        :param source: configuration source
        :type source: :class:`str`
        :return: a configuration object
        :rtype: :class:`~.Config`

        """
        return cls(toml.loads(source))

    @classmethod
    def from_path(cls, path: pathlib.Path):
        """Load configuration from path.

        :param path: configuration file path
        :type path: :class:`pathlib.Path`
        :return: a configuration object
        :rtype: :class:`~.Config`

        """
        with open(str(path), 'r') as f:
            return cls.from_source(f.read())


class JukeboxConfig(Config):
    """Jukebox configuration, it has to be used to configure flask app.

    .. code-block:: python

       jukebox_config = JukeboxConfig.from_path('./config.toml')

    """

    @config_property
    def web(self) -> collections.abc.Mapping:
        """Configuration for flask app, it have to contains configuration
        below.

        - (:class:`bool`) ``debug``
        - (:class:`str`) ``secret_key``

        """
        config = self.data['web']
        assert 'debug' in config
        assert 'secret_key' in config
        return config

    @config_property
    def database(self) -> collections.abc.Mapping:
        """Database configuration

        - (:class:`str`) ``url``

        """
        config = self.data['database']
        assert 'url' in config
        return config

    @cached_property
    def database_engine(self) -> Engine:
        """Create database engine, it is binded to
        :class:`sqlalchemy.orm.session.Session`

        :return: sqlalchemy engine
        :rtype: :class:`sqlalchemy.orm.engine.Engine`

        """
        engine = create_engine(
            self.database['url'],
            encoding=self.database.get('encoding', 'utf-8'),
            echo=self.database.get('echo', True),
        )
        return engine

    def create_session(self, bind: Engine=None) -> SQLAlchemySession:
        """Create sqlalchemy session object, if ``bind`` is ``None``\ ,
        binding :attr:`~.JukeboxConfig.database_engine`\ .

        :return: a sqlalchemy session
        :rtype: :class:`sqlalchemy.orm.session.Session`

        """
        if bind is None:
            bind = self.database_engine
        return Session(bind=bind)
