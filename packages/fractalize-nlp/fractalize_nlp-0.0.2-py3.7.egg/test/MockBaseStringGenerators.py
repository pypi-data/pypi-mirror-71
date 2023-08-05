from fractalize_nlp.string_generators.utils import *

class MockBaseStringGenerator():
    def __init__(self, config):
        load_sources(self, config)
    
    def sample(self,n=10):
        return sample(self.__dict__[self.state_field],
                      self.state_field,
                      n)

class CorrectBaseStringGenerator(MockBaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)

class ContractedBaseStringGenerator(MockBaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)

class EmptyBaseStringGenerator(MockBaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)       

class ExtendedBaseStringGenerator(MockBaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)

class MismatchBaseStringGenerator(MockBaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)       

class MultipleBaseStringGenerator(MockBaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)

class NoDirBaseStringGenerator(MockBaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)    

class NonexistentBaseStringGenerator(MockBaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)

class NoStringBaseStringGenerator(MockBaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)
  