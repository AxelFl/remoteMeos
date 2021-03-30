# distanceMeos
Script for having a distance readout station and reporting it to MeOS

## Requirements
Requires `sireader`, install with `pip3 install sireader`

## Running script
First start meOS and go to the SportIdent tab
Then select TCP in the dropdown menu and press Activate and then at the boton select a port and press Start.

Run with the python script with

    python3 distanceMeos.py IP_Address port

Where IP_Address is the IP address to the computer running meOS, and the port is the port selected when starting the TCP-server in MeOS
  
