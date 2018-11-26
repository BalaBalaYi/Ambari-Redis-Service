# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Redis service params
"""

from resource_management import *

config = Script.get_config()

pid_file_dir = config['configurations']['redis-env']['pid.file.dir']
pid_file = format("{pid_file_dir}/redis.pid")
pid_file_slave = format("{pid_file_dir}/redis-slave.pid")
