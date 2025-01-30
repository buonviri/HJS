# ASSUMNES WINDOWS OS
# rename this script abcd.n.py where:
#   abcd is the product name
#   n is the number of serialized objects
#   use nnn... to control the desired number of leading zeroes
#   example: myproduct.099.py will create 001 through 099

import os

separator = '_'

# Template:

template = """<?xml version="1.0" encoding="utf-16"?>
<FT_EEPROM>
  <Chip_Details>
    <Type>FT X Series</Type>
  </Chip_Details>
  <USB_Device_Descriptor>
    <VID_PID>0</VID_PID>
    <idVendor>0403</idVendor>
    <idProduct>6015</idProduct>
    <bcdUSB>USB 2.0</bcdUSB>
  </USB_Device_Descriptor>
  <USB_Config_Descriptor>
    <bmAttributes>
      <RemoteWakeupEnabled>false</RemoteWakeupEnabled>
      <SelfPowered>false</SelfPowered>
      <BusPowered>true</BusPowered>
    </bmAttributes>
    <IOpullDown>false</IOpullDown>
    <MaxPower>90</MaxPower>
  </USB_Config_Descriptor>
  <USB_String_Descriptors>
    <Manufacturer>FTDI</Manufacturer>
    <Product_Description>FT230X on ABCD</Product_Description>
    <SerialNumber_Enabled>true</SerialNumber_Enabled>
    <SerialNumber>9876543210</SerialNumber>
    <SerialNumberPrefix>99999</SerialNumberPrefix>
    <SerialNumber_AutoGenerate>false</SerialNumber_AutoGenerate>
  </USB_String_Descriptors>
  <Hardware_Specific>
    <USB_Suspend_VBus>false</USB_Suspend_VBus>
    <RS485_Echo_Suppress>false</RS485_Echo_Suppress>
    <Port_A>
      <Hardware>
        <Device>FT230X/FT231X/FT234X (UART)</Device>
      </Hardware>
      <Driver>
        <D2XX>false</D2XX>
        <VCP>true</VCP>
      </Driver>
    </Port_A>
    <Battery_Charge_Detect>
      <Enable>false</Enable>
      <Power_Enable>false</Power_Enable>
      <Deactivate_Sleep>false</Deactivate_Sleep>
    </Battery_Charge_Detect>
    <Invert_RS232_Signals>
      <TXD>false</TXD>
      <RXD>false</RXD>
      <RTS>false</RTS>
      <CTS>false</CTS>
      <DTR>false</DTR>
      <DSR>false</DSR>
      <DCD>false</DCD>
      <RI>false</RI>
    </Invert_RS232_Signals>
    <CBUS_Signals>
      <C0>GPIO</C0>
      <C1>GPIO</C1>
      <C2>GPIO</C2>
      <C3>GPIO</C3>
    </CBUS_Signals>
    <IO_Pins>
      <DBUS>
        <SlowSlew>false</SlowSlew>
        <Schmitt>false</Schmitt>
        <Drive>4mA</Drive>
      </DBUS>
      <CBUS>
        <SlowSlew>false</SlowSlew>
        <Schmitt>false</Schmitt>
        <Drive>4mA</Drive>
      </CBUS>
    </IO_Pins>
  </Hardware_Specific>
</FT_EEPROM>"""

# End of Template, start of batch file

batch = ('@echo off\n'
'"C:\\Program Files (x86)\\FTDI\\FT_Prog\\FT_Prog-CmdLine.exe" SCAN PROG 0 C:\\EdgeCortix\\FDTI\\99999\\9876543210.xml CYCL 0\n'
'echo.\n'
'echo Verify programming succeeded!\n'
'timeout 5\n'
'"C:\\Program Files (x86)\\FTDI\\FT_Prog\\FT_Prog-CmdLine.exe" SCAN\n'
'timeout 3\n')

# End of batch file


def get_container():
    return os.getcwd().split('\\')[-1]  # get string after final backslash
# End


def get_limit():
    foo = os.path.basename(__file__)
    if foo.startswith('_'):  # remove leading underscore if present
        foo = foo[1:]
    foolist = foo.split('.')
    if len(foolist) == 3:  # ftdi.n.py should have three objects
        try:
            # sn limit as integer, length of limit string, prefix string
            return int(foolist[1]), len(foolist), foolist[0]  
        except:
            return -1, 0, 'none'  # invalid entry
    else:
        return -2, 0, 'none'  # wrong length
# End


lot_code = get_container()
if len(lot_code) in [5,]:  # check if length is in the list of valid lot code lengths
    max_sn, len_sn, product  = get_limit()
    if max_sn < 1:  # must be at least 1
        print('Invalid max serial number: ' + str(max_sn))
    else:
        print('Generating ' + str(max_sn) + ' serial number(s), format "' + 'n' * len_sn + '", for ' + product + ' lot code: ' + lot_code)
        for sn in range(max_sn):
            str_sn = str(sn+1).rjust(len_sn, '0')  # loop value is zero to n-1, so add one, and pad with leading zeroes
            if sn == 0:
                sn_start = lot_code + separator + str_sn
                sn_end = lot_code + separator + str_sn
            else:
                sn_end = lot_code + separator + str_sn
            with open(lot_code + separator + str_sn + '.xml', 'w', encoding="utf-16") as f:  # filename contains separator
                f.write(template.replace('ABCD', product).replace('9876543210', lot_code + str_sn).replace('99999', lot_code))  # programmed value does not
            with open(lot_code + separator + str_sn + '.bat', 'w') as f:  # filename contains separator
                f.write(batch.replace('ABCD', product).replace('9876543210', lot_code + separator + str_sn).replace('99999', lot_code))  # filename contains separator
        print(sn_start + ' thru ' + sn_end)
else:
    print('Invalid lot code: ' + lot_code)

# pause for user input
os.system("PAUSE")

# EOF
