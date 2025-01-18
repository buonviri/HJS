#!/bin/bash

sudo echo Target info:  # makes lspci line look less out of place

sudo lspci -vvv -d 1fdc: | grep -E 'LnkSta:.*Speed'  # highlight link info line
python3 ~/HJS/statlog/statlog.py S2XX-info-void | grep -E 'EdgeCortix.*S2M2'
if [ $? -eq 0 ]; then
    echo
    echo "Compute Node A:" | tee 'CB.log'
    python3 statlog.py S2M2-srread.a.0x10100+srwrite.a.0x10100.0+srread.a.0x10100-void | tee -a 'CB.log'
    echo " 01 00 00" | tee -a 'CB.log'
    python3 statlog.py S2M2-pin.M2EN_PG1.set+srread.a.0x1001C-void | tee -a 'CB.log'
    echo " P106 07" | tee -a 'CB.log'
    python3 statlog.py S2M2-srwrite.a.0x1001C.4+srread.a.0x1001C-void | tee -a 'CB.log'
    echo " 04 04" | tee -a 'CB.log'
    python3 statlog.py S2M2-pin.M2EN_PG2.set+srread.a.0x1001C-void | tee -a 'CB.log'
    echo " P111 04" | tee -a 'CB.log'
    python3 statlog.py S2M2-srwrite.a.0x1001C.0+srread.a.0x1001C+srwrite.a.0x10100.1+srread.a.0x10100-void | tee -a 'CB.log'
    echo " 00 00 01 01" | tee -a 'CB.log'
    echo
    python3 statlog.py S2M2-stats-void | tee -a 'CB.log'
    echo T >> 'CB.log'
    echo H >> 'CB.log'
    echo E >> 'CB.log'
    echo  >> 'CB.log'
    echo E >> 'CB.log'
    echo N >> 'CB.log'
    echo D >> 'CB.log'
else
    python3 ~/HJS/statlog/statlog.py S2XX-info-void | grep -E 'EdgeCortix.*S2LP'
    if [ $? -eq 0 ]; then
        echo
        echo "Compute Node A:" | tee 'CB.log'
        python3 statlog.py S2LP-srread.a.0x10100+srwrite.a.0x10100.0+srread.a.0x10100-void | tee -a 'CB.log'
        echo " 01 00 00" | tee -a 'CB.log'
        python3 statlog.py S2LP-pin.AEN_PG1.set+srread.a.0x1001C-void | tee -a 'CB.log'
        echo " P203 07" | tee -a 'CB.log'
        python3 statlog.py S2LP-srwrite.a.0x1001C.4+srread.a.0x1001C-void | tee -a 'CB.log'
        echo " 04 04" | tee -a 'CB.log'
        python3 statlog.py S2LP-pin.AEN_PG2.set+srread.a.0x1001C-void | tee -a 'CB.log'
        echo " P310 04" | tee -a 'CB.log'
        python3 statlog.py S2LP-srwrite.a.0x1001C.0+srread.a.0x1001C+srwrite.a.0x10100.1+srread.a.0x10100-void | tee -a 'CB.log'
        echo " 00 00 01 01" | tee -a 'CB.log'
        echo
        echo "Compute Node B:" | tee -a 'CB.log'
        python3 statlog.py S2LP-srread.b.0x10100+srwrite.b.0x10100.0+srread.b.0x10100-void | tee -a 'CB.log'
        echo " 01 00 00" | tee -a 'CB.log'
        python3 statlog.py S2LP-pin.BEN_PG1.set+srread.b.0x1001C-void | tee -a 'CB.log'
        echo " P009 07" | tee -a 'CB.log'
        python3 statlog.py S2LP-srwrite.b.0x1001C.4+srread.b.0x1001C-void | tee -a 'CB.log'
        echo " 04 04" | tee -a 'CB.log'
        python3 statlog.py S2LP-pin.BEN_PG2.set+srread.b.0x1001C-void | tee -a 'CB.log'
        echo " P505 04" | tee -a 'CB.log'
        python3 statlog.py S2LP-srwrite.b.0x1001C.0+srread.b.0x1001C+srwrite.b.0x10100.1+srread.b.0x10100-void | tee -a 'CB.log'
        echo " 00 00 01 01" | tee -a 'CB.log'
        echo
        python3 statlog.py S2LP-stats-void | tee -a 'CB.log'
        echo T >> 'CB.log'
        echo H >> 'CB.log'
        echo E >> 'CB.log'
        echo  >> 'CB.log'
        echo E >> 'CB.log'
        echo N >> 'CB.log'
        echo D >> 'CB.log'
    else
        printf "Compute Block enable - no S2 cards found.\n"
    fi
fi

# EOF
