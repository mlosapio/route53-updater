#!/usr/bin/env python

import boto.route53
import urllib2
import socket

####################################
# Crude script to update Route53 DNS
# consider it a poor-mans dyndns
####################################

AWSKEY = 
AWSSECRET = 
HOSTNAME = 'mtbethelfirehouse'
DOMAIN = 'warrenfire.org'
REGION = 'us-east-1'
IPWEBSITE = 'http://eth0.me'

existing = socket.gethostbyname(HOSTNAME + '.' + DOMAIN)

response = urllib2.urlopen(IPWEBSITE)
page = response.read().strip('\n')

if page != existing:
    print "%s not equal to %s" % (page, existing)
    conn = boto.route53.connection.Route53Connection(aws_access_key_id=AWSKEY, \
                                                     aws_secret_access_key=AWSSECRET)
    zone = conn.get_zone(DOMAIN)
    change = boto.route53.record.ResourceRecordSets(conn, zone.id)

    FQDN = HOSTNAME + '.' + DOMAIN
    change.add_change_record("UPSERT", 
           boto.route53.record.Record(name = FQDN, 
                                      type="A",
                                      resource_records=[page]))
    change.commit()
    print "IP address has been updated %s.%s is recorded as %s" % (HOSTNAME, DOMAIN, page)
else:
    print "All systems OK %s.%s is recorded as %s" % (HOSTNAME, DOMAIN, page)
