# -*- coding: utf-8 -*-

import sys, os, glob, pwd, grp, signal, time
from resource_management import *


class RedisSlave(Script):

    # Install Redis
    def install(self, env):
        import params
        env.set_params(params)

        # Install dependent packages
        self.install_packages(env)

        # Create user
        try:
            grp.getgrnam(params.redis_group)
        except KeyError:
            Group(group_name=params.redis_group)

        # Create group
        try:
            pwd.getpwnam(params.redis_user)
        except KeyError:
            User(username=params.redis_user,
                 gid=params.redis_group,
                 groups=[params.redis_group],
                 ignore_failures=True
                 )

        # Create directories
        Directory([params.redis_base_dir_slave, params.log_file_dir_slave, params.pid_file_dir, params.dir_slave],
                  mode=0755,
                  cd_access='a',
                  owner=params.redis_user,
                  group=params.redis_group,
                  create_parents=True
                  )

        # Download Redis
        cmd = format("cd {redis_base_dir_slave}; wget {redis_download_url} -O redis.tar.gz")
        Execute(cmd, user=params.redis_user)

        # Install Redis
        cmd = format("cd {redis_base_dir_slave}; tar -xf redis.tar.gz --strip-components=1; make")
        Execute(cmd, user=params.redis_user)

        # Ensure all files owned by Redis user
        cmd = format("chown -R {redis_user}:{redis_group} {redis_base_dir_slave}")
        Execute(cmd)

        # Remove Redis installation file
        cmd = format("cd {redis_base_dir_slave}; rm -fr redis.tar.gz")
        Execute(cmd, user=params.redis_user)

        Execute('echo "Redis install complete"')

    # Configure Redis
    def configure(self, env):
        import params
        env.set_params(params)

        network_configurations = params.config['configurations']['redis-conf-network']
        File(format("{redis_base_dir_slave}/redis.conf"),
             content=Template("redis-slave.conf.j2", configurations=network_configurations),
             owner=params.redis_user,
             group=params.redis_group
             )

        general_configurations = params.config['configurations']['redis-conf-general']
        File(format("{redis_base_dir_slave}/redis.conf"),
             content=Template("redis-slave.conf.j2", configurations=general_configurations),
             owner=params.redis_user,
             group=params.redis_group
             )

        cluster_configurations = params.config['configurations']['redis-conf-cluster']
        File(format("{redis_base_dir_slave}/redis.conf"),
             content=Template("redis-slave.conf.j2", configurations=cluster_configurations),
             owner=params.redis_user,
             group=params.redis_group
             )

        storage_configurations = params.config['configurations']['redis-conf-storage']
        File(format("{redis_base_dir_slave}/redis.conf"),
             content=Template("redis-slave.conf.j2", configurations=storage_configurations),
             owner=params.redis_user,
             group=params.redis_group
             )

        cmd = format("chown -R {redis_user}:{redis_group} {redis_base_dir_slave}")
        Execute(cmd)

        # Make sure pid directory exist
        Directory([params.pid_file_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.redis_user,
                  group=params.redis_group,
                  create_parents=True
                  )

        Execute('echo "Configuration complete"')


    def stop(self, env):
        import params
        env.set_params(params)

        # Stop Redis
        """
            Kill the process by pid file, then check the process is running or not. If the process is still running after the kill
            command, it will try to kill with -9 option (hard kill)
            """
        pid_file = params.pid_file_slave
        pid = os.popen('cat {pid_file}'.format(pid_file=pid_file)).read()

        process_id_exists_command = format("ls {pid_file} >/dev/null 2>&1 && ps -p {pid} >/dev/null 2>&1")

        kill_cmd = format("kill {pid}")
        Execute(kill_cmd,
                not_if=format("! ({process_id_exists_command})"))

        wait_time = 5

        hard_kill_cmd = format("kill -9 {pid}")
        Execute(hard_kill_cmd,
                not_if=format(
                    "! ({process_id_exists_command}) || ( sleep {wait_time} && ! ({process_id_exists_command}) )"),
                ignore_failures=True)


    def start(self, env):
        import params
        env.set_params(params)

        # Configure Redis
        self.configure(env)

        # Start Redis
        cmd = format("nohup {redis_base_dir_slave}/src/redis-server {conf_file_slave} &")
        Execute(cmd, user=params.redis_user)

        # Init Cluster
        if params.cluster_enabled_flag is True:
            # get ip
            ip = os.popen('cat /etc/hosts | grep {hostname} | awk -F " " \'{extra1}\''.format(hostname=params.hostname, extra1=params.extra1)).read().strip()
            time.sleep(10)
            add_slave_cmd = format("{redis_base_dir_slave}/src/redis-cli --cluster add-node {ip}:{slave_port} {existing_host}:{master_port} --cluster-slave")
            Execute(add_slave_cmd, user=params.redis_user, ignore_failures=True)


    def status(self, env):
        import status_params
        env.set_params(status_params)

        # Use built-in method to check status using pidfile
        check_process_status(status_params.pid_file_slave)


if __name__ == "__main__":
    RedisSlave().execute()