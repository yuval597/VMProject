from pydantic import BaseModel, ValidationError, field_validator
import json
from src.machine import Machine

class MachineModel(BaseModel):
    name: str
    os: str
    cpu: int
    ram: int

    @field_validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        if v.isdigit():
            raise ValueError("Name cannot be numeric")
        return v
    @field_validator("os")
    def validate_os(cls, v):
        if not v.strip():
            raise ValueError("OS cannot be empty")
        if v.isdigit():
            raise ValueError("OS cannot be numeric")
        return v


def prompt_for_machine ():
    name = input("Enter machine name here: ")
    os = input("Enter required OS here: ")
    cpu = input("Enter required CPU here: ")
    ram = input("Enter required RAM here: ")
    try:
        validated = MachineModel(
        name=name,
        os=os,
        cpu=cpu,
        ram=ram
        )
        machine = Machine(
            name=validated.name,
            os=validated.os,
            cpu=validated.cpu,
            ram=validated.ram
        )
        return machine

    except ValidationError as e:
        print("Invalid input:", e)
        return None
    

def main():
    machines = []
    while True:
        add_machine = input("Add new machine? (y/n): ").lower()
        if add_machine == "n":
            break
        machine = prompt_for_machine()
        if machine:
            machines.append(machine)
    machines_data = [m.to_dict() for m in machines]
    with open("configs/instances.json", "w") as f:
        json.dump(machines_data, f, indent=4)

if __name__ == "__main__":
    main()