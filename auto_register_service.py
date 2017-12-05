#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Auto register a service through route 53 in AWS

from __future__ import absolute_import, print_function

from time import sleep
from contextlib import closing
import socket
import boto
import requests
import os

def setup_dns(ip_address,domain_name):
    """Entrypoint."""
    r53 = boto.connect_route53(AWS_ACCESS_KEY,AWS_SECRET_KEY)
    zones = r53.get_all_hosted_zones()['ListHostedZonesResponse']['HostedZones']
    private_zone = find_private_zone(domain_name+".", zones)
    #reverse_zone = find_private_zone('100.10.in-addr.arpa.', zones)
    server_name=""
    #We will not go beyond 100, in case we reach 100 we will overrite the dns record
    for counter in xrange(1,101):
        server_name=SERVICE_NAME+str(counter)
        if health_check(server_name+"."+domain_name,HEALTH_CHECK_PORT) == False:
            break
    if private_zone != None:
    	delete_record(r53, private_zone,server_name+"."+domain_name+".", 'A', wait=True)
    upsert_record(r53, private_zone, server_name+"."+domain_name+".", ip_address, 'A', wait=True)


def find_private_zone(name, zones):
    for zone in zones:
        if zone.get('Name') == name and zone.get('Config', {}).get('PrivateZone') in [True, 'true']:
            return zone

    return None


def find_record(r53, zone_id, name, record_type):
    records = r53.get_all_rrsets(zone_id)

    for record in records:
        if record.name == name and record.type == record_type:
            return record

    return None


def upsert_record(r53, zone, name, record, record_type, ttl=60, wait=False):
    print("Inserting record {}[{}] -> {}; TTL={}".format(name, record_type, record, ttl))
    recordset = boto.route53.record.ResourceRecordSets(connection=r53, hosted_zone_id=zone.get('Id').split('/')[-1])
    recordset.add_change_record('UPSERT', boto.route53.record.Record(
        name=name,
        type=record_type,
        resource_records=[record],
        ttl=ttl
    ))
    changeset = recordset.commit()

    change_id = changeset['ChangeResourceRecordSetsResponse']['ChangeInfo']['Id'].split('/')[-1]

    while wait:
        status = r53.get_change(change_id)['GetChangeResponse']['ChangeInfo']['Status']
        if status == 'INSYNC':
            break

        sleep(10)

def delete_record(r53, zone, name, record_type, wait=False):
    print("Deleting record {}[{}] -> {}".format(name, record_type, name))

    zone_id = zone.get('Id').split('/')[-1]
    record = find_record(r53, zone_id, name, record_type)

    if not record:
        print("No record exists.")
        return

    recordset = boto.route53.record.ResourceRecordSets(connection=r53, hosted_zone_id=zone.get('Id').split('/')[-1])
    recordset.add_change_record('DELETE', record)
    changeset = recordset.commit()

    change_id = changeset['ChangeResourceRecordSetsResponse']['ChangeInfo']['Id'].split('/')[-1]

    while wait:
        status = r53.get_change(change_id)['GetChangeResponse']['ChangeInfo']['Status']
        if status == 'INSYNC':
            break

        sleep(10)


def health_check(host,port):
    try:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(2) #2 second timeout
            if sock.connect_ex((host, port)) == 0:
                return True
            else:
                return False
    except:
        return False

def get_env(key,default_value=""):
    value = os.environ.get(key);
    if value:
        return value
    return default_value


AWS_ACCESS_KEY = get_env('AWS_ACCESS_KEY')
AWS_SECRET_KEY = get_env('AWS_SECRET_KEY')
SERVICE_NAME = get_env('SERVICE_NAME')
HEALTH_CHECK_PORT = get_env('HEALTH_CHECK_PORT')
DOMAIN_NAME = get_env('DOMAIN_NAME')

if __name__ == "__main__":
    meta_data=requests.get("http://169.254.169.254/latest/meta-data/local-ipv4")
    setup_dns(meta_data.text,DOMAIN_NAME)
