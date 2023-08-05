# coding=utf-8

"""
    A collection of utility function for use with Scapy module.

    ~ CodesWhite (aka WhiteCode) @ 2017
"""

from time import sleep
from typing import Optional

from scapy.sendrecv import sendp, srp, conf  # Try to load scapy
# from scapy.layers.l2 import Ether, ARP, get_if_hwaddr, get_if_addr
from scapy.layers import l2


def unpack_iface(iface: str) -> tuple:
    """ Return tuple(IP: str, MAC: str) """
    return l2.get_if_addr(iface), l2.get_if_hwaddr(iface)


def get_gw() -> tuple:
    """ Return tuple(gateway_IP: IPv4Addreess, gateway_MAC: str) """
    gw_ip, iface = [
        x for x in conf.route.routes if x[2] != '0.0.0.0'][0][2:4]
    resp = arp_request(unpack_iface(iface), gw_ip)
    if not resp:
        raise TimeoutError('No ARP response received from supposed gateway!')
    return gw_ip, resp


def arp_response(src: str, src_mac: str, dst: str, dst_mac: str, count=3, interval=0.1) -> None:
    """ Sends an ARP response """
    for i in range(count):
        sendp(l2.Ether(dst=dst_mac, src=src_mac) /
              l2.ARP(op="is-at", hwsrc=src_mac,
                     psrc=src, hwdst=dst_mac, pdst=dst),
              verbose=False)
        if interval > 0:
            sleep(interval)


def arp_request(unpacked_iface: tuple, dst: str, retry=2, timeout=1) -> Optional[str]:
    """ Sends an ARP request and attempts to return target's MAC address """
    local_ip, local_mac = unpacked_iface
    rsp = srp(l2.Ether(dst='ff:ff:ff:ff:ff:ff', src=local_mac) /
              l2.ARP(hwsrc=local_mac, psrc=local_ip,
                     hwdst='ff:ff:ff:ff:ff:ff', pdst=dst),
              timeout=timeout, retry=retry, verbose=False)
    if not rsp[0]:
        return
    return rsp[0][0][1]['ARP'].hwsrc
