# termoslides

Simple (maybe the simplest) stupid terminal based slide viewer. Slides are composed as text files and are separated by `EOS\n` magic divider.

Usage:
```
python3 termoslides.py -h
usage: termoslides.py [-h] slides

Terminal Slides

positional arguments:
  slides      file containing slides

options:
  -h, --help  show this help message and exit
```

`termoslides` is a simple Python application which is dependent only on standard library and nothing else.

### Sample slide
```
Welcome to termoslides

This is the best terminal based slide viewer
EOS
Advantages

* none
* none that I can think of
```

Save the above text into _sample-slide.txt_ and run it:
`python3 termoslides.py sample-slide.txt`
