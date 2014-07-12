#! /bin/bash
sudo rm -r results
sudo rm -r buildResults
mkdir results
mkdir buildResults
python source/main_build.py
python source/main_predict.py