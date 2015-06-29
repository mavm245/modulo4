* hide/show. This commands hide/show the rootkit from lsmod(actually from /proc/modules).
* hsport PORT/ssport PORT. Hides(hsport) connection which have PORT as their source port, or "unhides it"(ssport) if it was previously hidden.
* hdport PORT/sdport PORT. Same as above but using destination port instead of source.
* hpid PID/spid PID. Hides or "unhides" a process that has PID as its pid. This is done by hooking the /proc readdir pointer.
* huser USER/suser USER. This commands hide or "unhide" a logged in user, so that who or other similar commands wont indicate USER is logged in the system. This is done by hooking /var/run/utmp.
*root PID. This makes the process identified by PID to contain uid 0 and gid 0. This is kind of dirty but works well; the credentials struct from the init process is copied to the process identified by PID.

$ echo "hsport 22" > /proc/buddyinfo

//Referencias

~http://average-coder.blogspot.mx/2011/12/linux-rootkit.html
~http://commons.oreilly.com/wiki/index.php/Network_Security_Tools/Modifying_and_Hacking_Security_Tools/Fun_with_Linux_Kernel_Modules
~https://books.google.com.mx/books?id=RSOrAQAAQBAJ&pg=PT190&lpg=PT190&dq=hiding+from+netstat&source=bl&ots=rO6C9sbYIH&sig=qoNiODe8nyXoVUh0qX4ZerQXFMo&hl=es-419&sa=X&ei=VnOQVaW7N4u2sAWzoIKwAQ&ved=0CFAQ6AEwBg#v=onepage&q=hiding%20from%20netstat&f=false
