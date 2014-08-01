from uno.base import UnoBase



class TestBase(UnoBase):
        pass

def test_UnoBase_render():
    tester = TestBase()
    tester._render = 'BASE'
    assert tester._render == 'BASE'

def test_UnoBase__html__():
    tester = TestBase()
    tester._render = 'BASE'
    assert tester.__html__() == u'BASE'

def test_UnoBase__str__():
    tester = TestBase()
    tester._render = 'BASE'
    assert tester.__str__() == 'BASE'

def test_UnoBase__repr__():
    tester = TestBase()
    tester._render = 'BASE'
    assert tester.__repr__() == 'BASE'

def test_UnoBase__unicode__():
    tester = TestBase()
    tester._render = 'BASE'
    assert tester.__unicode__() == u'BASE'

def test_UnoBase__call__():
    tester = TestBase()
    tester._render = 'BASE'
    assert tester.__call__() == tester

def test_UnoBase__add__():
    tester = TestBase()
    tester._render = 'BASE'
    assert tester + tester == 'BASEBASE'
    assert tester + 'yay'  == 'BASEyay'
    assert tester + 1      == 'BASE1'

def test_UnoBase__setattr__():
    tester = TestBase()
    tester._features = dict()
    tester.thing = 'should_not_show_up_in_features.keys()_list' #is not an UnoBase
    tester._something_else_that_should_not_show_up_in_features_keys_list = 1
    tester.shows_up = TestBase()
    assert len(tester._features.keys()) == 1
    assert 'shows_up' in tester._features.keys()
    assert isinstance(tester._features['shows_up'], UnoBase) #yea... thought of it last. w/e
