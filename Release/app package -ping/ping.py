#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: aribn
# 2018-02-02
# ping for Windows

import os
import sys
import socket
import struct
import select
import time
import ctypes
import threading
import queue

PostMessage=ctypes.windll.user32.PostMessageW
class CPing(object):
    "CPing(n_sender=1,callback=None,hwnd=0,msg=0)"
    def __init__(self,n_sender=1,callback=None,hwnd=0,msg=0):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        self._id = os.getpid() & 0xFFFF
        self._tasks=queue.Queue()
        self._callback=callback
        self._wnd=hwnd
        self._msg=msg
        self._thd_rcv=threading.Thread(target=lambda:self._recv_fun())
        self._thd_rcv.start()
        self._thd_snd=[threading.Thread(target=lambda:self._send_routine()) for x in range(n_sender)]
        for x in self._thd_snd:
            x.start()

    def send_ping(self,ip):
        self._tasks.put(ip)

    def _send_routine(self):
        while 1:
            ip=self._tasks.get()
            try:
                ip = socket.gethostbyname(ip)
                # Header is type (8), code (8), checksum (16), id (16), sequence (16)
                my_checksum = 0
                # Make a dummy heder with a 0 checksum
                # struct.pack(fmt, v1, v2, ...)
                # Return a string containing the values v1, v2, ... packed
                # according to the given format.
                # b:signed char, h:short 2, H:unsigned short 2
                header = struct.pack('bbHHh', 8, 0, my_checksum, self._id, 1)
                # struct.calcsize(fmt)
                # Return the size of the struct corresponding to the given format.
                byte_in_double = struct.calcsize("d") # C type: double
                data = (192 - byte_in_double) * b"P" # any char is OK, any length is OK
                data = struct.pack("d", time.clock()) + data

                # Calculate the checksum on the data and the dummy header.
                my_checksum = self._get_checksum(header + data)

                # It's just easier to make up a new header than to stuff it into the dummy.
                # socket.htons(x)
                # Convert 16-bit positive integers from host to network byte order.
                header = struct.pack("bbHHh", 8, 0, socket.htons(my_checksum), self._id, 1)
                packet = header + data
                # self._socket.sendto(packet, (ip, 1)) # getsockaddrarg() takes exactly 2 arguments
                self._socket.sendto(packet, (ip,0)) # it seems that 0~65535 is OK (port?)
            except:
                pass

    def _recv_fun(self):
        while True:
            select.select([self._socket], [], [])
            rec_packet, addr = self._socket.recvfrom(1024)
            icmp_header = rec_packet[20 : 28]
            ip_type, code, checksum, packet_ID, sequence = struct.unpack("bbHHh", icmp_header)
            if ip_type != 8 and packet_ID == self._id: # ip_type should be 0
                byte_in_double = struct.calcsize("d")
                time_sent = struct.unpack("d", rec_packet[28 : 28 + byte_in_double])[0]
                if self._callback:
                    self._callback((addr[0],time.clock() - time_sent))
                if self._wnd:
                    PostMessage(self._wnd,self._msg,0,0)




    def _get_checksum(self,source):
        """
        return the checksum of source
        the sum of 16-bit binary one's complement
        """
        checksum = 0
        count = (len(source) / 2) * 2
        i = 0
        while i < count:
            temp = (source[i + 1]) * 256 + (source[i]) # 256 = 2^8
            checksum = checksum + temp
            checksum = checksum & 0xffffffff # 4,294,967,296 (2^32)
            i = i + 2

        if i < len(source):
            checksum = checksum + ord(source[len(source) - 1])
            checksum = checksum & 0xffffffff

        # 32-bit to 16-bit
        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum = checksum + (checksum >> 16)
        answer = ~checksum
        answer = answer & 0xffff

        # why? ans[9:16 1:8]
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer

    def __del__(self):
        self._thd_rcv._stop()
        self._socket.close()


#ping=CPing(5,lambda x:print(x),0,0)
#ips=['1.1.1.'+str(x) for x in range(10)]+['127.0.0.'+str(x) for x in range(10)]
#for x in ips:
#    ping.send_ping(x)
#    print(x)
