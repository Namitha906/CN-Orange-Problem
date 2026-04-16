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
        dpid = event.connection.dpid
        in_port = event.port

        src = packet.src
        dst = packet.dst

        log.info("Switch %s: %s -> %s", dpid, src, dst)

        # Learn MAC address
        self.mac_to_port[src] = in_port

        # Forwarding logic
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
