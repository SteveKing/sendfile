# sendfile
Send files from a remote host and receive them using iTerm2's coprocess feature.

## Background

I often ssh to remote machines. Sometimes it's a direct connection, but more
often than not I have to first login to a corporate jumphost, then ssh from
there to a deployment leader, then from there to my target machine. It's a royal
pain if I need to copy files back to my Mac. I either have to set up a series of
ssh tunnels (usually forbidden by policy) or have to copy files from one host to
another across each hop (often not an option because I don't have write
permission to one or more intermediates). What's a guy to do?

I thought back to Ye Olden Dayes of dial-up bulletin board systems. They had a
nice simple way to copy files: Zmodem.  You could send a file from the remote
end then switch to Zmodem receive mode on the local end. If you had a
particularly sophisticated terminal program it would detect the Zmodem signature
and automatically start receiving.  If only we had something like that these
days...

Zmodem is still around.  The modern Unix-y package is called 'lrzsz' and it
compiles and runs on darned near anything.  Except... It's not pre-installed on
my target systems, and I don't have permission to install anything. Scratch
that.

But the idea is good. I just need to write the file transfer protocol myself. In
a small enough shell script that I can "upload" it using the same hotkey macro
which sets up all my bash aliases.

# License

Copyright (c) 2016 by Steve King <steve@narbat.com>
Permission is given to use and modify this code for any purpose, with or without
attribution. No warranty of any kind is expressed or implied.
