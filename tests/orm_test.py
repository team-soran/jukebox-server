from jukebox.orm import load_all_modules_from_dir


def test_load_all_modules_from_dir(tmpdir):
    testdir = tmpdir.mkdir('test')
    initpy = testdir.join('__init__.py')
    initpy.write('')
    foopy = testdir.join('foo.py')
    foopy.write("__all__ = 'a','b',\na=1\nb=2")
    barpy = testdir.join('bar.py')
    barpy.write("__all__ = 'c',\nc=1\nd=1")
    print(testdir.strpath)
    modules = [x for x in load_all_modules_from_dir(testdir.strpath)]
    assert len(modules) == 2
    modules = sorted(modules, key=lambda x: x.__name__)
    assert modules[0].c == 1
    assert modules[1].a == 1
    assert modules[1].b == 2
