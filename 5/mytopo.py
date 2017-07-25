
from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h1 = self.addHost( 'h1', ip = "172.16.0.2/24", defaultRoute = "via 172.16.0.1" )
        h2 = self.addHost( 'h2', ip = "192.168.1.2/24", defaultRoute = "via 192.168.1.1" )
        h3 = self.addHost( 'h3', ip = "10.2.0.2/24", defaultRoute = "via 10.2.0.1" )
       
        

        r1 = self.addSwitch( 'r1' )

        s1 = self.addSwitch( 's2' )
        
        s2 = self.addSwitch( 's3' )
        s3 = self.addSwitch( 's4' )
        s4 = self.addSwitch( 's5' )
        s5 = self.addSwitch( 's6' )
        s6 = self.addSwitch( 's7' )
        

        s7 = self.addSwitch( 's8' )
        s8 = self.addSwitch( 's9' )

        self.addLink(h1,s1)

        
        
        self.addLink(s1,s2)
        self.addLink(s1,s3)
        self.addLink(s2,s3)
        self.addLink(s2,s4)
        self.addLink(s3,s5)
        self.addLink(s4,s5)
        self.addLink(s4,s6)
        self.addLink(s5,s6)
        
        

        self.addLink(s6,r1)
        self.addLink(h2,s7)
        self.addLink(s7,r1)


        self.addLink(r1,s8)
        self.addLink(s8,h3)


topos = { 'mytopo': ( lambda: MyTopo() ) }
