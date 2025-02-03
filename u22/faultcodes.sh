#!/bin/bash

echo POWER_FAULT_NONE        0          // power fault bit maps
echo POWER_FAULT_TEMP_SENSE  0x0001     // temp1075 > thresh
echo POWER_FAULT_TEMP_TPS    0x0002     // tps > shutdown temp
echo POWER_FAULT_TEMP_BMC    0x0004     // bmc > shutdown temp
echo POWER_FAULT_TEMP_SAKURA 0x0008     // sakura > shutdown temp
echo POWER_FAULT_FAN         0x0010     // fan stalled
echo POWER_FAULT_VOLT        0x0020
echo POWER_FAULT_ILIMIT      0x0040
echo POWER_FAULT_BAD         0x0080     // power good not sensed
echo POWER_FAULT_IO          0x0100     // error accessing power device
echo POWER_FAULT_OTHER       0x0200
echo POWER_FAULT_SHUTDOWN    0x8000     // power has been disabled

# EOF
