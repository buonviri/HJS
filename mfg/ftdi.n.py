# ASSUMNES WINDOWS OS
# rename this script abcd.n.py where:
#   abcd is the product name
#   n is the number of serialized objects
#   use nnn... to control the desired number of leading zeroes
#   example: myproduct.099.py will create 001 through 099
#   leading underscore may be added for sorting purposes
# override dot files: lot min max len product sep
# examples:
#   lot = 12345
#   min = 1
#   max = 99
#   len = 3 (001 to 099)
#   product = S2M2 or S2LP
#   sep = -PAC
# also attempts to populate the 'all' folder with multipurpose batch files
# todo: add prefix? or just use 12345-AET001

import os

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
         'echo SCAN and PROG\n'
         '"C:\\Program Files (x86)\\FTDI\\FT_Prog\\FT_Prog-CmdLine.exe" SCAN PROG 0 C:\\EdgeCortix\\hex-ftdi-cfg\\ftdi\\99999\\9876543210.xml\n'
         'echo SCAN and CYCL\n'
         '"C:\\Program Files (x86)\\FTDI\\FT_Prog\\FT_Prog-CmdLine.exe" SCAN CYCL 0\n'
         'echo DONE\n')
         # removed: 'timeout 10\n')

# End of batch file, start of all

all = """@echo off
:start

echo.
echo Connect the Renesas Programmer.
PAUSE 
echo.

:hex
cd..
cd..
cd hex
echo %cd%
call PRIMARY-cli.bat

echo.
echo Disconnect the Renesas Programmer 5x2.
echo Cycle power and wait for the LED to blink.
PAUSE
echo.

:ftdi
cd..
cd ftdi
cd 99999
echo %cd%
call 99999-PACZZZ.bat
color 07

echo.
echo Cycle power.
PAUSE
echo.

:cfg
cd..
cd..
cd cfg-edit
cd 99999
echo %cd%
call cfg-edit-99999-PACZZZ.bat

echo.
echo THE END

:end
timeout 60"""

# End of all


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
            # sn min is always 1, sn max as integer, length of limit string, prefix string
            return 1, int(foolist[1]), len(foolist[1]), foolist[0]  
        except:
            return -1, -1, 0, 'none'  # invalid entry
    else:
        return -2, -2, 0, 'none'  # wrong length
# End


# Read file info or use defaults
try:  # all four must be defined for this to work
    with open('.lot', 'r') as f:
        lot_code = f.read().strip()
    with open('.min', 'r') as f:
        min_sn = int(f.read())
    with open('.max', 'r') as f:
        max_sn = int(f.read())
    with open('.len', 'r') as f:
        len_sn = int(f.read())
    with open('.product', 'r') as f:
        product = f.read().strip()
    print('Overrides: ' + ' '.join( [lot_code, str(min_sn), str(max_sn), str(len_sn), product] ))
except:
    lot_code = get_container()  # use folder name
    min_sn, max_sn, len_sn, product  = get_limit()  # read from file name
try:  # check for separator
    with open('.sep', 'r') as f:
        separator = f.read().strip()
except:
    separator = '_'  # default

sn_start = ''
missing_folder = False
if len(lot_code) in [5,]:  # check if length is in the list of valid lot code lengths
    if max_sn < 1:  # must be at least 1
        print('Invalid max serial number: ' + str(max_sn))
    else:
        print('Generating serial numbers in range ' + str(min_sn) + ':' + str(max_sn) + ', format "' + 'n' * len_sn + '", for ' + product + ' lot code: ' + lot_code)
        for sn in range(min_sn, max_sn+1):
            str_sn = str(sn).rjust(len_sn, '0')  # pad with leading zeroes
            if sn_start == '':  # define both
                sn_start = lot_code + separator + str_sn
                sn_end = lot_code + separator + str_sn
            else:  # update ending sn
                sn_end = lot_code + separator + str_sn
            with open(lot_code + str_sn + '.xml', 'w', encoding="utf-16") as f:  # xml is number
                f.write(template.replace('ABCD', product).replace('9876543210', lot_code + str_sn).replace('99999', lot_code))  # programmed value is number
            with open(lot_code + separator + str_sn + '.bat', 'w') as f:  # batch filename contains separator
                f.write(batch.replace('ABCD', product).replace('9876543210', lot_code + str_sn).replace('99999', lot_code))  # filename pointer is number
            try:
                with open('..\\..\\all\\' + lot_code + '\\' + lot_code + separator + str_sn + '.bat', 'w') as f:  # batch filename contains separator
                    f.write(all.replace('PRIMARY', 'P112').replace('99999', lot_code).replace('ZZZ', str_sn))
            except:
                missing_folder = True
        print(sn_start + ' thru ' + sn_end)
else:
    print('Invalid lot code: ' + lot_code)

if missing_folder:  # \all\lotcode is missing
    print('\nCould not find "\\all\\' + lot_code + '\\" folder.')

# pause for user input, should be done in batch file instead
# os.system("PAUSE")

# EOF

"""
:start
echo Press a key (A, B, or C):
set /p input=
if "%input%"=="A" goto label_a
if "%input%"=="B" goto label_b
if "%input%"=="C" goto label_c
echo Invalid input. Please try again.
goto start

:label_a
echo You pressed A!
goto end

:label_b
echo You pressed B!
goto end

:label_c
echo You pressed C!
goto end

:end
echo Program finished.
pause
"""