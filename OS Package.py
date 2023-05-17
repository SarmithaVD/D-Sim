import threading
import time
import random
import queue
import tkinter as tk
from tkinter import messagebox

# Define the maximum number of I/O requests that can be in the queue
MAX_QUEUE_SIZE = 100

# Define a class to represent an I/O request
class IORequest:
    def __init__(self, id, sector, num_sectors, callback=None):
        self.id = id
        self.sector = sector
        self.num_sectors = num_sectors
        self.callback = callback

# Define a class to represent the I/O request queue
class IORequestQueue:
    def __init__(self):
        self.queue = queue.Queue(MAX_QUEUE_SIZE)
        self.sem = threading.Semaphore(1)

    # Add an I/O request to the queue
    def add_io_request(self, request):
        self.sem.acquire()
        self.queue.put(request)
        self.sem.release()

    # Remove an I/O request from the queue
    def remove_io_request(self):
        self.sem.acquire()
        request = self.queue.get()
        self.sem.release()
        return request

    # Check if an I/O request queue is empty
    def is_io_request_queue_empty(self):
        return self.queue.empty()

    # Get the size of an I/O request queue
    def get_io_request_queue_size(self):
        return self.queue.qsize()

# Define a class to represent an I/O scheduler   
class IOScheduler:
    def __init__(self, name, read_threshold=10, write_threshold=100):
        self.name = name
        self.read_threshold = read_threshold
        self.write_threshold = write_threshold
        self.request_queue = IORequestQueue()
        self.listeners = []
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.scheduler).start()

    def stop(self):
        self.running = False

    def schedule_io_request(self, request):
        self.request_queue.add_io_request(request)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)

    def notify_listeners(self, request):
        for listener in self.listeners:
            listener(request)

    def scheduler(self):
        while self.running:
            if not self.request_queue.is_io_request_queue_empty():
                request = self.request_queue.remove_io_request()
                if request.num_sectors <= self.read_threshold:
                    self.handle_read(request)
                elif request.num_sectors >= self.write_threshold:
                    self.handle_write(request)
                else:
                    self.handle_seek(request)

    def handle_read(self, request):
        time.sleep(100)  # Simulate read operation
        if request.callback:
            request.callback(request)
        self.notify_listeners(request)

    def handle_write(self, request):
        time.sleep(100)  # Simulate write operation
        if request.callback:
            request.callback(request)
        self.notify_listeners(request)

    def handle_seek(self, request):
        time.sleep(100)  # Simulate seek operation
        self.request_queue.add_io_request(request)  # Add request back to queue after seek

# Define a class to represent a disk
class Disk:
    def __init__(self, id, num_sectors=100):
        self.id = id
        self.num_sectors = num_sectors
        self.io_scheduler = None
        self.sector_data = {i: None for i in range(num_sectors)}

    def set_io_scheduler(self, io_scheduler):
        self.io_scheduler = io_scheduler

    def get_sector_data(self, sector):
        return self.sector_data.get(sector)

    def set_sector_data(self, sector, data):
        self.sector_data[sector] = data

    def read(self, sector, num_sectors, callback=None):
        if self.io_scheduler:
            request = IORequest(self.id, sector, num_sectors, callback)
            self.io_scheduler.schedule_io_request(request)

    def write(self, sector, data, callback=None):
        if self.io_scheduler:
            request = IORequest(self.id, sector, len(data), callback)
            self.io_scheduler.schedule_io_request(request)
            self.set_sector_data(sector, data)

    def seek_sector(self, sector):
        if sector < 0 or sector >= self.num_sectors:
            raise ValueError("Invalid sector number")
        return sector

# Define a class to represent a GUI for the disk simulation
class DiskSimulationGUI:
    def __init__(self, disk):
        self.disk = disk

        # Initialize the GUI
        self.root = tk.Tk()
        self.root.title(f"Disk {disk.id} Simulation")

        # Create the widgets
        self.sector_label = tk.Label(self.root, text="Select sector:")
        self.sector_entry = tk.Entry(self.root, width=10)
        self.read_button = tk.Button(self.root, text="Read", command=self.read_sector)
        self.write_label = tk.Label(self.root, text="Data to write:")
        self.write_entry = tk.Entry(self.root, width=20)
        self.write_button = tk.Button(self.root, text="Write", command=self.write_sector)
        self.display_button = tk.Button(self.root, text="Display", command=self.display_sector)
        self.output_label = tk.Label(self.root, text="")
        
        # Position the widgets
        self.sector_label.grid(row=0, column=0, padx=5, pady=5)
        self.sector_entry.grid(row=0, column=1, padx=5, pady=5)
        self.read_button.grid(row=0, column=2, padx=5, pady=5)
        self.write_label.grid(row=1, column=0, padx=5, pady=5)
        self.write_entry.grid(row=1, column=1, padx=5, pady=5)
        self.write_button.grid(row=1, column=2, padx=5, pady=5)
        self.display_button.grid(row=2, column=0, padx=5, pady=5)
        self.output_label.grid(row=2, column=1, padx=5, pady=5)

    def read_sector(self):
        sector = int(self.sector_entry.get())
        self.disk.read(sector, 1, self.update_output)

    def write_sector(self):
        sector = int(self.sector_entry.get())
        data = self.write_entry.get()
        self.disk.write(sector, data, self.update_output)

    def display_sector(self):
        sector = int(self.sector_entry.get())
        data = self.disk.get_sector_data(sector)
        if data is None:
            self.output_label.config(text=f"No data in sector {sector}.")
        else:
            self.output_label.config(text=f"Data in sector {sector}: {data}.")

    def update_output(self, request):
        self.display_sector()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Create a Disk object
    disk1 = Disk(1)

    # Create an IOScheduler object with read and write thresholds of 10 and 100 sectors, respectively
    scheduler1 = IOScheduler("Scheduler 1", read_threshold=10, write_threshold=100)
    disk1.set_io_scheduler(scheduler1)

    # Create a DiskSimulationGUI object
    gui = DiskSimulationGUI(disk1)

    #scheduler1.add_listener(gui.display_request)
    # Start the I/O scheduler
    scheduler1.start()

    # Start the GUI main loop
    gui.run()

    # Stop the I/O scheduler when the GUI main loop exits
    scheduler1.stop()