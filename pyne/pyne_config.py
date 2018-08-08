from pyne.pyne_test_collection import PyneTestCollection


class PyneConfig:
    def __init__(self):
        self.report_between_suites = True
        self.test_collection = PyneTestCollection()

config = PyneConfig()
