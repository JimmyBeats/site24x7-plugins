#!/usr/bin/python

import json
import platform
import subprocess

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "3"

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
            if '<defunct>' in line:
                continue
            line_raw = line.split(' ')
            data[line_raw[-1]] = line_raw[-2]
    except Exception as exception:
        data['status']=0
        data['msg']='error while executing top command'

    return data


if __name__ == '__main__':

    print json.dumps(metricCollector(), indent=4, sort_keys=True)
