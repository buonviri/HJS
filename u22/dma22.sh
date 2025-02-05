#!/bin/bash

# whichever one is last wins
size="1024"  # 1k * 1k
size="1048576"  # 1k * 1k * 1k

echo
printf "\e[1;31m   Hopefully you already typed 'ant22' !!!\e[0m\n"

echo
echo Testing Device 0, DDR0...
~/dna2_self_test_2_2_0/dma_test 0 ddr0 $size &> ~/.dma00
# echo $?
cat ~/.dma00 | \grep -i -E "passed|failed"  # | sed "s/Read speed/RD/g" | sed "s/Write speed/WR/g"

echo
echo Testing Device 0, DDR1...
~/dna2_self_test_2_2_0/dma_test 0 ddr1 $size &> ~/.dma01
# echo $?
cat ~/.dma01 | \grep -i -E "passed|failed"  # | sed "s/Read speed/RD/g" | sed "s/Write speed/WR/g"

echo
echo Testing Device 1, DDR0...
~/dna2_self_test_2_2_0/dma_test 1 ddr0 $size &> ~/.dma10
# echo $?
cat ~/.dma10 | \grep -i -E "passed|failed"  # | sed "s/Read speed/RD/g" | sed "s/Write speed/WR/g"

echo
echo Testing Device 1, DDR1...
~/dna2_self_test_2_2_0/dma_test 1 ddr1 $size &> ~/.dma11
# echo $?
cat ~/.dma11 | \grep -i -E "passed|failed"  # | sed "s/Read speed/RD/g" | sed "s/Write speed/WR/g"

rm ~/.dma*  # remove log files

echo
echo "   Sincerely, HJS"
echo

# EOF

