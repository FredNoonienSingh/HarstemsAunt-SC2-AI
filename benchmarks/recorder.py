import functools
from typing import List, Dict

def record_benchmark(attributes:List) -> Dict:
    """_summary_

    Args:
        attributes (List): _description_

    Returns:
        Dict: _description_
    """

    def decorator(cls):
        instance = cls.__init__

        def new_instance(self, *args, **kwargs):
            instance(self,*args,**kwargs)
            if not hasattr(self, '_recorded_values'):
                self._recorded_values = {}
            for attr_name in attributes:
                if hasattr(self, attr_name):
                    self._recorded_values[attr_name] = getattr(self, attr_name)

        cls.__init__ = new_instance
        return cls
    return decorator