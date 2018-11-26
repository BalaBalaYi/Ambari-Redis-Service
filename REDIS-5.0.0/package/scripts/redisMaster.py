# -*- coding: utf-8 -*-

import sys, os, glob, pwd, grp, signal, time
from resource_management import *


class RedisMaster(Script):

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
        Directory([params.redis_base_dir, params.log_file_dir, params.pid_file_dir, params.dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.redis_user,
                  group=params.redis_group,
                  create_parents=True
                  )

        # Download Redis
        cmd = format("cd {redis_base_dir}; wget {redis_download_url} -O redis.tar.gz")
        Execute(cmd, user=params.redis_user)

        # Install Redis
        cmd = format("cd {redis_base_dir}; tar -xf redis.tar.gz --strip-components=1; make")
        Execute(cmd, user=params.redis_user)

        # Ensure all files owned by Redis user
        cmd = format("chown -R {redis_user}:{redis_group} {redis_base_dir}")
        Execute(cmd)

        # Remove Redis installation file
        cmd = format("cd {redis_base_dir}; rm -fr redis.tar.gz")
        Execute(cmd, user=params.redis_user)

        Execute('echo "Redis install complete"')

    # Configure Redis
    def configure(self, env):
        import params
        env.set_params(params)

        network_configurations = params.config['configurations']['redis-conf-network']
        File(format("{redis_base_dir}/redis.conf"),
             content=Template("redis-master.conf.j2", configurations=network_configurations),
             owner=params.redis_user,
             group=params.redis_group
             )

        general_configurations = params.config['configurations']['redis-conf-general']
        File(format("{redis_base_dir}/redis.conf"),
             content=Template("redis-master.conf.j2", configurations=general_configurations),
             owner=params.redis_user,
             group=params.redis_group
             )

        cluster_configurations = params.config['configurations']['redis-conf-cluster']
        File(format("{redis_base_dir}/redis.conf"),
             content=Template("redis-master.conf.j2", configurations=cluster_configurations),
             owner=params.redis_user,
             group=params.redis_group
             )

        storage_configurations = params.config['configurations']['redis-conf-storage']
        File(format("{redis_base_dir}/redis.conf"),
             content=Template("redis-master.conf.j2", configurations=storage_configurations),
             owner=params.redis_user,
             group=params.redis_group
             )

        cmd = format("chown -R {redis_user}:{redis_group} {redis_base_dir}")
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
        pid_file = params.pid_file
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
        start_cmd = format("nohup {redis_base_dir}/src/redis-server {conf_file} &")
        Execute(start_cmd, user=params.redis_user)

        wait_time = 10

        # Init Cluster
        if params.cluster_enabled_flag is True:
            init_cluster_cmd = format("echo yes | {redis_base_dir}/src/redis-cli --cluster create {cluster_master_host_port_param}")
            Execute(init_cluster_cmd, user=params.redis_user, ignore_failures=True)


    def status(self, env):
        import status_params
        env.set_params(status_params)

        # Use built-in method to check status using pidfile
        check_process_status(status_params.pid_file)


if __name__ == "__main__":
    RedisMaster().execute()