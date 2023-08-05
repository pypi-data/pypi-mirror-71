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

import logging
from pathlib import Path

from dynamixel_sdk import DXL_HIBYTE, DXL_HIWORD, DXL_LOBYTE, DXL_LOWORD

from ..base import BaseDevice

logger = logging.getLogger(__name__)


class DynamixelDevice(BaseDevice):
    """Implements specific functionality for Dynamixel devices.

    Differences are:

    - different version of :py:meth:`get_model_path` that
      will point to the local ``device`` directory in the ``dynamixel``
      module

    - the initialization parameters are the same as for the class
      :py:class:`BaseDevice`
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_model_path(self):
        """Builds the path to the `.yml` documents.

        Returns:
            str :A full document path including the name of the model and the
                extension `.yml`.
        """
        # return os.path.join(os.path.dirname(__file__), 'devices')
        return Path(__file__).parent / 'devices/'

    def register_low_endian(self, value, size):
        """Converts a value into a list of bytes in little endian order.

        Args:
            value (int): the value of the register
            size (int): the size of the register

        Returns:
            (list) List of bytes of len ``size`` with bytes ordered lowest
                first.
        """
        if size == 1:
            return [value]
        elif size == 2:
            return [DXL_LOBYTE(value), DXL_HIBYTE(value)]
        elif size == 4:
            lw = DXL_LOWORD(value)
            hw = DXL_HIWORD(value)
            return [DXL_LOBYTE(lw), DXL_HIBYTE(lw),
                    DXL_LOBYTE(hw), DXL_HIBYTE(hw)]
        else:
            logger.error(f'Unexpected register size: {size}')
            return None
