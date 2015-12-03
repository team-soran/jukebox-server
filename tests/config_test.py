import pathlib
import pytest

from jukebox.config import Config, JukeboxConfig, config_property


@pytest.fixture
def fx_config_source():
    return '''
    [web]
    debug = true
    secret_key = "hello world"

    [database]
    url = "sqlite:///"
    '''


class TestConfig(Config):

    @config_property
    def debug(self):
        config = self.data['debug']
        assert isinstance(config, bool)
        return config


def test_config(tmpdir):
    toml_source = '''
    [helloworld]
    debug = true
    '''
    jukebox_config_from_srouce = TestConfig.from_source(toml_source)
    assert jukebox_config_from_srouce.data['helloworld']['debug']
    toml_file = tmpdir.mkdir('toml').join('fixture.toml')
    toml_file.write(toml_source)
    path = pathlib.Path(tmpdir.strpath) / 'toml' / 'fixture.toml'
    jukebox_config = TestConfig.from_path(path)
    assert jukebox_config.data == jukebox_config_from_srouce.data


def test_config_config_property():
    toml_source = '''
    [helloworld]
    a = 1
    '''
    with pytest.raises(TypeError):
        jukebox_config = TestConfig.from_source(toml_source)
        assert jukebox_config.debug
    toml_source = '''
    debug = "a"
    '''
    with pytest.raises(AssertionError):
        jukebox_config = TestConfig.from_source(toml_source)
        print(jukebox_config.debug)


def test_jukebox_config_web():
    toml_file = '''
    [web]
    debug = true
    testing = false
    secret_key = "abc"
    '''
    jukebox_config = JukeboxConfig.from_source(toml_file)
    assert jukebox_config.web['debug']
    assert not jukebox_config.web['testing']
    assert jukebox_config.web['secret_key'] == "abc"


def test_jukebox_config_web_typeerror():
    with pytest.raises(TypeError):
        toml_file = '''
        [hello]
        world = 1
        '''
        jukebox_config = JukeboxConfig.from_source(toml_file)
        assert jukebox_config.web


def test_jukebox_config_web_assertionerror():
    with pytest.raises(AssertionError):
        toml_file = '''
        [web]
        testing = true
        '''
        jukebox_config = JukeboxConfig.from_source(toml_file)
        print(jukebox_config.web)
    with pytest.raises(AssertionError):
        toml_file = '''
        [web]
        debug = 1
        '''
        jukebox_config = JukeboxConfig.from_source(toml_file)
        print(jukebox_config.web)
    with pytest.raises(AssertionError):
        toml_file = '''
        [web]
        secret_key = 1
        '''
        jukebox_config = JukeboxConfig.from_source(toml_file)
        print(jukebox_config.web)


def test_jukebox_config_database():
    toml_file = '''
    [database]
    url = "sqlite:///"
    '''
    jukebox_config = JukeboxConfig.from_source(toml_file)
    assert jukebox_config.database['url']
    toml_file = '''
    [hi]
    a = "a"
    '''
    with pytest.raises(TypeError):
        jukebox_config = JukeboxConfig.from_source(toml_file)
        assert jukebox_config.database['url']
    toml_file = '''
    [database]
    a = "sqlite:///"
    '''
    with pytest.raises(AssertionError):
        jukebox_config = JukeboxConfig.from_source(toml_file)
        assert jukebox_config.database['url']


def test_jukebox_config_database_engine(fx_config_source):
    jukebox_config = JukeboxConfig.from_source(fx_config_source)
    assert jukebox_config.database_engine
    expect_url = jukebox_config.database['url']
    assert str(jukebox_config.database_engine.url) == expect_url
    assert jukebox_config.database_engine.echo
