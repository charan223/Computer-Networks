
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.openflow.libopenflow_01 import *
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.packet import ethernet
from pox.lib.packet.ethernet import ETHER_ANY, ETHER_BROADCAST
from pox.lib.packet import arp, ipv4, icmp
from pox.lib.packet.icmp import TYPE_ECHO_REQUEST, TYPE_ECHO_REPLY,\
                                 TYPE_DEST_UNREACH, CODE_UNREACH_NET, CODE_UNREACH_HOST
from pox.lib.util import dpidToStr
from pox.lib.util import str_to_bool
import time
import l2


log = core.getLogger()

def get_log():
    return log


arpTable = {}

portTable = {}


rDST_NETWORK = 0
rNEXTHOP_IP = 1
rNEXTHOP_PORT_NAME = 2
rNEXTHOP_PORT_IP = 3
rNEXTHOP_PORT = 4


pPORT = 0
pPORT_MAC = 1
pPORT_IP = 2



class routerConnection(object):

  def __init__(self,connection):
    dpid = connection.dpid
    log.debug('-' * 50 + "dpid=" + str(dpid) + '-' * 50)
    log.debug('-' * 50 + "I\'m a StaticRouter" + '-' * 50)

    
    arpTable[dpid] = {}
    
    portTable[dpid] = []

   
    for entry in connection.ports.values():
      port = entry.port_no
      mac = entry.hw_addr
      
      if port <= of.ofp_port_rev_map['OFPP_MAX']:
        arpTable[dpid][port] = {}
        if port == 1:
          ip = IPAddr('172.16.0.1')
          arpTable[dpid][port][ip] = mac
          portTable[dpid].append([port, mac, ip])
        elif port == 2:
          ip = IPAddr('192.168.1.1')
          arpTable[dpid][port][ip] = mac
          portTable[dpid].append([port, mac, ip])
        elif port == 3:
          ip = IPAddr('10.2.0.1')
          arpTable[dpid][port][ip] = mac
          portTable[dpid].append([port, mac, ip])
        
    
    log.debug('-'*50 + 'arpTable' + '-'*50)
    log.debug(arpTable)

    
    log.debug('-'*50 + 'portTable' + '-'*50)
    log.debug(portTable)

    
    self.routeTable = []
    self.routeTable.append(['10.2.0.0/24',
                            '10.2.0.2', 'r1-eth3', '10.2.0.1', 3])
    self.routeTable.append(['192.168.1.0/24',
                            '192.168.1.2', 'r1-eth2', '192.168.1.1', 2])
    self.routeTable.append(['172.16.0.0/24',
                            '172.16.0.2', 'r1-eth1', '172.16.0.1', 1])

    self.connection = connection
    connection.addListeners(self)

  
  def _handle_FlowRemoved(self,event):
    dpid = event.connection.dpid
    log.debug('-' * 50 + "dpid=" + str(dpid) + '-' * 50)
    log.debug('A FlowRemoved Message Recieved')
    log.debug('---A flow has been removed')

  
  def _handle_PacketIn(self,event):
    dpid = self.connection.dpid
    log.debug('-' * 50 + "dpid=" + str(dpid) + '-' * 50)
    log.debug("A PacketIn Message Recieved")
    packet = event.parsed

    # arp
    if packet.type == ethernet.ARP_TYPE:
      log.debug('---It\'s an arp packet')
      arppacket = packet.payload
    
      if arppacket.opcode == arp.REPLY:
        arpTable[self.connection.dpid][event.ofp.in_port][arppacket.protosrc] = arppacket.hwsrc
        arpTable[self.connection.dpid][event.ofp.in_port][arppacket.protodst] = arppacket.hwdst
        
        log.debug('------arpTable learned form arp Reply srt and dst')
        log.debug('------' + str(arpTable))
     
      if arppacket.opcode == arp.REQUEST:
        log.debug('------Arp request')
        log.debug('------' + arppacket._to_str())
        arpTable[self.connection.dpid][event.ofp.in_port][arppacket.protosrc] = arppacket.hwsrc
        
        log.debug('------arpTable learned form arp Request srt')
        log.debug('------' + str(arpTable))

        
        if arppacket.protodst in arpTable[self.connection.dpid][event.ofp.in_port]:
          log.debug('------I know that ip %s,send reply'%arppacket.protodst)

          
          a = arppacket
          r = arp()
          r.hwtype = a.hwtype
          r.prototype = a.prototype
          r.hwlen = a.hwlen
          r.protolen = a.protolen
          r.opcode = arp.REPLY
          r.hwdst = a.hwsrc
          r.protodst = a.protosrc
          r.protosrc = a.protodst
          r.hwsrc = arpTable[self.connection.dpid][event.ofp.in_port][arppacket.protodst]
          e = ethernet(type=packet.type, src=r.hwsrc,dst=a.hwsrc)
          e.set_payload(r)
          msg = of.ofp_packet_out()
          msg.data = e.pack()
          msg.actions.append(of.ofp_action_output(port=event.ofp.in_port))
          self.connection.send(msg)

    
    if packet.type == ethernet.IP_TYPE:
      log.debug('---It\'s an ip packet')
      ippacket = packet.payload
      
      dstip = ippacket.dstip
      log.debug(str(dstip))
      
      for t in portTable[dpid]:
        selfip = t[pPORT_IP]
        
        if dstip == selfip:
          
          if ippacket.protocol == ipv4.ICMP_PROTOCOL:
            log.debug('!!!!!!!!!!An icmp for me!!!!!!!!!!!')
            icmppacket = ippacket.payload
           
            if icmppacket.type == TYPE_ECHO_REQUEST:
              selfmac = t[pPORT_MAC]
              log.debug('!!!!!!!!!!An icmp echo request for me!!!!!!!!!!!')

              
              r = icmppacket
              r.type = TYPE_ECHO_REPLY

              
              s = ipv4()
              s.protocol = ipv4.ICMP_PROTOCOL
              s.srcip = selfip
              s.dstip = ippacket.srcip
              s.payload = r

              
              e = ethernet()
              e.type = ethernet.IP_TYPE
              e.src = selfmac
              e.dst = packet.src
              e.payload = s

              
              msg = of.ofp_packet_out()
              msg.data = e.pack()
              msg.actions.append(of.ofp_action_output(port=event.port))
              self.connection.send(msg)
              log.debug('!!!!!!!!!!Reply it!!!!!!!!!!!')
              return
            else:
              
              return
          
          else:
            
            return

      
      for t in self.routeTable:
        
        dstnetwork = t[rDST_NETWORK]
        
        if dstip.inNetwork(dstnetwork):
          log.debug('------ip dst %s is in the routeTable' % dstip)

         
          nh_port = t[rNEXTHOP_PORT]
          log.debug(str(nh_port)+' '+str(event.ofp.in_port))
          if nh_port == event.ofp.in_port:
            return

          nh_ip = IPAddr(t[rNEXTHOP_IP])
          
          if nh_ip == IPAddr('0.0.0.0'):
            nh_ip = dstip
          nh_port_ip = IPAddr(t[rNEXTHOP_PORT_IP])

          
          nh_mac_src = arpTable[dpid][nh_port][nh_port_ip]

          
          if nh_ip in arpTable[dpid][nh_port]:
            log.debug('------I know the next dst %s mac' % nh_ip)
            nh_mac_dst = arpTable[dpid][nh_port][nh_ip]

            
            msg1 = of.ofp_flow_mod()
          
            msg1.match = of.ofp_match()
            msg1.match.dl_type = ethernet.IP_TYPE
            msg1.match.nw_dst = dstip
           
            msg1.command = 0
            msg1.idle_timeout = 10
            msg1.hard_timeout = 30
            msg1.buffer_id = event.ofp.buffer_id
            msg1.flags = 3  # of.ofp_flow_mod_flags_rev_map('OFPFF_CHECK_OVERLAP') | of.ofp_flow_mod_flags_rev_map('OFPFF_CHECK_OVERLAP')
            msg1.actions.append(of.ofp_action_dl_addr.set_src(nh_mac_src))
            msg1.actions.append(of.ofp_action_dl_addr.set_dst(nh_mac_dst))
            msg1.actions.append(of.ofp_action_output(port=nh_port))
            self.connection.send(msg1)
            log.debug('###Add a flow###')

          
          else:
            log.debug('------I don\'t know the next dst %s mac,make an arp request' % IPAddr(t[rNEXTHOP_IP]))
            
            r = arp()
            r.opcode = arp.REQUEST
            r.protosrc = nh_port_ip
            r.hwsrc = nh_mac_src
            r.protodst = nh_ip
            e_arp = ethernet(type=ethernet.ARP_TYPE, src=r.hwsrc, dst=ETHER_BROADCAST)
            e_arp.set_payload(r)
            msg = of.ofp_packet_out()
            msg.data = e_arp.pack()
            msg.actions.append(of.ofp_action_output(port=nh_port))
            msg.in_port = event.ofp.in_port
            event.connection.send(msg)

            
            nh_mac_dst = ETHER_BROADCAST
            msg1 = of.ofp_packet_out()
            msg1.in_port = event.port
            msg1.buffer_id = event.ofp.buffer_id
            msg1.actions.append(of.ofp_action_dl_addr.set_src(nh_mac_src))
            msg1.actions.append(of.ofp_action_dl_addr.set_dst(nh_mac_dst))
            msg1.actions.append(of.ofp_action_output(port=nh_port))
            self.connection.send(msg1)

          return

     
      r = icmp()
      r.type = TYPE_DEST_UNREACH
      r.code = CODE_UNREACH_NET
      d = ippacket.pack()[:ippacket.iplen + 8]
      import struct
      d = struct.pack("!I", 0) + d  
      r.payload = d
      s = ipv4()
      s.protocol = ipv4.ICMP_PROTOCOL
      for t in portTable[dpid]:
        selfip = t[pPORT_IP]
        if(event.port == t[pPORT]):
          s.srcip = selfip
          break
      s.dstip = ippacket.srcip
      s.payload = r
      e = ethernet()
      e.type = ethernet.IP_TYPE
      e.src = packet.dst
      e.dst = packet.src
      e.payload = s

      
      msg = of.ofp_packet_out()
      msg.data = e.pack()
      msg.actions.append(of.ofp_action_output(port=event.port))
      self.connection.send(msg)


class MyHubComponent(object):
  def __init__(self):
    core.openflow.addListeners(self)

  def _handle_ConnectionUp(self,event):
    dpid = event.connection.dpid
    log.debug('-' * 45 + "A Switch ConnectionUp!"+dpidToStr(dpid) + '-' * 50)
    if dpid == 1:
      log.debug('yeh router hai '+dpidToStr(dpid))
      routerConnection(event.connection)
    else:
      l2.l2_switch(event.connection,str_to_bool(False))

  def _handle_ConnectionDown(self,event):
    dpid = event.connection.dpid
    
    try:
      arpTable.pop(dpid)
      log.debug('Remove a arpTable of dpid %s' % dpid)
      portTable.pop(dpid)
      log.debug('Remove a portTable of dpid %s' % dpid)
    except:
      pass

def launch(hold_down=l2.get_fdelay()):
  try:

    l2.set_fdelay(int(str(hold_down), 10))  
    assert l2.get_fdelay() >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")
  core.registerNew(MyHubComponent)













