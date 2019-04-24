#### Convert rtsp.c to rtsp_curl.py

A basic RTSP transfer [rtsp.c][1]

---

Example:

```

stream_uri = 'rtsp://127.0.0.1:554/video.mp4'
rtsp = Rtsp_Curl()
rtsp.init(stream_uri, 'username:password')
rtsp.auth()
rtsp.rtsp_describe()
control = rtsp.get_media_control_attribute()
rtsp.rtsp_setup(transport, control)
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