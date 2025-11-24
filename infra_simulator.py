from pydantic import BaseModel, ValidationError, field_validator
import json
from src.machine import Machine
import subprocess
import logging

LOG_FILE = "logs/provisioning.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

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
        return validated.model_dump()

    except ValidationError as e:
        logger.error("Invalid input: %s", e)
        return None
    

def install_service():
    try:
        result = subprocess.run(
            ["bash", "scripts/install_nginx.sh"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Service installing script finished successfully")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Service installing script failed!")
        print("Exit code", e.returncode)
        print("strerr", e.stderr)

def main():
    logger.info("Provisioning started")
    machines = []
    while True:
        add_machine = input("Add new machine? (y/n): ").lower()
        if add_machine == "n":
            break
        machine_data = prompt_for_machine()
        if machine_data:
            machines.append(machine_data)
            print(f"{machine_data['name']} added successfully")
    with open("configs/instances.json", "w") as f:
        json.dump(machines, f, indent=4)
        logger.info("Provisioning finished, saved %d machines", len(machines))
    install_service()

if __name__ == "__main__":
    main()