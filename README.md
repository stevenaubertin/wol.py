# Wake-on-LAN

## Synopsis

Application that sends the [Wake-on-LAN](https://en.wikipedia.org/wiki/Wake-on-LAN) magic packet to a computer in order to wake him up from slumber.

## To Use

Clone this repository and run the python script (wol.py) with the mac address of the target.
From your command line:

```bash
# Clone this repository
git clone https://github.com/stevenaubertin/wol.py
# Go into the repository
cd wol.py
# Run the app
python wol.py -m 1c:1b:04:55:4a:00
```

### There is other command line arguments that can be used:
```
#Specify the mac address with -m
#This is required
python wol.py -m 1c:1b:04:55:4a:00
```
```
#Specify the broadcast ip address with -i
#By default it's 192.168.0.255
python wol.py -i 192.168.0.255 -m 1c:1b:04:55:4a:00
```
```
#For verbosity use -v
python wol.py -m 1c:1b:04:55:4a:00 -v 
```
```
#Specify the port to use with -p by default it's 9
python wol.py -m 1c:1b:04:55:4a:00 -p 9
```
```
#Print help message
python wol.py -h
python wol.py
```

#### License [MIT](LICENSE)
