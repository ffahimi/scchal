#!/bin/bash

cd ~/PycharmProjects/SoundCloudChallenge/src
export PYTHONPATH=~/
echo $PYTHONPATH
python run.py $1 $2 2>&1 >> logOutput.log
cd ~
