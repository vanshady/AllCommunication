#!/bin/bash

# usage:
# sh VideoMerger.sh [url0] [url1] [url2] [url3] ... [url n] [outputFileName]

# takes in urls to videos on signingsavvy.com, downloads and concats them
# outputs at ./output/outputFileName
# silently overwrites if file name already exists

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

outputName=${@: -1}

if ([[ ${outputName} == https://www.signingsavvy.com/signs/mp4/* ]]) then
    outputName="output.mp4"
    echo "[WARNING] No ouput file name specified. Outputs to output.mp4."
fi

ffmpeg -y -i "concat:${intermediates}" -c copy ../output/${outputName}

rm *.mp4
rm intermediate_*.ts

# https://www.signingsavvy.com/signs/mp4/7/7449.mp4 https://www.signingsavvy.com/signs/mp4/7/7448.mp4
