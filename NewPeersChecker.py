__author__ = 'alexisgallepe'

import time
import Peer
from threading import Thread
from pubsub import pub


class NewPeersChecker(Thread):
    def __init__(self, tracker, torrent):
        Thread.__init__(self)
        self.tracker = tracker
        self.torrent = torrent
        self.peerFailed = [("","")]

    def run(self):

        while True:
            # if peerConnected == 50 sleep 50 secondes
            peers = self.tracker.getPeersFromTrackers()
            for peer in peers:
                if not (peer[0],peer[1]) in self.peerFailed:
                    #self.peerList.append((peer[0],peer[1]))
                    p = Peer.Peer(self.torrent,peer[0],peer[1])
                    if not p.connectToPeer(3):
                        self.peerFailed.append((peer[0],peer[1]))
                        # be careful, must empty list sometimes
                    else:
                        pub.sendMessage('newPeer',peer=p)

            print self.peerFailed
            time.sleep(10000)