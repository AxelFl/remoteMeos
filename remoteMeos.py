from sireader import SIReader, SIReaderReadout, SIReaderControl, SIReaderCardChanged, SIReaderException
from time import sleep
import socket
import datetime
import sys

def get_card_data(si):
    # wait for a card to be inserted into the reader
    while not si.poll_sicard():
        sleep(1)

    # Some properties are now set
    card_number = si.sicard
    card_type = si.cardtype

    # read out card data
    card_data = si.read_sicard()
    card_data["punches"].insert(0, (1, card_data["start"]))
    card_data["punches"].append((2, card_data["finish"]))

    return convert_card_data(card_data, card_number, card_type)


def convert_card_data(card_data, card_number, card_type):  # Returns as byte-like 
    # Standard stuff first
    total_data = reverse_bytes(64, 8)  # Cardtype ????, should just work with 64

    total_data += reverse_bytes(len(card_data["punches"]), 16)  # Number of punches

    total_data += reverse_bytes(card_number, 32)  # SIcard number
    total_data += reverse_bytes(0, 32)  # codeDay: obsolete, always 0
    total_data += reverse_bytes(0, 32)  # codeTime: always 0 as MeOS uses 00:00:00 as reference time with TCP

    # Loop trough punches 
    # First reversed code number, then time after 00:00:00 in 1/10s
    for punch in card_data["punches"]:
        total_data += reverse_bytes(punch[0], 32)
        total_data += reverse_bytes(convert_time(punch[1]), 32)
    
    return bitstring_to_bytes(total_data)


def send_card_data(data, TCP_IP, TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Start TCP socket
    s.connect((TCP_IP, TCP_PORT))
    s.send(data)
    s.close()


def reverse_bytes(data, width):  # Int to reverse binary string
    binary = '{:0{width}b}'.format(data, width=width)  # Make into binary string and pad with zeroes
    byte = []
    for i in range(0, len(binary), 8):
        byte.append(binary[i:i+8])  # Split binarystring into bytes

    reverse = "".join(byte[::-1])  # Make into binary-string with bytes reversed
    return reverse


def reverse_byte_like(data, width):
    integer = int(data[2:], 2)
    return reverse_bytes(integer, width)


def convert_time(time):  # Datetime.time to deciseconds after 00:00:00
    hour_to_decisecond = time.hour * 36000
    minute_to_decisecond = time.minute * 600
    second_to_decisecond = time.second * 10
    return hour_to_decisecond + minute_to_decisecond + second_to_decisecond


def bitstring_to_bytes(s):  # Not sure how this works
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])


def main():
    # Connect to base station, the station is automatically detected,
    # if this does not work, give the path to the port as an argument
    # see the pyserial documentation for further information.
    si = SIReaderReadout()
    si.CARD["SI10"]["P1"] = 512  # Fix issue with reading SI10
    si.set_extended_protocol()

    while 1:
        try:
            new_data = get_card_data(si)
            send_card_data(new_data, sys.argv[1], int(sys.argv[2]))
            si.ack_sicard()

        except (SIReaderCardChanged, SIReaderException):  # Ignore ETX-byte error, and removing card too fast
            sleep(5)


if __name__ == "__main__":
     main()
