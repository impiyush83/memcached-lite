
#!/bin/sh

touch memcache.csv && python3 server/server_impl.py $1
