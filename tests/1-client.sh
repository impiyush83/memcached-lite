#!/bin/sh

touch memcache_test.csv && python3 server/server-impl.py 6969
python3 client/client-impl.py 6969
