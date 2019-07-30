"""Some helper functions for creating docstrings"""


def docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec


def docstring_parameter_dict(sub):
    def dec(obj):
        holder = []
        for key, value in sub.items():
            holder.append(' {0} {1}'.format(key, value))
        string = ','.join(holder)
        obj.__doc__ = obj.__doc__.format(string)
        return obj
    return dec
