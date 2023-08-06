Convenient command line and library wrapper for youtube-dl.

*Latest release 20200621*:
* YDL.run: just catch the youtube_dl DownloadError.
* Changes to the default output filename template.
* Other minor internal changes.

The `youtube-dl` tool and associated `youtube_dl` Python module
are very useful for downloading media from various websites.
However, as an end user who almost never streams because of my
soggy internet link, I find fetching several items is quite serial and
visually noisy.

This module provides a command line tool `ydl` which:
- runs multiple downloads in parallel with progress bars
- prints the downloaded filename as each completes

Interactively, I keep this shell function:

    ydl(){
      ( set -ue
        dldir=${DL:-$HOME/dl}/v
        [ -d "$dldir" ] || set-x mkdir "$dldir"
        cd "$dldir"
        command ydl ${1+"$@"}
      )
    }

which runs the downloader in my preferred download area
without tedious manual `cd`ing.

## Function `main(argv=None, cmd=None)`

Main command line.

## Class `OverYDL`

A manager for multiple `YDL` instances.

## Class `YDL`

Manager for a download process.

### Method `YDL.__init__(self, url, *, fstags, upd=None, tick=None, over_progress=None, **kw_opts)`

Initialise the manager.

Parameters:
* `url`: the URL to download
* `fstags`: mandatory keyword argument, a `cs.fstags.FSTags` instance
* `upd`: optional `cs.upd.Upd` instance for progress reporting
* `tick`: optional callback to indicate state change
* `over_progress`: an `OverProgress` to which to add each new `Progress` instance
* `kw_opts`: other keyword arguments are used to initialise
  the options for the underlying `YoutubeDL` instance

## Class `YDLCommand(cs.cmdutils.BaseCommand)`

`ydl` command line implementation.


Command line usage:

    Usage: YDLCommand [-f] {URLs|-}...
        -f  Force download - do not use the cache.

# Release Log



*Release 20200621*:
* YDL.run: just catch the youtube_dl DownloadError.
* Changes to the default output filename template.
* Other minor internal changes.

*Release 20200615.1*:
Add usage message to docstring.

*Release 20200615*:
* Initial "daemon" mode, suitable for "tail -f .ydld-queue | ydl -", handy for keeping around in a tmux session.
* Assorted small bugfixes.

*Release 20200521*:
Initial PyPI release.
