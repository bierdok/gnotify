gnotify
=======

Command line program to get notified on your Google devices from a text-to-speech.

Works with:

- [Google Translate](https://translate.google.com/) converts a text-to-speech to an audio resource.
- [PyChromecast](https://github.com/balloob/pychromecast) interacts with Google devices to play audio resource.
- [Cachier](https://github.com/atmb4u/cashier) persists audio resource into user cache with mongo.

Installation
------------

From GitHub:

```
# pip3 --no-cache-dir install https://github.com/bierdok/gnotify/archive/master.zip
```

From the source tree:

```
# python3 setup.py install clean
```

Usage
-----

```
gnotify --help
```
