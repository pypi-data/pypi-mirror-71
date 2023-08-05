# simplelanscan

Run a simple arp scan of the network and push the results to ElasticSearch.


```
pip install simplelanscan
```



## Systemd Hack
cp /usr/local/lib/python3.7/dist-packages/scan_lan_clients.service /etc/systemd/system/.
cp /usr/local/lib/python3.7/dist-packages/simplelanscan/config.ini to /usr/local/bin/config.ini
cp /usr/local/lib/python3.7/dist-packages/simplelanscan/index.json to /usr/local/bin/index.json