
# Youtube Downloader

Youtube downloader is a GUI helper for [youtube-dl](https://github.com/ytdl-org/youtube-dl/). It provides a graphical interface to add, track and remove videos from youtube. 

## Preview

![preview](https://imgur.com/Mz01ecJ.png)

## Dependency

This software is based on [PySide2](https://www.qt.io/qt-for-python) and [youtube-dl](https://github.com/ytdl-org/youtube-dl/).

## Features

It allows for customizing your downloads:

- Select where a single download should be stored
- What kind of file it should be
- Pause and resume 
- Download thumbnail


## Usage

Youtube downloader’s goal is comfort. To add your download you can just paste the link into the input and hit enter or press button but I strongly recommend to drag a youtube video’s thumbnail and drop it into youtube downloader.

![drop](https://thumbs.gfycat.com/BoldSnappyEarthworm-size_restricted.gif)

## Web Browser integration

Youtube Downloader is integrated with Firefox, that's mean it will read currently opened tabs with YouTube's links. It provides a feature to quick download currently played videos from YouTube.

## Installation

Prepare youtube downloader to work

### Manual

```bash
git clone https://github.com/blooser/youtube-downloader
cd youtube-downloader
python setup.py build
sudo setup.py install
```

### PyPi

```bash
pip install youtube-downloader
```

## License

Youtube downloader is a free software released under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).
