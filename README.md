# Disk-Simulator-with-a-GUI

OBJECTIVE: To simulate a disk I/O scheduler and a GUI to interact with it, which can be useful for learning about the basic principles of operating systems and disk I/O scheduling. 

GUI USED: tkinter

The package also imports the following modules:
threading: provides low-level threading API.
time: provides time-related functions.
random: provides random number generation functions.
queue: provides a thread-safe queue data structure.
tkinter: provides GUI toolkit for Python.
tkinter.messagebox: provides a dialog box for displaying messages in the GUI.

The program simulates a disk I/O scheduler and a GUI to interact with it. In operating systems, an I/O scheduler is responsible for managing the requests for input/output operations (such as reading or writing data from/to a disk) issued by multiple processes or threads running concurrently on a system. The I/O scheduler schedules these requests in an efficient manner to optimize the usage of system resources.

The package contains the following classes:
IORequest: represents an I/O request.
IORequestQueue: represents the queue of I/O requests.
IOScheduler: represents the I/O scheduler that processes I/O requests from the queue.
Disk: represents a disk that can read and write data from its sectors, and has an I/O scheduler associated with it.
DiskSimulationGUI: represents a graphical user interface for the disk simulation.
