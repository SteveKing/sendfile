# sendfile
Send files from a remote host and receive them using iTerm2's coprocess feature.

## The Problem

I often ssh to remote machines. Sometimes it's a direct connection, but more
often than not I have to first login to a corporate jumphost, then ssh from
there to a deployment leader, then from there to my target machine. It's a royal
pain if I need to copy files back to my Mac. I either have to set up a series of
ssh tunnels (usually forbidden by policy) or have to copy files from one host to
another across each hop (usually forbidden by lack of write permission on the
intermediaries).

I need a way to transmit files over the existing ssh stdio. Ideally I'd use
something like zmodem which is designed for this very purpose. Unfortunately
it's not installed on the remote machines, and I don't have the ability to
install new software.

## The Solution

My solution is sendfile.  The sending end relies only on tools that are already
installed on my remote machines: bash, tar, and base64.  The 'sendfile' command
is only six lines of shell script. The 'recvfile' command on my Mac is a custom
Python script.

Sendfile starts by sending a unique string that I can use as a trigger in iTerm.
When iTerm sees the string it runs recvfile as a co-process.  Sendfile sends
a base64-encoded tar file which recvfile unpacks.

## Setup

1. Put recvfile.py somewhere convenient on your Mac.

2. Set up the following trigger in your iTerm profile:

    * Regular Expression: `^\s*-\*-\{\{SENDFILE\}\}-\*-\s*$`
    * Action: `Run Silent Coprocess...`
    * Parameters: `/usr/bin/python /path/to/recvfile.py`

3. On the remote machine, source 'sendfile.sh' (or copy the sendfile function
   into your .bashrc).

## Usage

On the remote machine type "sendfile filename".  Multiple filenames can be
given. You'll see the start string `-*-{{SENDFILE}}-*-` printed out, after
which iTerm will execute 'recvfile.py'.  The received files are placed in
`~/Downloads/` in a new directory named for the remote hostname and the current
date/time.

## Author

Copyright (c) 2016 Steve King, <steve@narbat.com>
