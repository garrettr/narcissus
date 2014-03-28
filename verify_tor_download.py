#!/usr/bin/env python

import os
import subprocess
import tempfile

# XXX urllib2 doesn't validate certificates!
# probably want to use requests (https://pypi.python.org/pypi/requests) instead
import urllib2

# https://www.torproject.org/docs/verifying-signatures.html.en

TBB_SIGNING_KEYID="0x416F061063FEE659"
TBB_SIGNING_KEY_FINGERPRINT="8738 A680 B84B 3031 A630  F2DB 416F 0610 63FE E659"

def gpg_has_key(keyid):
    rc = subprocess.call(["gpg", "--fingerprint", keyid])
    # exits with 0 if keyid found, 2 if not
    return True if rc == 0 else False

def gpg_recv_key(keyid):
    rc = subprocess.call(["gpg", "--keyserver", "x-hkp://pool.sks-keyservers.net", "--recv-keys", keyid])
    # TODO: handle errors

def gpg_verify_sig(sig_filename):
    # This function assumes that the file to be verified is in the same
    # directory as the sig_file, and has the same filename, minus either ".sig"
    # or ".asc"
    assert sig_filename.split(".")[-1] in ("sig", "asc")
    rc = subprocess.call(["gpg", "--verify", sig_filename])
    return True if rc == 0 else False

def verify_download(dl_url, sig_url):
    tmp_dir = tempfile.mkdtemp()
    dl_path = os.path.join(tmp_dir, dl_url.split('/')[-1])
    sig_path = os.path.join(tmp_dir, sig_url.split('/')[-1])
    with open(dl_path, "w") as dl_fp:
        dl_fp.write(urllib2.urlopen(dl_url).read())
    with open(sig_path, "w") as sig_fp:
        sig_fp.write(urllib2.urlopen(sig_url).read())
    verified = gpg_verify_sig(sig_path)
    # TODO: we are responsible for cleaning up tmp_dir
    return verified

def main():
    if not gpg_has_key(TBB_SIGNING_KEYID):
        gpg_recv_key(TBB_SIGNING_KEYID)
    dl_url = "http://tor.zilog.es/dist/torbrowser/3.5.3/tor-browser-linux32-3.5.3_en-US.tar.xz"
    sig_url = "http://tor.zilog.es/dist/torbrowser/3.5.3/tor-browser-linux32-3.5.3_en-US.tar.xz.asc"
    print verify_download(dl_url, sig_url)

if __name__ == "__main__":
    main()
