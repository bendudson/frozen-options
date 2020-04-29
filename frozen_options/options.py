try:
    from collections.abc import Mapping  # >= python 3.3
except:
    from collections import Mapping

class Options(Mapping):
    """Immutable dictionary-like structure for configuration options
    
    Examples
    --------

    Create like a dict, including nested Options:

    data = Options(setting = value, 
                   section = Options(subsetting = value2))
    
    Access data with ["key"] or .key syntax:

    data["setting"] # => value
    data.section.subsetting  # => value2

    Transform nested data structures without mutating the original.
    This is done by merging nested dicts or Options 
    (any collection.abs.Mapping objects).

    data2 = Options(data, {"section":{"subsetting": newvalue}})
    
    data2 is now the same as data, but 
    data.section.subsetting  # => newvalue

    These are shallow copies, so in a nested tree of Options only the parts
    which change are copied.
    """
    
    __isfrozen = False  # Allow changes during initialisation

    def __init__(self, *args, **kwargs):
        """
        Inputs
        ------
        
        arguments    Mapping objects e.g dictionaries or Objects
                     These are recursively merged together, so that
                     nested dictionaries or Options are combined.
                     This transforms nested immutable structures.
        
        keywords     Replace or set keys. These replace rather than merge.
        """
        self.__data = {}
        for arg in args:
            for key, value in arg.items():
                if (key in self.__data and
                    isinstance(self.__data[key], Mapping) and
                    isinstance(value, Mapping)):
                    # Recursively merge Options with any Mapping e.g. dict, other Options
                    self.__data[key] = Options(self.__data[key], value)
                else:
                    self.__data[key] = value
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
        """Return a copy, recursively overriding given values. Don't add new keys.
        If this Option contains nested Options, then those values are also extracted.      
        """
        newdata = self.__data.copy()

        def getExistingKeys(values):
            for key, value in values.items():
                if key in newdata: # Ignore unknown keys
                    if (isinstance(newdata[key], Options) and
                        isinstance(value, Mapping)):
                        newdata[key] = newdata[key].withValues(value)
                    else:
                        newdata[key] = value

        # Arguments are collections e.g. dicts, other Options
        for arg in args:
            getExistingKeys(arg)
        # Other keywords
        getExistingKeys(kwargs)
        return Options(newdata)

    def without(self, *omit_keys):
        """Return a copy without the given keys"""
        newdata = {}
        for key, value in self.__data.items():
            if key not in omit_keys:
                newdata[key] = value
        return Options(newdata)

    def __str__(self):
        return self.__data.__str__()
    
    def __repr__(self):
        return "Options(" + ", ".join([str(key) + "=" + repr(value)
                                       for key, value in self.__data.items()]) + ")"
