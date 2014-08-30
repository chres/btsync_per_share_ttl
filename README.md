
__BitTorrent Sync__ only implements a global "sync_trash_ttl" option, but it may
be desired to specify "sync_trash_ttl" for each individual shared folder.

__BTSync Trash__ implements trashing functionalities that enable
"sync_trash_ttl" settings for every shared folder. Simply add

    //"sync_trash_ttl" : X,

to each shared folder in the config file of __BitTorrent Sync__.

__BitTorrent Sync__ will remove trashed files __X__ days according to the global
"sync_trash_ttl" setting in __all__ shared folders while __BTSync Trash__ will
remove trashed files only in shared folders that contain //"sync_trash_ttl".

In most cases, it may be desired to disable __BitTorrent Sync__ completely
such that trashed files are only removed in shared shared folders that contain
//"sync_trash_ttl". To do that, simply disable the global "sync_trash_ttl":

    "sync_trash_ttl" : 0,

Installation (arch linux)
------------------------

    $ makepkg
    # pacman -U btsync_per_share_ttl-1-1-any.pkg.tar.xz

Start (arch linux)
------------------

    # systemctl start btsync_per_share_ttl.service


