from collections import defaultdict
import copy


class OptDict(defaultdict):
    """ Recursive default dictionary definition allowing to traverse it based
        on optional (potential missing) keys. Useful for traversing JSON with
        missing keys
    """

    def __missing__(self, key):
        return self.default_factory()

    @classmethod
    def from_dict(cls, dictionary):
        """Creates an OptDict from a dict"""

        empty = lambda: cls(empty)  # Recursive empty defaultdict definition
        opt_dict_factory = lambda dict_val: cls(empty, dict_val)

        def to_opt_dict(d):
            for k, v in d.items():
                if isinstance(v, dict):
                    new_dict = to_opt_dict(v)
                    d[k] = new_dict
                elif isinstance(v, list):
                    new_list = list(map(lambda x: to_opt_dict(x) if isinstance(x, dict) else x, v))
                    d[k] = new_list
            return opt_dict_factory(d)

        return to_opt_dict(copy.deepcopy(dictionary))
