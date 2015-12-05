from pytest import fixture, yield_fixture

from jukebox.config import JukeboxConfig
from jukebox.orm import Base


@fixture
def fx_jukebox_config():
    return JukeboxConfig({
        'database': {
            'url': 'sqlite:///'
        }
    })


@yield_fixture
def fx_connection(fx_jukebox_config):
    """Joining a session into an external transaction


    .. seealso::

       `SQLAlchemy session transaction`__
           Documentation for SQLAlchemy session transaction for test suites

    __ http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites

    """  # noqa
    engine = fx_jukebox_config.database_engine
    connection = engine.connect()
    try:
        Base.metadata.create_all(bind=connection)
        transaction = connection.begin()
        yield connection
    finally:
        transaction.rollback()
        connection.close()


@yield_fixture
def fx_session(fx_connection, fx_jukebox_config):
    session = fx_jukebox_config.create_session(bind=fx_connection)
    try:
        yield session
    finally:
        session.close()
