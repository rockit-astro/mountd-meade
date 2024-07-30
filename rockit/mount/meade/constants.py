#
# This file is part of the Robotic Observatory Control Kit (rockit)
#
# rockit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rockit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rockit.  If not, see <http://www.gnu.org/licenses/>.

"""Constants and status codes used by meaded"""


class CommandStatus:
    """Numeric return codes"""
    # General error codes
    Succeeded = 0
    Failed = 1
    Blocked = 2

    InvalidControlIP = 5

    # Command-specific codes
    NotConnected = 10
    InvalidMountConfiguration = 11
    NotDisconnected = 14
    UnknownParkPosition = 15

    OutsideHALimits = 20
    OutsideDecLimits = 21

    _messages = {
        # General error codes
        1: 'error: command failed',
        2: 'error: another command is already running',
        5: 'error: command not accepted from this IP',

        # Command-specific codes
        9: 'error: PWI4 software is not running',
        10: 'error: mount has not been initialized',
        11: 'error: mount handset is not correctly configured',
        14: 'error: mount has already been initialized',
        15: 'error: unknown park position',

        20: 'error: requested coordinates outside HA limits',
        21: 'error: requested coordinates outside Dec limits',

        # tel specific codes
        -100: 'error: terminated by user',
        -101: 'error: unable to communicate with telescope daemon',
        -102: 'error: command not available for this telescope'
    }

    @classmethod
    def message(cls, error_code):
        """Returns a human readable string describing an error code"""
        if error_code in cls._messages:
            return cls._messages[error_code]
        return 'error: Unknown error code {}'.format(error_code)


class TelescopeState:
    """Represents the current mount state"""
    Disabled, Initializing, Stopped, Slewing, Tracking = range(5)

    _labels = {
        0: 'DISABLED',
        1: 'INITIALIZING',
        2: 'STOPPED',
        3: 'SLEWING',
        4: 'TRACKING',
    }

    _colors = {
        0: 'red',
        1: 'yellow',
        2: 'red',
        3: 'yellow',
        4: 'green'
    }

    @classmethod
    def label(cls, status, formatting=False):
        """
        Returns a human readable string describing a status
        Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._labels and status in cls._colors:
                return f'[b][{cls._colors[status]}]{cls._labels[status]}[/{cls._colors[status]}][/b]'
            return '[b][red]UNKNOWN[/red][/b]'

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN'