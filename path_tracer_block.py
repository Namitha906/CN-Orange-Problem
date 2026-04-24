from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class PathTracer(object):
    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}

        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port

        # Learn MAC address
        src = packet.src
        dst = packet.dst
        self.mac_to_port[src] = in_port

        dpid = self.connection.dpid
        log.info("Switch %s: %s -> %s", dpid, src, dst)

        # 🔴 BLOCK SCENARIO
        if packet.find('ipv4'):
            ip_packet = packet.find('ipv4')

            if str(ip_packet.dstip) == "10.0.0.2":
                log.warning("Blocking traffic to %s", ip_packet.dstip)

                msg = of.ofp_flow_mod()
                msg.match.dl_type = 0x0800   # IPv4
                msg.match.nw_dst = ip_packet.dstip
                msg.idle_timeout = 30
                msg.hard_timeout = 60

                self.connection.send(msg)
                return

        # Forwarding logic (learning switch)
        if dst in self.mac_to_port:
            out_port = self.mac_to_port[dst]
        else:
            out_port = of.OFPP_FLOOD

        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        self.connection.send(msg)


def launch():
    def start_switch(event):
        log.info("Controlling switch %s", event.connection.dpid)
        PathTracer(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
