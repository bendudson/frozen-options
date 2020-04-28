try:
    from collections.abc import Mapping  # >= python 3.3
except:
    from collections import Mapping

class Options(Mapping):
    """Immutable dictionary-like structure for configuration options
    """
    __isfrozen = False  # Allow changes during initialisation
    
    def __init__(self, *args, **kwargs):
        self.__data = {}
        for arg in args:
            for key in arg:
                self.__data[key] = arg[key]
        # Other keywords 
        for key in kwargs:
            self.__data[key] = kwargs[key]
        self.__isfrozen = True  # Disable further updates
    
    def keys(self):
        return self.__data.keys()

    def items(self):
        return self.__data.items()
    
    def __contains__(self, key):
        return key in self.__data
    
    def __getitem__(self, key):
        return self.__data.__getitem__(key)

    def __getattr__(self, key):
        """Access dictionary items using dot access shorthand"""
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        if self.__isfrozen:
            raise TypeError("'Options' object does not support item assignment")
        object.__setattr__(self, key, value)
    
    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def withValues(self, *args, **kwargs):
        """Return a copy, overriding given values. Don't add new keys"""
        newdata = self.__data.copy()
        # Arguments are collections e.g. dicts, other Options
        for arg in args:
            for key in arg:
                if key in newdata: # Ignore unknown keys
                    newdata[key] = arg[key]
        # Other keywords
        for key in kwargs:
            if key in newdata: # Ignore unknown keys
                newdata[key] = kwargs[key]
        return Options(**newdata)
    
    def without(self, *omit_keys):
        """Return a copy without the given keys"""
        newdata = {}
        for key, value in self.__data.items():
            if key not in omit_keys:
                newdata[key] = value
        return Options(**newdata)
    
    def __str__(self):
        return self.__data.__str__()
    
    def __repr__(self):
        return "Options(" + ", ".join([str(key) + "=" + repr(value)
                                       for key, value in self.__data.items()]) + ")"

