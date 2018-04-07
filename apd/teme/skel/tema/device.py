"""
This module represents a device.

Computer Systems Architecture Course
Assignment 1
March 2018
"""

from threading import Event, Thread, Lock
from multiprocessing.dummy import Pool as ThreadPool
from barrier import ReusableBarrierCond

class Device(object):
    """
    Class that represents a device.
    """

    def __init__(self, device_id, sensor_data, supervisor):
        """
        Constructor.

        @type device_id: Integer
        @param device_id: the unique id of this node; between 0 and N-1

        @type sensor_data: List of (Integer, Float)
        @param sensor_data: a list containing (location, data) as measured by this device

        @type supervisor: Supervisor
        @param supervisor: the testing infrastructure's control and validation component
        """
        self.device_id = device_id
        self.sensor_data = sensor_data
        self.supervisor = supervisor

        self.lock_locations = {}
        self.scripts = []
        self.neighbors = None
        self.timepoint_start = Event()
        self.timepoint_start.clear()
        self.devices_done = None
        self.thread = DeviceThread(self)
        self.thread.start()

    def __str__(self):
        """
        Pretty prints this device.

        @rtype: String
        @return: a string containing the id of this device
        """
        return "Device %d" % self.device_id

    def setup_devices(self, devices):
        """
        Setup the devices before simulation begins.

        @type devices: List of Device
        @param devices: list containing all devices
        """
        if self.device_id == 0:
            devices_done = ReusableBarrierCond(len(devices))
            for location in self.sensor_data:
                self.lock_locations[location] = Lock()


            for device in devices:
                for location in device.sensor_data:
                    if not location in self.lock_locations:
                        self.lock_locations[location] = Lock()

            for device in devices:
                device.lock_locations = self.lock_locations
                device.devices_done = devices_done

    def assign_script(self, script, location):
        """
        Provide a script for the device to execute.

        @type script: Script
        @param script: the script to execute from now on at each timepoint; None if the
            current timepoint has ended

        @type location: Integer
        @param location: the location for which the script is interested in
        """
        if script is not None:
            self.scripts.append(((script, location)))
        else:
            self.timepoint_start.set()

    def get_data(self, location):
        """
        Returns the pollution value this device has for the given location.

        @type location: Integer
        @param location: a location for which obtain the data

        @rtype: Float
        @return: the pollution value
        """
        return self.sensor_data[location] if location in self.sensor_data else None

    def set_data(self, location, data):
        """
        Sets the pollution value stored by this device for the given location.

        @type location: Integer
        @param location: a location for which to set the data

        @type data: Float
        @param data: the pollution value
        """
        if location in self.sensor_data:
            self.sensor_data[location] = data

    def shutdown(self):
        """
        Instructs the device to shutdown (terminate all threads). This method
        is invoked by the tester. This method must block until all the threads
        started by this device terminate.
        """
        self.thread.join()

class DeviceThread(Thread):
    """
    Class that implements the device's worker thread.
    """

    def __init__(self, device):
        """
        Constructor.

        @type device: Device
        @param device: the device which owns this thread
        """
        Thread.__init__(self, name="Device Thread %d" % device.device_id)
        self.device = device
    def run(self):

        while True:
            self.device.neighbors = self.device.supervisor.get_neighbours()
            if self.device.neighbors is None:
                break

            self.device.timepoint_start.wait()
            self.device.timepoint_start.clear()

            nb_tasks = len(self.device.scripts)
            if nb_tasks > 8:
                nb_tasks = 8
            elif nb_tasks == 0:
                self.device.devices_done.wait()
                continue

            pool = ThreadPool(nb_tasks)
            new_pool_list = [(self.device, ) + tup for tup in self.device.scripts]
            pool.map(run_script, new_pool_list)

            pool.close()
            pool.join()

            self.device.devices_done.wait()

def run_script((device, script_to_run, location)):
    """
    function that implements the algorithm for running scripts

    @type device: Device
    @param device: the device which owns this function

    @type script_to_run: Script
    @param script_to_run: the script used

    @type location: Integer
    @param location: the location received with the script
    """
    script_data = []
    device.lock_locations[location].acquire()

    for dev in device.neighbors:
        data = dev.get_data(location)
        if data is not None:
            script_data.append(data)

    data = device.get_data(location)
    if data is not None:
        script_data.append(data)

    if script_data != []:
        result = script_to_run.run(script_data)

        for dev in device.neighbors:
            dev.set_data(location, result)

        device.set_data(location, result)
    device.lock_locations[location] .release()
