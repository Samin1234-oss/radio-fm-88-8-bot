#!/bin/bash
# install ffmpeg
apt update
apt install -y ffmpeg

# start bot
python radio_fm_88_8_bot.py
