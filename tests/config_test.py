import pathlib
import pytest

from jukebox.config import Config, JukeboxConfig


class TestConfig(Config):

    pass


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
        assert jukebox_config.web
    with pytest.raises(AssertionError):
        toml_file = '''
        [web]
        debug = 1
        '''
        jukebox_config = JukeboxConfig.from_source(toml_file)
        assert jukebox_config.web
    with pytest.raises(AssertionError):
        toml_file = '''
        [web]
        secret_key = 1
        '''
        jukebox_config = JukeboxConfig.from_source(toml_file)
        assert jukebox_config.web
