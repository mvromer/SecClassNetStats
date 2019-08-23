#!/bin/bash

zmap -p 80 -o results.csv -b blacklist.txt -t 14400 -B 50M -q
