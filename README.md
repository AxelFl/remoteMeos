# remoteMeos
Script for having a distance readout station and reporting it to MeOS

## Requirements
Requires `python3` and  the package `sireader`. 
Python3 can be installed from [python.org](https://python.org) an `sireader`is installed with running `pip3 install sireader`


## Running script
First start meOS and go to the SportIdent tab.

Then select TCP in the dropdown menu and press Activate and then at the bottom select a port and press Start.

Run with the python script with

    python3 distanceMeos.py IP_Address port

Where IP_Address is the IP address to the computer running meOS, and the port is the port selected when starting the TCP-server in MeOS

When running the script and MeOS on different networks it is important to make sure that the port being used is forwarded to the computer running MeOS. This is usually done in the settings of the router that is running the network that MeOS is using.
  
