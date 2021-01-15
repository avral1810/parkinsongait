#!/bin/sh

FILES="$1"

python3 data_cleaning.py run "$FILES"
python3 train-save.py run
