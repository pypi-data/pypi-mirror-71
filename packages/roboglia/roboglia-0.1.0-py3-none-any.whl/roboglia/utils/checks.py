# Copyright (C) 2020  Alex Sonea

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


def check_key(key, dict_info, context, context_id, logger, message=None):
    """Checks if a `key` is in a dictionary `dict_info` and raises a customized
    exception message with better context.

    Args:
        key (str): the key we are looking for
        dict_info (dict): the dictionary where we are looking
        context (str): a string indicating the context of the check, for
            example 'Bus' or 'Device'
        context_id (str or int): indicates the precise context (the name
            of the object or, in case the `key` we are searching is the name
            we will have to use the index of the item in the initialization
            dictionary)
        logger (logger object): where the logging will be written
        message (str): if this is provided the function will use this message
            for logging and raise instead of building a message specific
            for the context.

    Raises:
        KeyError: if the `key` is not found in the `dict_info`
    """
    if key not in dict_info:
        if message is None:
            message = f'"{key}" specification missing ' + \
                      f'for {context}: {context_id}'
        else:
            message = f'{message} for {context}: {context_id}'
        logger.critical(message)
        raise KeyError(message)


def check_type(value, to_type, context, context_id, logger, message=None):
    """Checks if a value is of a certain type and raises a customized
    exception message with better context.

    Args:
        value (any): a value to be checked
        to_type (type): the type to be checked against
        context (str): a string indicating the context of the check, for
            example 'Bus' or 'Device'
        context_id (str or int): indicates the precise context (the name
            of the object or, in case the `key` we are searching is the name
            we will have to use the index of the item in the initialization
            dictionary)
        logger (logger object): where the logging will be written
        message (str): if this is provided the function will use this message
            for logging and raise instead of building a message specific
            for the context.

    Raises:
        ValueError: if the value is not of the type indicated
    """
    if type(to_type) == list:
        # we compare with a list of types
        for one_type in to_type:
            if isinstance(value, one_type):
                # we are ok
                return None
    else:
        # one value only
        if isinstance(value, to_type):
            # we are ol
            return None
    # if we are here it means that either in the one type or a list of types
    # we could not find a match
    if message is None:
        message = f'value {value} should be of type {to_type} ' + \
                    f'for {context}: {context_id}'
    else:
        message = f'{message} for {context}: {context_id}'
    logger.critical(message)
    raise ValueError(message)


def check_options(value, options, context, context_id, logger, message=None):
    """Checks if a value is in a list of allowed options.

    Args:
        value (any): a value to be checked
        options (list): the allowed options for the value
        context (str): a string indicating the context of the check, for
            example 'Bus' or 'Device'
        context_id (str or int): indicates the precise context (the name
            of the object or, in case the `key` we are searching is the name
            we will have to use the index of the item in the initialization
            dictionary)
        logger (logger object): where the logging will be written
        message (str): if this is provided the function will use this message
            for logging and raise instead of building a message specific
            for the context.

    Raises:
        ValueError: if the value is not in the allowed options
    """
    if value not in options:
        if message is None:
            message = f'value {value} should be one of {options} ' + \
                      f'for {context}: {context_id}'
        else:
            message = f'{message} for {context}: {context_id}'
        logger.critical(message)
        raise ValueError(message)


def check_not_empty(value, descriptor, context, context_id, logger,
                    message=None):
    """Checks if a value is not empty (``''`` or ``{}`` or ``[]`` or ``None``).

    Parameters
    ----------
    value: any
        a value to be checked

    descriptor: str
        a string identifying the value checked, for example 'name'

    context: str
        a string indicating the context of the check, for example 'Bus' or
        'Device'

    context_id: str
        indicates the precise context (the name of the object)

    logger: logger object
        where the logging will be written

    message: str
        if this is provided the function will use this message
        for logging and raise instead of building a message specific
        for the context.

    Raises
    ------
    ValueError
        if the value is empty
    """
    if not value:
        if message is None:
            message = f'Parameter "{descriptor}" should not be empty ' + \
                      f'for {context}: "{context_id}"'
        else:
            message = f'{message} for {context}: "{context_id}"'
        logger.critical(message)
        raise ValueError(message)
