#!/usr/bin/python
# -*- coding: utf-8 -*-


torrentServer = '221.150.182.23'
torrentPort = 9091
torrentUser = 'admin'
torrentPassword = 'lgtwins'

tc = transmissionrpc.Client(torrentServer, torrentPort, torrentUser, torrentPassword)
torrents = tc.get_torrents()
for torrent in torrents:
        if (torrent.status == 'seeding'):
                print torrent.id
                print torrent.date_added
                print torrent.status
                print torrent.isFinished
                print torrent.name
                print torrent.percentDone
                tc.remove_torrent(torrent.id)

f = open("./x.torrent", 'r')
data = b64encode(f.read())
tc.add_torrent(data)
f.close()
