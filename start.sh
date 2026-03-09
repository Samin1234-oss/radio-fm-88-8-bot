#!/bin/bash
# Download ffmpeg if it doesn't exist
if [ ! -f "./ffmpeg" ]; then
    echo "📥 Downloading ffmpeg..."
    curl -LO https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz
    tar -xf ffmpeg-release-i686-static.tar.xz
    mv ffmpeg-*-static/ffmpeg ./ffmpeg
    chmod +x ./ffmpeg
    rm -rf ffmpeg-release-i686-static.tar.xz ffmpeg-*-static
fi

# Run the bot
python3 radio_fm_88_8_bot.py