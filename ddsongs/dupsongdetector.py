import logging
import os
import shlex

import taglib

import sys

import re


class DupSongDetector:
    def __init__(self, path, log_level=0) -> None:
        super().__init__()

        # Regular expression that cleans the music title, ie:
        # Let's be happy (Remastered) -> let's be happy
        # Let's be happy -> let's be happy
        self.clean_title_re = re.compile(r"(\s?(?!\()(?!\s).)*")

        self.log = self._get_logger(log_level)

        self.srcdir = path

    def detect_dupes(self) -> list:
        # Duplicate file list
        dup_files = []

        if os.path.isdir(self.srcdir):
            song_titles = []

            # 'Walk' through all the files/dirs in the srcdir
            for root, dirs, files in os.walk(self.srcdir, topdown=False):
                # Query all the files
                for song_file in files:
                    # Get file full path
                    path = os.path.join(root, song_file)

                    # Tries to get song info
                    try:
                        # Parse the libs
                        song = taglib.File(path)

                        # Get song title & author
                        title = song.tags["TITLE"][0]
                        artist = song.tags["ARTIST"][0]

                        # Clean it
                        title = self._clean_music_title(title)

                        title = "{} - {}".format(title, artist.lower())

                        self.log.debug("Checking if '{}' is a dupe".format(title))

                        # If duplicate
                        if title in song_titles:
                            # Sends a clean path to dupe files
                            dup_files.append(shlex.quote(path))
                            self.log.debug("Dupe detected: '{}'".format(title))
                        else:
                            song_titles.append(title)
                            self.log.debug("Not dupe: '{}'".format(title))

                        # Closes song
                        song.close()
                    except:
                        # log.warn("'{}' doesn't has tags.".format(path))
                        pass
            return dup_files

    def _get_logger(self, log_level=0):
        # Get the logger
        module = sys.modules['__main__'].__file__
        log = logging.getLogger(module)

        # Log level
        log.setLevel(log_level)

        if log_level == 0:
            log.disabled = True

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create formater
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Add formatter to handler
        ch.setFormatter(formatter)

        # Add handler to logger
        log.addHandler(ch)

        return log

    # ie:
    # Let's be happy (Remastered) -> let's be happy
    # Let's be happy -> let's be happy
    def _clean_music_title(self, title):
        return self.clean_title_re.search(title)[0].lower()
