# --This file is used strictly for creating docs-----------
from physics.fields import available_fields
from physics.docstring import docstring_parameter_dict


class DocBase(object):

    # @docstring_parameter_dict(available_fields)
    # def fields(self):
    #     """The available fields are {0}.
    #
    #     """

    @docstring_parameter_dict(available_fields)
    def fields(self):
        """The available fields are:
         {0}.

        """
