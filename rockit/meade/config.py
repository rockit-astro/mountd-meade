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

"""Helper function to validate and parse the json config file"""

import json
from rockit.common import daemons, IP, validation

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'daemon', 'log_name', 'control_machines', 'serial_port', 'serial_baud', 'serial_timeout',
        'latitude', 'longitude', 'altitude', 'initialize_timeout', 'slew_timeout', 'slew_loop_delay',
        'ha_soft_limits', 'dec_soft_limits', 'park_positions'
    ],
    'properties': {
        'daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'log_name': {
            'type': 'string',
        },
        'control_machines': {
            'type': 'array',
            'items': {
                'type': 'string',
                'machine_name': True
            }
        },
        # optional
        'dome_daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'serial_port': {
            'type': 'string',
        },
        'serial_baud': {
            'type': 'number',
            'min': 0
        },
        'serial_timeout': {
            'type': 'number',
            'min': 0
        },
        'latitude': {
            'type': 'number',
            'minimum': -90,
            'maximum': 90
        },
        'longitude': {
            'type': 'number',
            'minimum': -180,
            'maximum': 180
        },
        'altitude': {
            'type': 'number',
            'minimum': 0
        },
        'initialize_timeout': {
            'type': 'number',
            'min': 0
        },
        'slew_timeout': {
            'type': 'number',
            'minimum': 0
        },
        'slew_loop_delay': {
            'type': 'number',
            'minimum': 0
        },
        'idle_loop_delay': {
            'type': 'number',
            'minimum': 0
        },
        'ha_soft_limits': {
            'type': 'array',
            'maxItems': 2,
            'minItems': 2,
            'items': {
                'type': 'number',
                'min': -180,
                'max': 180
            }
        },
        'dec_soft_limits': {
            'type': 'array',
            'maxItems': 2,
            'minItems': 2,
            'items': {
                'type': 'number',
                'min': -90,
                'max': 90
            }
        },
        'park_positions': {
            'type': 'object',
            'additionalProperties': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['desc', 'alt', 'az'],
                'properties': {
                    'desc': {
                        'type': 'string',
                    },
                    'alt': {
                        'type': 'number',
                        'min': 0,
                        'max': 90
                    },
                    'az': {
                        'type': 'number',
                        'min': 0,
                        'max': 360
                    }
                }
            }
        }
    }
}


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validation.validate_config(config_json, CONFIG_SCHEMA, {
            'daemon_name': validation.daemon_name_validator,
            'machine_name': validation.machine_name_validator
        })

        self.daemon = getattr(daemons, config_json['daemon'])
        self.log_name = config_json['log_name']
        self.control_ips = [getattr(IP, machine) for machine in config_json['control_machines']]

        self.dome_daemon = None
        if 'dome_daemon' in config_json:
            self.dome_daemon = getattr(daemons, config_json['dome_daemon'])

        self.serial_port = config_json['serial_port']
        self.serial_baud = int(config_json['serial_baud'])
        self.serial_timeout = int(config_json['serial_timeout'])
        self.latitude = float(config_json['latitude'])
        self.longitude = float(config_json['longitude'])
        self.altitude = float(config_json['altitude'])
        self.initialize_timeout = config_json['initialize_timeout']
        self.slew_timeout = config_json['slew_timeout']
        self.slew_loop_delay = config_json['slew_loop_delay']
        self.idle_loop_delay = config_json['idle_loop_delay']
        self.ha_soft_limits = config_json['ha_soft_limits']
        self.dec_soft_limits = config_json['dec_soft_limits']
        self.park_positions = config_json['park_positions']
