#!/usr/bin/python

import json
import platform
import subprocess

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "6"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

TOPCOMMAND='ps -eo comm=|sort|uniq -c | sort -k1nr | head -n 50'

def metricCollector():
    data = {}
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required']=HEARTBEAT

    try:
        proc = subprocess.Popen(TOPCOMMAND,stdout=subprocess.PIPE,close_fds=True,shell=True)
        top_output = proc.communicate()[0]
        for line in top_output.split('\n'):
           if not line:
               continue

           # Not interested in defunct processes
           if '<defunct>' in line:
               continue

           # Not interested in processes with slashes
           if '/' in line:
               continue

           # split the line so we have key => val
           line_raw = line.split(' ')

           # get the value
           value = line_raw[-2]

           # if hyphen, we not interested
           if '-' in value:
               continue

           # The processes we are interested in
           required_keys = ['php-cli', 'httpd', 'php', 'run-php', 'run-php-lock', 'redis-server', 'exim', 'aws', 'python', 'bash', 'cron', 'crond']

           # if the value is only 1, then also not interested (only tracking processes that have multiple)
           if (value > 1) and line_raw[-1] in required_keys:
               data[line_raw[-1]] = value

           # now make sure that any process we are interested have been included (even if none currently running)
           for key in required_keys:
               if key not in data:
                   data[key] = 0

    except Exception as exception:
        data['status']=0
        data['msg']='error while executing top command'

    return data


if __name__ == '__main__':

    print json.dumps(metricCollector(), indent=4, sort_keys=True)
