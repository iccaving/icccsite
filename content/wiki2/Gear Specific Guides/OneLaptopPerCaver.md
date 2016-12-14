Date: 01-01-2000
Title: OneLaptopPerCaver
Type: wiki


Survex on OLPC / XO
-------------------

### "One Laptop Per Caver"

My XO was croaking a little after various fiddles that had already taken
place, so I reflashed direct from a USB stick (just download two files,
plugin & reboot...): <http://wiki.laptop.org/go/Activated_Upgrade>

Changed over to XFCE4 via these instructions:
<http://wiki.laptop.org/go/Xfce>

Notes on OLPC/XFCE: To mount drive, open XFCE file manager (central
'folder' icon in dock) and click on device in left pane.

Got working cavern+aven binaries direct from Ubuntu Hardy Heron
distribution via:





-   cp -a /usr/bin/cavern /usr/bin/aven
    /usr/share/survex /media/memorystick...

get the /usr/share/survex in its rightful place (need to be root),
otherwise will complain about missing language info.

You now have working cavern!

Compiles mig.sxv (3291 stations, 3316 shots) in \~2 or 3 s.





Aven
----

Needs

-   yum install wxGTK

(Note caps!)

Hmm, unfortunately this provides on the OLPC the 2.8 version of the
libraries, whereas the Ubuntu aven links to 2.6. What now?





xcaverot
--------

Alas even xcaverot is imcompatible: loads fonts in the old style
X-server way, which have been removed from the OLPC to slim down X11.





------------------------------------------------------------------------





Option Z
--------

Install Debian / Ubuntu.
