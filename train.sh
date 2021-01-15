#!/bin/sh

FILES="$1/*.txt"

for f in $FILES
do
  python3 data_cleaning.py "train $f"
done

FILES="dataFiles/fortrain/"

python3 combine.py "$FILES"
python3 train-save.py train
