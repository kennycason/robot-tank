# Robot Tank

#### Venv Setup
```bash
pip install virtualenv
virtualenv -p python3.9.15 venv
source venv/bin/activate
```


## Client Dependencies
```shell
pip install pygame
pip install requests
TODO add more dependencies
```

## Client Dependencies
```shell
pip install flask
pip install flask_core
TODO add more dependencies
```
## Tank Client - PyGame + PS5 Controller


#### Start

```shell
python pygame-client/tank_client_ps5_controller.py
```


## Tank CLI

#### Start

```shell
python tank_cli.py
```

#### Controls

```shell
# ↖  ↑  ↗   1 speed--
#   QWE     2 speed++
# ← ASD →   H clockwise
#   ZXC     J counterclockwise
# ↙  ↓  ↘　
```


## Tank Web Server

Deploy
```shell
rsync -azvh server spider.local:~/robot-tank/ 
```

```shell
ssh spider.local
cd robot-tank/server/
export FLASK_APP=tank_server
flask run -h 192.168.4.76 -p 8080
```

#### Endpoints
```shell
POST /tank/forward
POST /tank/reverse
POST /tank/stop
POST /tank/turn-left
POST /tank/turn-right
POST /tank/left-track-forward
POST /tank/left-track-reverse
POST /tank/right-track-forward
POST /tank/right-track-reverse
POST /tank/clockwise
POST /tank/counter-clockwise
POST /tank/counter-clockwise
POST /tank/counter-clockwise
```

```shell
GET /tank/status
```
Response:
```json
{
    "leftTrack": {
        "speed": 100
    },
    "rightTrack": {
        "speed": 100
    }
}
```



#### Stream Video over TCP

Server (spider.local)
```bash
libcamera-vid -t 0  -q 100 --framerate 3 -n --codec mjpeg --inline --listen -o tcp://192.168.4.76:8888 -v
```
or
```bash
libcamera-vid -t 0  -q 75 --framerate 10 -n --codec mjpeg --inline --listen -o tcp://192.168.4.76:8888 -v 
```


Client (VLC -> Open Network)
```bash
tcp/mjpeg://192.168.4.76:8888
```
Client using FFPlay
```bash
ffplay -probesize 32 -analyzeduration 0 -fflags nobuffer -fflags flush_packets -flags low_delay -framerate 30 -framedrop tcp://192.168.4.76:8888
```

#### Compile C++ code that uses RF24/SPI libraries

```bash
 g++ -L/usr/local/include/ scanner.cpp -lrf24
```


## Video Recordings:
https://v.usetapes.com/oFj2Rk1B44





## Sample Output

#### CLI Output

```shell
#### Output
```shell
python tank_cli.py
Init Track, enA: 16, in1: 20, in2: 26
Init Track, enA: 25, in1: 24, in2: 23
stop
left track stop
left track stop
w
forward
left track forward
left track forward
x
reverse
left track reverse
left track reverse
d
turn right
left track forward
left track stop
a
turn left
left track stop
left track forward
h
rotate clockwise
left track forward
left track reverse
j
rotate counterclockwise
left track reverse
left track forward
e
left track forward
c
left track reverse
q
left track forward
z
left track reverse
s
stop
left track stop
left track stop
```

