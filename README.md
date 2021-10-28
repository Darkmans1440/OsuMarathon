## Preface

This program uses [Pydub](https://github.com/jiaaro/pydub) to modify audio.

This program uses [Colorama](https://github.com/tartley/colorama) to make the console look pretty.

This program is probably pretty bad. It's my first ever program in python.

I downloaded pycharm, followed their quick tutorial, typed code, and searched the internet when I needed to know
something. Quality programming.

## How to setup/download

Download Python from [here](https://www.python.org/downloads/)

Click the green Code button towards the top-right of this repository and then Download Zip.

After that, extract the OsuMarathon-main folder out of the zip to wherever you want.

Then, download ffmpeg/ffprobe from [here](https://www.ffmpeg.orgt/download.html)

And finally, drag the downloaded ffmepg/ffprobe into the OsuMarathon-main folder.

## How to launch

Launch the program by double-clicking Main.py.

After that, you should see a command window like this popup:

![the window](https://i.imgur.com/uJV2lRX.png)

## Arguments

The command window accepts input like a console window. You are going to use this to create your marathon.

Every space is equal to a new argument. To make an argument span multiple spaces, encase it with double quotations.

An example, when you input

> property title "my custom marathon!"

The above would equal 3 arguments (property, title, "my custom marathon!")

And without the double quotations, it would equal 5 arguments (property, title, my, custom, marathon!).

## Making a marathon

Read the usage for each command in the command window for a more detailed explanation.

1. Load beatmaps into the program by using the 'load' command
2. (Optional) swap the order of the loaded beatmaps using the 'swap' command
3. Configure the properties of the marathon using the 'property' command.
4. Create the marathon using the 'create' command.
