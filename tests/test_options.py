import pytest

from frozen_options import Options

def test_getitem():
    opt = Options(key=2, test=42)

    assert opt["test"] == 42
    assert opt["key"] == 2

def test_getattr():
    opt = Options(key=2, test=42)

    assert opt.test == 42
    assert opt.key == 2

def test_keys():
    opt = Options(key=2, test=42)
    keys = list(opt.keys())
    assert len(keys) == 2
    assert "key" in keys
    assert "test" in keys

def test_setattr():
    with pytest.raises(TypeError) as excinfo:
        opt = Options()
        opt.value = 3
    assert "assignment" in str(excinfo.value)

def test_setitem():
    with pytest.raises(TypeError) as excinfo:
        opt = Options()
        opt["value"] = 3
    assert "assignment" in str(excinfo.value)

def test_del():
    opt = Options(key=2, test=42)
    with pytest.raises(TypeError) as excinfo:
        del opt["key"]
    assert "deletion" in str(excinfo.value)  

def test_withAll_1():
    opt = Options(key=2, test=42)
    opt2 = opt.withAll(test=4)
    assert opt2.test == 4
    assert opt.test == 42

def test_withAll_2():
    opt = Options(key=2, test=42)
    opt2 = opt.withAll(test=4, an_other="hello")
    
    assert opt2.an_other == "hello"
    assert opt2.test == 4
    assert opt.test == 42
    with pytest.raises(KeyError) as excinfo:
        val = opt.an_other
    assert "an_other" in str(excinfo)

def test_withValues_1():
    opt = Options(key=2, test=42)
    opt2 = opt.withValues(test=4)
    assert opt2.test == 4
    assert opt.test == 42


def test_withValues_2():
    opt = Options(key=2, test=42)
    opt2 = opt.withValues(test=4, an_other="hello")
    
    assert opt2.test == 4
    with pytest.raises(KeyError) as excinfo:
        val = opt2.an_other
    assert "an_other" in str(excinfo)
    
    assert opt.test == 42
    with pytest.raises(KeyError) as excinfo:
        val = opt.an_other
    assert "an_other" in str(excinfo)

def test_without():
    opt = Options(key=2, test=42)
    opt2 = opt.without("test")
    
    assert opt.test == 42
    with pytest.raises(KeyError) as excinfo:
        val = opt2.test
    assert "test" in str(excinfo)

def test_without_2():
    opt = Options(key=2, test=42)
    opt2 = opt.without("test", "key")
    
    assert opt.test == 42
    assert opt.key == 2
    with pytest.raises(KeyError) as excinfo:
        val = opt2.test
    assert "test" in str(excinfo)
    with pytest.raises(KeyError) as excinfo:
        val = opt2.key
    assert "key" in str(excinfo)
