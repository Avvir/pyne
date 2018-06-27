from .expectations import expect
from .matchers import anything

def test__anything__satisfies_to_be():
    expect(anything).to_be(1234)