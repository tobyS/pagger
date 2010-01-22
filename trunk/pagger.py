#!/usr/bin/env python

import sys

sys.path.append('./src')

# import lastfm.service
# import lastfm.artist
# import lastfm.track
# 
# service = lastfm.service.Service('682587831457dcf13f569c79b930d866')
# artist = lastfm.artist.Artist(service, '2 Unlimited')
# track = lastfm.track.Track(service, artist, 'Get ready for this')
# for tag in track.get_top_tags():
# 	print(tag.__dict__)

from program.main import Main

main = Main()
main.run()
