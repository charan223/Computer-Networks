"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        Switch = self.addSwitch( 's1' )
   

        # Add links
        self.addLink( leftHost, Switch ,bw=1,delay=1,loss=1 )
        self.addLink( Switch, rightHost ,bw=1,delay=1,loss=2 )
        


topos = { 'mytopo': ( lambda: MyTopo() ) }
