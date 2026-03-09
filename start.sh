#!/bin/bash
# Download small audio-only ffmpeg binary at start
wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-i686-static.tar.xz -O ffmpeg.tar.xz
tar -xf ffmpeg.tar.xz
mv ffmpeg*/ffmpeg ./ffmpeg
chmod +x ./ffmpeg

# Run bot
python radio_fm_88_8_bot.py