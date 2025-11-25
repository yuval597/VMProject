# This file defines the MachineModel (for validation) and Machine (final machine object).
# MachineModel = the actual object we create and save, based on the validated data

import logging

logger = logging.getLogger(__name__)

# Machine class - represents a final machine in the system
# It stores machine data after validation and can turn itself into a dictionary for saving to JSON
class Machine:
    def __init__(self, name, os, cpu, ram):
        self.name = name
        self.os = os
        self.cpu = cpu
        self.ram = ram
        
        logger.info(f"Machine created:{self.name}(OS={self.os},CPU={self.cpu},RAM={self.ram})")

# Convert Machine object into a dictionary (used when saving to JSON file)
    def to_dict(self):
        return {
            "name":self.name,
            "os":self.os,
            "cpu":self.cpu,
            "ram":self.ram

        }
        