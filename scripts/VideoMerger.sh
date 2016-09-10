#!/bin/bash

# usage:
# sh VideoMerger.sh [url0] [url1] [url2] [url3] ... [url n] [outputFileName]

# takes in urls to videos on signingsavvy.com, downloads them and concats
# outputs in ./output folder

mkdir -p temp
mkdir -p output

cd temp

for url in "$@"
do
    if !([[ $url == https://www.signingsavvy.com/signs/mp4/* ]])
        then continue
    fi

    curl -O $url
done

for file in *.mp4
do
    ffmpeg -y -i $file -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate_${file}.ts
done

intermediates=""
for file in intermediate_*.ts
do
    intermediates="${intermediates}${file}|"
done

ffmpeg -y -i "concat:${intermediates}" -c copy ../output/${@: -1}

rm *.mp4
rm intermediate_*.ts

# https://www.signingsavvy.com/signs/mp4/7/7449.mp4 https://www.signingsavvy.com/signs/mp4/7/7448.mp4
