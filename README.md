## Meade LX200-GPS mount daemon

`meade_mountd` interfaces with the mount over RS232 and exposes a
coherent telescope control interface via Pyro.

`tel` is a commandline utility for controlling the telescope.

### Configuration

Configuration is read from json files that are installed by default to `/etc/mountd`.
A configuration file is specified when launching the server, and the `tel` frontend will search this location when launched.

```python
{
  "daemon": "warwick_telescope", # Run the server as this daemon. Daemon types are registered in `rockit.common.daemons`.
  "log_name": "meaded@warwick", # The name to use when writing messages to the observatory log.
  "control_machines": ["WarwickTCS"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `rockit.common.IP`.
  "serial_port": "/dev/mount", # Serial FIFO for communicating with the mount
  "serial_baud": 9600, # Serial baud rate
  "serial_timeout": 3, # Serial comms timeout
  "latitude": 52.376861, # Site latitude in degrees.
  "longitude": -1.583861, # Site longitude in degrees.
  "altitude": 94, # Site altitude in metres.
  "initialize_timeout": 120, # Maximum time to connect and configure the mount (in seconds)
  "slew_timeout": 90, # Maximum time to slew from any position to any other position (in seconds)
  "slew_loop delay": 0.25, # Interval to poll the mount status while slewing (in seconds)
  "idle_loop_delay": 1, # Interval to poll the mount status while not slewing (in seconds)
  "ha_soft_limits": [-82, 82], # Allowed hour angle range in degrees
  "dec_soft_limits": [-20, 85], # Allowed declination range in degrees
  "park_positions": {
    "zenith": { # Positions that can be used with 'tel park'.
      "desc": "pointing directly up", # Description reported by 'tel park'.
      "alt": 90, # Altitude in degrees.
      "az": 0 # Azimuth in degrees.
    }
  }
}
```

### Initial Installation

The automated packaging scripts will push 3 RPM packages to the observatory package repository:

| Package                   | Description                                                                  |
|---------------------------|------------------------------------------------------------------------------|
| rockit-meade-server       | Contains the `meade_mountd` server and systemd service file.                 |
| rockit-meade-client       | Contains the `tel` commandline utility for controlling the telescope server. |
| rockit-meade-data-warwick | Contains the json configuration for the Windmill Hill telescope.             |
| python3-rockit-meade      | Contains the python module with shared code.                                 |

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable --now meade_mountd@<config>
```

where `config` is the name of the json file for the appropriate telescope.

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `rockit.common.daemons` for the daemon specified in the config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl restart meade_mountd@<config>
```

### Testing Locally

The server and client can be run directly from a git clone:
```
./meade_mountd warwick.json
MOUNTD_CONFIG_PATH=./warwick.json ./tel status
```
