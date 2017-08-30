#!/bin/bash -
dir="/home/yufujimoto/Desktop/Colorize"
src="/home/yufujimoto/GitHub/colorize"

dir_org="$dir/source"
dir_inp="$dir/input"
dir_col="$dir/colorized"
dir_out="$dir/output"

# Specify the file extention of original image files.
ext="JPG"

# Create thumbnails which suite for the colorization.
python2 "$src_2/thumbs.py" "$dir_org" "$dir_inp" 400 ".$ext" ".png"

# Get created thumbnails and recursively colorizing.
for fl in $dir_inp
do
    if [ -d "$fl" ]
    then
        for fl_inp in $fl/*
        do
            # Get the file name without extension.
            fl_nam=${fl_inp##*/}
            
            # Give the output file name.
            fl_col="$dir_col/$fl_nam"
            fl_out="$dir_out/$fl_nam"
            
            # Colorize.
            (cd "$src"; th colorize.lua "$fl_inp" "$fl_col")
            
            # Get the original file and its size.
            fl_ori="$dir_org/${fl_nam//png/$ext}"
            
            # Resize the colorized image.
            python2 "$dir_org/pixelmath.py" "$fl_col" "$fl_ori" "$fl_out"
            
            echo $fl_inp
        done
    fi
done

