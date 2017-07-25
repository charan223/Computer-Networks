#!/usr/bin/env python

#from numpy import *
#import Gnuplot
import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink

class CustomTopo(Topo):
	"Create Custom topology"

	def build(self):
		# Initialize topology
		h1= self.addHost('h1')
		h2= self.addHost('h2')
		s1 = self.addSwitch('s1')
                s2 = self.addSwitch('s2')
		
		# self.addLink(s1,s2,bw=0.5, delay='1ms', loss=1)
		self.addLink(h1,s1,bw=3, delay='1ms', loss=1)
                self.addLink(s1,s2,bw=2, delay='100ms', loss=1)
		self.addLink(s2,h2,bw=3, delay='1ms', loss=2)

def TCPTest():
	"Test for a TCP network"
	t = CustomTopo()
	mn  = Mininet(link = TCLink, host = CPULimitedHost, topo = t)
	mn.start()
	print "TCP Test started"
	print(mn.hosts)
	host1, host2 = mn.get('h1','h2')
	host1.cmd('sudo tcpdump -n -i h1-eth0  > TCPfileh1.txt &')
	host2.cmd('sudo tcpdump -n -i h2-eth0 > TCPfileh2.txt &')
	mn.iperf((host1, host2))
	mn.stop()
	f = open("ResultTCP.txt", "w+")
	f1 = open("TCPfileh1.txt", "r")
	f2 = open("TCPfileh2.txt", "r")
	t1 = 0
	p1 = 0
	t2 = 0
	p2 = 0
	for line in f1:
		packet = line.split(' ')
		if len(packet)>2 and '10.0.0.1' in packet[2]:
			try:
				t1=t1+int(packet[-1])
				p1=p1+1
			except:
				pass

	for line in f2:
		packet = line.split(' ')
		if len(packet)>2 and '10.0.0.1' in packet[2]:
			try:
				t2=t2+int(packet[-1])
				p2=p2+1
			except:
				pass

        z0="Number"
        z1="packets_sent"
        z2="packets_received"
        z3="bytes_sent"
        z4="bytes_received"
        z5="TCPgoodput"
        z6="Packet_loss"
        print>>f, z0, z1, z2, z3, z4, z5, z6
	print>>f, '0', p1, p2, t1, t2 , float(t2)/t1 , p1-p2
	f1.close()
	f2.close()
	f.close()

def UDPTest():
	"Test for a UDP network"
	t = CustomTopo()
	mn  = Mininet(link = TCLink, host = CPULimitedHost, topo = t)
	mn.start()
	print "UDP Test started"
	print(mn.hosts)
	host1, host2 = mn.get('h1','h2')
        sw11,sw12 =mn.get('s1','s2')
        sw21,sw22 =mn.get('s1','s2')
	file = open("2/9/throughput.txt","w") #################################################################################
	Bandwidth = ['64' , '128' , '256', '512', '1024' ,'2048' ,'4096']
	for i,b in enumerate(Bandwidth):
		x = 'sudo tcpdump udp -n -i h1-eth0 > 2/9/UDPfile' + str(i+1) + 'h1.txt &'
		y = 'sudo tcpdump udp -n -i h2-eth0 > 2/9/UDPfile' + str(i+1) + 'h2.txt &'
                sx1= 'sudo tcpdump udp -n -i s1-eth1 > 2/9/UDPfile' + str(i+1) + 's11.txt &'
                sy1= 'sudo tcpdump udp -n -i s2-eth1 > 2/9/UDPfile' + str(i+1) + 's21.txt &'
                sx2= 'sudo tcpdump udp -n -i s1-eth2 > 2/9/UDPfile' + str(i+1) + 's12.txt &'
                sy2= 'sudo tcpdump udp -n -i s2-eth2 > 2/9/UDPfile' + str(i+1) + 's22.txt &'
		host1.cmd(x)
		host2.cmd(y)
                sw11.cmd(sx1)
                sw21.cmd(sy1)
                sw12.cmd(sx2)
                sw22.cmd(sy2)
		val = mn.iperf((host1, host2) , udpBw=b, l4Type = 'UDP')
		print>>file,val[0]," ",val[1]	# throughput udp in throughput.txt
		host1.cmd("kill %sudo")
		host2.cmd("kill %sudo")
                sw11.cmd("kill %sudo")
                sw21.cmd("kill %sudo")
                sw12.cmd("kill %sudo")
                sw22.cmd("kill %sudo")
	mn.stop()
	file.close()


        f=open("2/9/packlostswitches.txt", "w" )

        for i,b in enumerate(Bandwidth):
                bcb = open("2/9/UDPfile"+ str(i+1) +"h1.txt", "r")
		vcv = open("2/9/UDPfile"+ str(i+1) +"h2.txt", "r")
		f1 = open("2/9/UDPfile"+ str(i+1) +"s11.txt", "r")
		f2 = open("2/9/UDPfile"+ str(i+1) +"s12.txt", "r")
                f3 = open("2/9/UDPfile"+ str(i+1) +"s21.txt", "r")
		f4 = open("2/9/UDPfile"+ str(i+1) +"s22.txt", "r")
                

		p11 = 0
		p12 = 0
		p21 = 0
		p22 = 0
                z1=0
                z2=0
                for line in bcb:
                    z1=z1+1
                for line in vcv:
                    z2=z2+1

                for line in f1:
                    p11=p11+1
                for line in f2:
                    p12=p12+1
                for line in f3:
                    p21=p21+1
                for line in f4:
                    p22=p22+1
                print>>f, "\nUDP_Bandwidth : ", b ,"Kbps"
                print>>f ,"packets switch1-eth1 :" ,p11, "\npackets switch1-eth2 :",p12,"\nfractionpacketslost :",100*float(p11-p12)/p11
                print>>f ,"packets switch2-eth1 :" ,p21, "\npackets switch2-eth2 :",p22,"\nfractionpacketslost :",100*float(p21-p22)/p21
                print>>f ,"packets h1 :" ,z1, "\npackets h2 :",z2,"\nfractionpacketslost :",100*float(z1-z2)/z1
                #f.close()
                f1.close()
                f2.close()
                f3.close()
                f4.close()
                bcb.close()
                vcv.close()

        f.close()

	
	f = open("2/9/packetlossplot.txt", "w+")
        fu = open("2/9/normthruudplot.txt", "w+")
	for i,b in enumerate(Bandwidth):
		f1 = open("2/9/UDPfile"+ str(i+1) +"h1.txt", "r")
		f2 = open("2/9/UDPfile"+ str(i+1) +"h2.txt", "r")
		t1 = 0
		p1 = 0
		t2 = 0
		p2 = 0
		for line in f1:
			packet = line.split(' ')
			if len(packet)>2 and '10.0.0.1' in packet[2]:
				try:
					t1=t1+int(packet[-1])
					p1=p1+1
				except:
					pass

		for line in f2:
			packet = line.split(' ')
			if len(packet)>2 and '10.0.0.1' in packet[2]:
				try:
					t2=t2+int(packet[-1])
					p2=p2+1
				except:
					pass
		print>>f, b," ",p1-p2  # packet loss Result.txt
                print>>fu, b," ",float(t2)/t1 # normthruudp normthruputudp.txt
                 
		f1.close()
		f2.close()
	f.close()
	

def plotGraph():
	# ('64Kbps', '65.6 Kbits/sec')
	# Extract 64 and 65.6 from testfile and plot the graph using gnuplot
	# test is a temporay file created
	f = open("thruudpplot.txt","w+")
	x = open("throughput.txt", "r")
	for line in x:
		y = line.split(" ")
		#print>>f, y[1].split('K')[0], y[3].split()[0]
	        print>>f,y[0]," ",y[1]
        f.close()
	x.close()
	g = Gnuplot.Gnuplot()
	g.title('UDP throughput')
	g.xlabel('Bandwidth')
	g.ylabel('Throughput')
	g('set term png')
	g('set out "outputplot1thru.png"')
	databuff = Gnuplot.File("thruudpplot.txt", using='1:2',with_='line', title="UDP Throughput")
	g.plot(databuff)

        
        #f = open("packetlossplot.txt","w+")
        g = Gnuplot.Gnuplot()
	g.title('UDP PacketLoss')
	g.xlabel('Bandwidth')
	g.ylabel('PacketLoss')
	g('set term png')
	g('set out "outputplot1pl.png"')
	databuff = Gnuplot.File("packetlossplot.txt", using='1:2',with_='line', title="UDP PacketLoss")
	g.plot(databuff)
        #f.close()    
 

        #f = open("normthruudplot.txt","w+")
        g = Gnuplot.Gnuplot()
	g.title('UDP Normthroughput')
	g.xlabel('Bandwidth')
	g.ylabel('NormThroughput')
	g('set term png')
	g('set out "outputplot1normthru.png"')
	databuff = Gnuplot.File("normthruudplot.txt", using='1:2',with_='line', title="UDP NormThroughput")
	g.plot(databuff)
        #f.close()






if __name__ == '__main__':	
    #TCPTest()
    UDPTest()
    #plotGraph()
