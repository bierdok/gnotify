#!/usr/bin/env python3
# coding: utf-8

__version__ = "0.1.0"
__usage__ = "Usage: gnotify -H [ip-addresses] -l [language] [text-to-speech]"


def main():
    import getopt
    import os
    import sys

    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhH:l:", ["version", "help", "ip-addresses=", "language="])
    except getopt.GetoptError:
        print(__usage__)
        sys.exit(2)

    lang = os.getenv("GNOTIFY_LANG", "")
    ips = [ip for ip in os.getenv("GNOTIFY_IPS", "").split(',') if ip]
    tts = " ".join(args)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(__usage__)
            sys.exit(2)
        elif opt in ("-v", "--version"):
            print("Version: {}".format(__version__))
            sys.exit(2)
        elif opt in ("-l", "--language"):
            lang = arg
        elif opt in ("-H", "--ip-addresses"):
            ips = [ip for ip in arg.split(',') if ip]

    import re

    errors = []

    if len(ips) == 0:
        errors.append('Please enter one or more ip addresses separated by commas as an option.')

    if str(lang) == "":
        errors.append('Please enter a language code (ISO 639-1) as an option.')
    elif not re.match(r"^\w{2}$", lang):
        errors.append('Please enter a valid language code (ISO 639-1) as an option.')

    if not tts or str(tts) == "":
        errors.append('Please enter a text-to-speech as arguments.')
    elif len(tts) > 5000:
        errors.append('The requested text-to-speech is too long (> 5000).')

    if errors:
        print(__usage__ + '\n')
        print('\n'.join(errors))
        sys.exit(2)

    import time
    from pychromecast import Chromecast
    from pychromecast.error import ChromecastConnectionError
    from socketserver import ThreadingTCPServer
    from http.server import SimpleHTTPRequestHandler
    from threading import Thread
    from cachier import cachier

    @cachier()
    def get_tts_mp3(tl, q):

        from urllib.error import HTTPError
        from urllib.parse import urlencode
        from urllib.request import Request
        from urllib.request import urlopen

        request = Request("{}?{}".format(
            "https://translate.google.com/translate_tts",
            urlencode({
                "ie": "UTF-8",
                "q": q,
                "tl": tl,
                "client": "tw-ob"
            })
        ))
        request.add_header("Referer", "http://translate.google.com/")
        request.add_header("User-Agent", "stagefright/1.2 (Linux;Android 5.0)")

        try:
            response = urlopen(request)
        except HTTPError:
            print("Google Translate error")
            sys.exit(2)

        return response.read()

    class FileHTTPRequestHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(get_tts_mp3(lang, tts))

        def log_message(self, format, *args): return

    for ip in ips:
        try:
            cast = Chromecast(ip)
        except ChromecastConnectionError as e:
            print(e)
            sys.exit(2)

        server_ip = cast.socket_client.socket.getsockname()[0]
        server = ThreadingTCPServer((server_ip, 0), FileHTTPRequestHandler)
        server_port = str(server.server_address[1])

        thread = Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

        cast.wait()

        mc = cast.media_controller
        mc.play_media("http://{}:{}".format(server_ip, server_port), "audio/mpeg")

        while mc.status.player_state != "IDLE":
            try:
                time.sleep(0.05)
            except KeyboardInterrupt:
                mc.stop()
                break

        server.shutdown()
        server.server_close()
