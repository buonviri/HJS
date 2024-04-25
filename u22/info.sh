#!/bin/bash

lscpu | grep -Po 'Model name:\s+\K.*' | tee ~/mycpu.txt

# EOF
