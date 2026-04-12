from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

mac_to_port={}

def _handle_PacketIn(event):
	packet=event.parsed
	dpid=event.connection.dpid
	in_port=event.port

	if dpid not in mac_to_port:
		mac_to_port[dpid]={}

	src=packet.src
	dst=packet.dst

	mac_to_port[dpid][src]=in_port     #Learn MAC address
	if dst in mac_to_port[dpid]:
		out_port=mac_to_port[dpid][dst]
	else:
		out_port=of.OFPP_FLOOD

	action=of.ofp_action_output(port=out_port)

	if out_port!=of.OFPP_FLOOD:
		msg=of.ofp_flow_mod()
		msg.match.in_port=in_port
		msg.match.dl_dst=dst
		msg.actions.append(action)
		event.connection.send(msg)

	msg=of.ofp_packet_out()
	msg.data=event.ofp
	msg.actions.append(action)
	msg.in_port=in_port
	event.connection.send(msg)

def launch():
	core.openflow.addListenerByName("PacketIn",_handle_PacketIn)
	log.info("Learning Switch Running....")

