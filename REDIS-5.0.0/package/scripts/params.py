# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Redis Params configurations
"""

from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
import status_params
import os

config = Script.get_config()

java64_home = config['hostLevelParams']['java_home']
hostname = config['hostname']


# = = = = = = = = = = = = = = = = = = = =
#          redis env
# = = = = = = = = = = = = = = = = = = = =
redis_user = config['configurations']['redis-env']['redis.user']
redis_group = config['configurations']['redis-env']['redis.group']
redis_base_dir = config['configurations']['redis-env']['redis.base.dir']
redis_download_url = config['configurations']['redis-env']['redis.download.url']

pid_file_dir = config['configurations']['redis-env']['pid.file.dir']
log_file_dir = config['configurations']['redis-env']['log.file.dir']
conf_file = redis_base_dir + '/redis.conf'

#slave
redis_base_dir_slave = redis_base_dir + '/slave'
log_file_dir_slave = log_file_dir + '/slave'
conf_file_slave = redis_base_dir_slave + '/redis.conf'


# = = = = = = = = = = = = = = = = = = = =
#          redis network config
# = = = = = = = = = = = = = = = = = = = =
bind = config['configurations']['redis-conf-network']['bind']
if bind == 'none' or not bind:
    bind = '# bind 127.0.0.1'
else:
    bind = 'bind ' + bind
protected_mode = config['configurations']['redis-conf-network']['protected-mode']
if protected_mode is True:
    protected_mode = 'yes'
else:
    protected_mode = 'no'
master_port = config['configurations']['redis-conf-network']['master-port']
slave_port = config['configurations']['redis-conf-network']['slave-port']
tcp_backlog = config['configurations']['redis-conf-network']['tcp-backlog']
unixsocket = config['configurations']['redis-conf-network']['unixsocket']
if unixsocket == 'none' or not unixsocket:
    unixsocket = '# unixsocket /tmp/redis.sock'
else:
    unixsocket = 'unixsocket ' + unixsocket
unixsocketperm = config['configurations']['redis-conf-network']['unixsocketperm']
if unixsocketperm == 'none' or not unixsocketperm:
    unixsocketperm = '# unixsocketperm 700'
else:
    unixsocketperm = 'unixsocketperm ' + unixsocketperm
timeout = config['configurations']['redis-conf-network']['timeout']
tcp_keepalive = config['configurations']['redis-conf-network']['tcp-keepalive']



# = = = = = = = = = = = = = = = = = = = =
#          redis general config
# = = = = = = = = = = = = = = = = = = = =
# GENERAL
loglevel = config['configurations']['redis-conf-general']['loglevel']
logfile = log_file_dir + '/redis.log'
logfile_slave = log_file_dir_slave + '/redis.log'
syslog_enabled = config['configurations']['redis-conf-general']['syslog-enabled']
if syslog_enabled is True:
    syslog_enabled = 'yes'
else:
    syslog_enabled = 'no'
syslog_ident = config['configurations']['redis-conf-general']['syslog-ident']
syslog_facility = config['configurations']['redis-conf-general']['syslog-facility']
databases = config['configurations']['redis-conf-general']['databases']
always_show_logo = config['configurations']['redis-conf-general']['always-show-logo']
if always_show_logo is True:
    always_show_logo = 'yes'
else:
    always_show_logo = 'no'

# SECURITY
requirepass = config['configurations']['redis-conf-general']['requirepass']
if requirepass == 'none' or not requirepass:
    requirepass = '# requirepass foobared'
else:
    requirepass = 'requirepass ' + requirepass

# CLIENTS
maxclients = 'maxclients ' + config['configurations']['redis-conf-general']['maxclients']

# MEMORY MANAGEMENT
maxmemory = config['configurations']['redis-conf-general']['maxmemory']
if maxmemory == '0' or not maxmemory:
    maxmemory = '# maxmemory <bytes>'
else:
    maxmemory = 'maxmemory ' + maxmemory
maxmemory_policy = 'maxmemory-policy ' + config['configurations']['redis-conf-general']['maxmemory-policy']
maxmemory_samples = 'maxmemory-samples '+ config['configurations']['redis-conf-general']['maxmemory-samples']
replica_ignore_maxmemory = config['configurations']['redis-conf-general']['replica-ignore-maxmemory']
if replica_ignore_maxmemory is True:
    replica_ignore_maxmemory = 'replica-ignore-maxmemory yes'
else:
    replica_ignore_maxmemory = 'replica-ignore-maxmemory no'

# LAZY FREEING
lazyfree_lazy_eviction = config['configurations']['redis-conf-general']['lazyfree-lazy-eviction']
if lazyfree_lazy_eviction is True:
    lazyfree_lazy_eviction = 'yes'
else:
    lazyfree_lazy_eviction = 'no'
lazyfree_lazy_expire =  config['configurations']['redis-conf-general']['lazyfree-lazy-expire']
if lazyfree_lazy_expire is True:
    lazyfree_lazy_expire = 'yes'
else:
    lazyfree_lazy_expire = 'no'
lazyfree_lazy_server_del = config['configurations']['redis-conf-general']['lazyfree-lazy-server-del']
if lazyfree_lazy_server_del is True:
    lazyfree_lazy_server_del = 'yes'
else:
    lazyfree_lazy_server_del = 'no'
replica_lazy_flush = config['configurations']['redis-conf-general']['replica-lazy-flush']
if replica_lazy_flush is True:
    replica_lazy_flush = 'yes'
else:
    replica_lazy_flush = 'no'

# APPEND ONLY MODE
appendonly = config['configurations']['redis-conf-general']['appendonly']
if appendonly is True:
    appendonly = 'yes'
else:
    appendonly = 'no'
appendfilename = '"' + config['configurations']['redis-conf-general']['appendfilename'] + '"'
appendfsync = 'appendfsync ' + config['configurations']['redis-conf-general']['appendfsync']
no_appendfsync_on_rewrite = config['configurations']['redis-conf-general']['no-appendfsync-on-rewrite']
if no_appendfsync_on_rewrite is True:
    no_appendfsync_on_rewrite = 'yes'
else:
    no_appendfsync_on_rewrite = 'no'
auto_aof_rewrite_percentage = config['configurations']['redis-conf-general']['auto-aof-rewrite-percentage']
auto_aof_rewrite_min_size = config['configurations']['redis-conf-general']['auto-aof-rewrite-min-size'] + 'mb'
aof_load_truncated = config['configurations']['redis-conf-general']['aof-load-truncated']
if aof_load_truncated is True:
    aof_load_truncated = 'yes'
else:
    aof_load_truncated = 'no'
aof_use_rdb_preamble = config['configurations']['redis-conf-general']['aof-use-rdb-preamble']
if aof_use_rdb_preamble is True:
    aof_use_rdb_preamble = 'yes'
else:
    aof_use_rdb_preamble = 'no'


# = = = = = = = = = = = = = = = = = = = =
#          redis cluster config
# = = = = = = = = = = = = = = = = = = = =
cluster_enabled = config['configurations']['redis-conf-cluster']['cluster-enabled']
cluster_master_host_list = config['configurations']['redis-conf-cluster']['cluster-master-host-list']
if cluster_master_host_list != 'none':
    cluster_master_host_port_param = ''
    for i, cluster_master_host in enumerate(cluster_master_host_list.split(",")):
        cluster_master_host_port_param = cluster_master_host_port_param + cluster_master_host + ':' + master_port + ' '
        if i == 0:
            existing_host = cluster_master_host

if cluster_enabled is True:
    cluster_enabled_flag = True
    cluster_enabled = 'cluster-enabled yes'

    # other params setting
    cluster_config_file = 'cluster-config-file ' + config['configurations']['redis-conf-cluster']['cluster-config-file']
    cluster_node_timeout = 'cluster-node-timeout ' + config['configurations']['redis-conf-cluster']['cluster-node-timeout']
    cluster_replica_validity_factor = 'cluster-replica-validity-factor ' + config['configurations']['redis-conf-cluster']['cluster-replica-validity-factor']
    cluster_migration_barrier = 'cluster-migration-barrier ' + config['configurations']['redis-conf-cluster']['cluster-migration-barrier']
    cluster_require_full_coverage = config['configurations']['redis-conf-cluster']['cluster-require-full-coverage']
    if cluster_require_full_coverage is True:
        cluster_require_full_coverage = 'cluster-require-full-coverage yes'
    else:
        cluster_require_full_coverage = 'cluster-require-full-coverage no'
    cluster_replica_no_failover = config['configurations']['redis-conf-cluster']['cluster-replica-no-failover']
    if cluster_replica_no_failover is True:
        cluster_replica_no_failover = 'cluster-replica-no-failover yes'
    else:
        cluster_replica_no_failover = 'cluster-replica-no-failover no'
else:
    cluster_enabled_flag = False
    cluster_enabled = 'cluster-enabled no'

    # other params setting
    cluster_config_file = '# cluster-config-file nodes-6379.conf'
    cluster_node_timeout = '# cluster-node-timeout 15000'
    cluster_replica_validity_factor = '# cluster-replica-validity-factor 10'
    cluster_migration_barrier = '# cluster-migration-barrier 1'
    cluster_require_full_coverage = '# cluster-require-full-coverage yes'
    cluster_replica_no_failover = '# cluster-replica-no-failover no'


# = = = = = = = = = = = = = = = = = = = =
#          redis storage config
# = = = = = = = = = = = = = = = = = = = =
# SNAPSHOTTING
save_enabled = config['configurations']['redis-conf-storage']['save-enabled']
if save_enabled is True:
    save_config = config['configurations']['redis-conf-storage']['save-config']
else:
    save_config = '# save ""'
stop_writes_on_bgsave_error = config['configurations']['redis-conf-storage']['stop-writes-on-bgsave-error']
if stop_writes_on_bgsave_error is True:
    stop_writes_on_bgsave_error = 'yes'
else:
    stop_writes_on_bgsave_error = 'no'
rdbcompression = config['configurations']['redis-conf-storage']['rdbcompression']
if rdbcompression is True:
    rdbcompression = 'yes'
else:
    rdbcompression = 'no'
rdbchecksum = config['configurations']['redis-conf-storage']['rdbchecksum']
if rdbchecksum is True:
    rdbchecksum = 'yes'
else:
    rdbchecksum = 'no'
dbfilename = config['configurations']['redis-conf-storage']['dbfilename']
dir = config['configurations']['redis-conf-storage']['dir']
dir_slave = dir + '/slave'

# REPLICATION
replica_serve_stale_data = config['configurations']['redis-conf-storage']['replica-serve-stale-data']
if replica_serve_stale_data is True:
    replica_serve_stale_data = 'yes'
else:
    replica_serve_stale_data = 'no'
replica_read_only = config['configurations']['redis-conf-storage']['replica-read-only']
if replica_read_only is True:
    replica_read_only = 'yes'
else:
    replica_read_only = 'no'
repl_diskless_sync = config['configurations']['redis-conf-storage']['repl-diskless-sync']
if repl_diskless_sync is True:
    repl_diskless_sync = 'yes'
else:
    repl_diskless_sync = 'no'
repl_diskless_sync_delay = config['configurations']['redis-conf-storage']['repl-diskless-sync-delay']
repl_disable_tcp_nodelay = config['configurations']['redis-conf-storage']['repl-disable-tcp-nodelay']
if repl_disable_tcp_nodelay is True:
    repl_disable_tcp_nodelay = 'yes'
else:
    repl_disable_tcp_nodelay = 'no'
replica_priority = config['configurations']['redis-conf-storage']['replica-priority']





# = = = = = = = = = = = = = = = = = = = =
#                 main
# = = = = = = = = = = = = = = = = = = = =
pid_file = pid_file_dir + '/redis.pid'
pid_file_slave = pid_file_dir + '/redis-slave.pid'


# = = = = = = = = = = = = = = = = = = = =
#                 extra
# = = = = = = = = = = = = = = = = = = = =
extra1 = '{print $1}'

