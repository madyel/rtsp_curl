#### Convert rtsp.c to rtsp_curl.py 
![](https://travis-ci.org/madyel/rtsp_curl.svg?branch=master) ![](https://img.shields.io/github/license/madyel/rtsp_curl.svg) ![](https://img.shields.io/github/last-commit/madyel/rtsp_curl.svg)

A basic RTSP transfer [rtsp.c][1]

---

Example:


```
import time
from madyel import Rtsp_Curl

stream_uri = 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'
rtsp = Rtsp_Curl()
rtsp.init(stream_uri, 'username:password')
rtsp.auth()
rtsp.rtsp_describe()
control = rtsp.get_media_control_attribute()
rtsp.rtsp_setup(control)
rtsp.rtsp_play(stream_uri)

time.sleep(5)

rtsp.rtsp_teardown()
rtsp.rtsp_curl_close()

```

##### Install_requires

```
pip install scanf 
pip install pycurl
```
<em>for macOS</em>:
```
PYCURL_SSL_LIBRARY=openssl LDFLAGS="-L/usr/local/opt/openssl/lib" CPPFLAGS="-I/usr/local/opt/openssl/include" pip install --no-cache-dir pycurl
```

```
/\
||_____-----_____-----_____
||   O                  O  \
||    O\\    ___    //O    /
||       \\ /   \//        \
||         |_O O_|         /
||          ^ | ^          \
||        // UUU \\        /
||    O//            \\O   \
||   O                  O  /
||_____-----_____-----_____\
||
||.           

```

[1]: [https://curl.haxx.se/libcurl/c/rtsp.html]