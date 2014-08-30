#!/usr/bin/python
# BitTorrent sync only implements a global "sync_trash_ttl" option, but it may
# be desired to specify "sync_trash_ttl" for each individual shared folder.
#
# This script implements a hack that enables "sync_trash_ttl" to be set for 
# each shared folder.
# Simply add   //"sync_trash_ttl" : X,   to each shared folder in the config
# file for BitTorrent sync. NOTICE that the line should be commented out such
# that btsync do not read the line (this script will read the line).
# It is highly recommented to add a global  "sync_trash_ttl" : 0  in the config
# file to disable btsync from removing trashed files, such that it is only this
# script that remove trashed files.

import os, time, sys, json, re, shutil
import pyparsing as pp
import argparse


# Load btsync.conf file into json
def load_config(filename):
    assert(isinstance(filename, str))

    text = ""
    try:
        f = open(filename)
    except IOError:
        print(std.strerr, "Cannot open {}".format(filename))
        sys.exit(1)
    else:
        text = f.read()
        f.close()

    # Remove c comments /* ... */
    ccomments = pp.nestedExpr("/*", "*/").suppress()
    text = ccomments.transformString(text)

    # Fixme: The regex substitution wrongly uncomments global occurences of
    # 'sync_trash_ttl'. This may lead to problems reading the json file in case
    # multiple global occurences of 'sync_trash_ttl' exists. It may also
    # trigger an incorrect warning in the function test_config()!

    # Uncomment //"sync_trash_ttl" : x"
    text = re.sub(r'/{2,}\s*("sync_trash_ttl"\s+:\s+[0-9]+)','\g<1>',text)

    # Remove c++ comments // ...
    cppcomments = pp.cppStyleComment.suppress()
    text = cppcomments.transformString(text)

    # Return config as dict
    return json.loads(text)

# Check config file
def test_config(config):
    assert(isinstance(config, dict))

    # It may not be intented to have both btsync and this script trashing files
    # in .SyncArchive directories.
    if not ('sync_trash_ttl' in config) or (config['sync_trash_ttl'] != 0):
        # This warning may be triggered incorrectly. See function load_config()
        print("Warning: You may want to disable the global 'sync_trash_ttl'",
                "in btsync config file")

    if not 'shared_folders' in config:
        print("Warning: No shared folders were found in btsync config file!")


def main(argv=None):
    # Config file
    #CONFIG_FILE = "/home/cws/.config/btsync/btsync.conf"

    # Load btsync configuration file
    config = load_config(args.configfile)

    # Test configuration file
    test_config(config)

    # Get current time
    now = time.time()

    # There is nothing to do if we do not find any shared folders
    if not 'shared_folders' in config:
        return

    # For each shared folder
    for folder in config['shared_folders']:

        # Skip folder if 'dir' or 'sync_trash_ttl' is not a key in shared folder
        if not {'dir','sync_trash_ttl'}.issubset(folder):
            continue

        ttl = folder['sync_trash_ttl']
        path = os.path.join(folder['dir'],'.SyncArchive')

        # Skip if trash directory doesn't exist
        if not os.path.isdir(path):
            continue

        # Skip if 'sync_trash_ttl' is disabled
        if ttl == 0:
            continue

        # Remove directories/files within trash folder (.SyncArchive) that are
        # older than ttl days
        for f in os.listdir(path):
            f = os.path.join(path,f)

            print(f)
            if os.stat(f).st_mtime < now - ttl*24*60*60:
                if os.path.isfile(f):
                    os.remove(f)
                    print("Removed file:", f)
                elif os.path.isdir(f):
                    shutil.rmtree(f)
                    print("Removed directory:", f)
                else:
                    print(f, "is neither a file or directory.",
                            "Please remove it manually.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--config', dest='configfile', action='store',
        help='BitTorrent sync config file',
        required=True)

    args = parser.parse_args()

    sys.exit(main(args))
