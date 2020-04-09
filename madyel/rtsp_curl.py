import pycurl
from scanf import scanf
import random
import os.path
import time
from pathlib import Path
import subprocess

DEBUG = True
TRANSPORT_TCP_OR_UDP = True

PORT_F = random.randint(49152, 65534)
PORT_T = PORT_F + 1

FILENAME_SDP=str(Path(__file__).resolve().parent)+"/file_tmp.sdp"

USER_AGENT='MadYel RTSP'

if TRANSPORT_TCP_OR_UDP:
    # UDP #
    transport = "RTP/AVP;unicast;client_port={}-{}".format(PORT_F, PORT_T)
else:
    transport = "RTSP;unicast;client_port={}-{}".format(PORT_F, PORT_T)

class Storage:
    def __init__(self):
        self.contents = ''
        self.line = 0

    def store(self, buf):
        self.line = self.line + 1
        self.contents = "%s%i: %s" % (self.contents, self.line, buf.decode())

    def __str__(self):
        return self.contents

class file_sdp(object):
    def __init__(self, name, type):
        self.name=name
        self.type=type
    def get_file_sdp(self):
        self.file_sdp = open(self.name, self.type)
        return self.file_sdp

class Rtsp_Curl(object):
    def __init__(self):
        pass
    def init(self, url, user_pwd):
        self.curl = pycurl.Curl()
        self.url = url
        self.user_pwd = user_pwd
        self.transport = transport
        if DEBUG:
            self.curl.setopt(pycurl.VERBOSE, 1)
            self.curl.setopt(pycurl.NOPROGRESS, 1)
        self.curl.setopt(pycurl.USERAGENT, USER_AGENT)
        self.curl.setopt(pycurl.TCP_NODELAY, 0)
        self.curl.setopt(pycurl.URL, self.url)
        self.curl.setopt(pycurl.OPT_RTSP_STREAM_URI, self.url)

    def auth(self):
        self.curl.setopt(pycurl.USERPWD, self.user_pwd)
        self.curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_DIGEST)
        self.curl.perform()


    def rtsp_describe(self):
        retrieved_body = Storage()
        retrieved_headers = Storage()
        self.filename_sdp = file_sdp(FILENAME_SDP, "w+").get_file_sdp()
        self.curl.setopt(pycurl.WRITEFUNCTION, self.get_sdp_filename)
        self.curl.setopt(pycurl.OPT_RTSP_REQUEST, pycurl.RTSPREQ_DESCRIBE)
        #self.curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.store)
        #self.curl.setopt(pycurl.HEADERFUNCTION, retrieved_headers.store)
        self.curl.perform()
        #print(retrieved_body)
        #print(retrieved_headers)


    def rtsp_options(self):
        self.curl.setopt(pycurl.OPT_RTSP_REQUEST, pycurl.RTSPREQ_OPTIONS)
        self.curl.perform()


    def rtsp_setup(self, control):
        uri = self.url + '/%s' % control
        retrieved_body = Storage()
        retrieved_headers = Storage()
        self.curl.setopt(pycurl.OPT_RTSP_STREAM_URI, uri)
        self.curl.setopt(pycurl.OPT_RTSP_REQUEST, pycurl.RTSPREQ_SETUP)
        self.curl.setopt(pycurl.OPT_RTSP_TRANSPORT, self.transport)
        self.curl.setopt(pycurl.WRITEFUNCTION, retrieved_body.store)
        self.curl.setopt(pycurl.HEADERFUNCTION, retrieved_headers.store)
        self.curl.perform()
        #print(retrieved_body)
        #print(retrieved_headers)


    def rtsp_play(self, url):
        self.curl.setopt(pycurl.OPT_RTSP_STREAM_URI, url)
        self.curl.setopt(pycurl.RANGE, 'npt=0.000-')
        self.curl.setopt(pycurl.OPT_RTSP_REQUEST, pycurl.RTSPREQ_PLAY)
        self.curl.perform()


    def rtsp_teardown(self):
        self.curl.setopt(pycurl.OPT_RTSP_REQUEST, pycurl.RTSPREQ_TEARDOWN)
        self.curl.perform()

    def rtsp_curl_close(self):
        self.curl.close()

    def get_media_control_attribute(self):
        while not os.path.exists(FILENAME_SDP):
            time.sleep(1)
        if os.path.isfile(FILENAME_SDP):
            tuple_control = ()
            self.filename_sdp = file_sdp(FILENAME_SDP, "r").get_file_sdp()
            for x in self.filename_sdp:
                control = scanf('a=control:%s', x)
                if control is not None:
                    tuple_control = tuple_control + control
            self.filename_sdp.close()
            return tuple_control[1]
        else:
            raise ValueError("%s isn't a file!" % FILENAME_SDP)


    def get_sdp_filename(self,sdp_filename):
        # print(sdp_filename.decode("utf-8"))
        self.filename_sdp.write(sdp_filename.decode("utf-8"))
        self.filename_sdp.close()

if __name__ == '__main__':
    url = 'rtsp://10.10.100.180:554/test.mp4&t=unicast&p=udp&ve=H264&w=1920&h=1080&ae=PCMU&sr=8000'
    rtsp=Rtsp_Curl()
    rtsp.init(url,'admin:admin')
    rtsp.rtsp_options()
    rtsp.auth()
    rtsp.rtsp_describe()
    control = rtsp.get_media_control_attribute()
    rtsp.rtsp_setup(control)
    rtsp.rtsp_play(url)
    print(PORT_F)
    time.sleep(60)
    #subprocess.call('ffplay -i ' + FILENAME_SDP)
    rtsp.rtsp_teardown()
    rtsp.rtsp_curl_close()