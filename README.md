# Retro Ethernet Sniffer

![Project Preview](./image/_DSC7089.jpg)

A WiFi sniffer that identifies devices communicating on your network (Ethernet) and displays their MAC addresses in binary form on an LED Matrix, giving it a retro style.

## Hardware

### Prerequisites

- Raspberry Pi (3B or later)

- LED matrix driven by MAX7219. It is recommended to use at least 4 8x8 matrix modules. A module containing 4 matrices on a single board is recommended and costs around CNY 17.6.

- Level shifter (optional). Although not required, it is recommended by the developers of luma.led_matrix to add a level shifter between your Raspberry Pi GPIO and LED module for better performance.

- Wires, power supply, etc.

### Wiring

| Board Pin | Name | Remarks     | RPi Pin | RPi Function     |
|-----------|------|-------------|---------|------------------|
| 1         | VCC  | +5 Power    | 2       | 5V0              |
| 2         | GND  | Ground      | 6       | GND              |
| 3         | DIN  | Data In     | 19      | GPIO 10(MOSI)    |
| 4         | CS   | Chip Select | 24      | GPIO 8(SPI CE0)  |
| 5         | CLK  | Clock       | 23      | GPIO 11(SPI CLK) |

The above table is copied from the [luma.led_matrix documentation](https://luma-led-matrix.readthedocs.io/en/latest/install.html#max7219-devices-spi) and it should work for most setups.

## Software

After configuring all the hardware components, it's time to run this exciting project!

To run this script, you need to first install Python 3 and pip on your Raspberry Pi (in my case, it's a Pi 3B).

```bash
sudo apt update
sudo apt install python3 python3-pip
```

Next, install Scapy and luma.led_matrix. You can install them using pip.

```bash
# You can use either of the following commands
pip install -r requirements.txt
# or
sudo pip install luma.led-matrix
sudo pip install scapy
# I personally prefer the first option.
```

After installing the required Python packages, enable the SPI interface in `raspi-config` using the following command:

```bash
sudo raspi-config
```

In the `Interface` submenu, find the `SPI` option and turn it on. Then, reboot your Raspberry Pi. You can also perform this step in the GUI, but I find the command-line interface more convenient.

Finally, you can run the script with the following command:

```bash
sudo python3 ./main.py
```

Enjoy! (If it works :)