#!/bin/bash

# shellcheck source=/dev/null
source ~/miniconda3/etc/profile.d/conda.sh
cd ~/lanz_podcast && conda activate py36 && python main.py
