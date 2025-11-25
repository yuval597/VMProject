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
    logger.info("Starting NGINX install script (scripts/install_nginx.sh)")
    try:
        result = subprocess.run(
            ["bash", "scripts/install_nginx.sh"],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info("NGINX install script finished successfully")
        print("Service installing script finished successfully")
        if result.stdout:
            logger.info("NGINX script stdout:\n%s", result.stdout.strip())
        if result.stderr:
            logger.warning("NGINX script stderr:\n%s", result.stderr.strip())
        
    except subprocess.CalledProcessError as e:
        logger.error("NGINX install script failed with exit code %d", e.returncode)
        print("Service installation script failed!")
        if e.stdout:
            logger.error("NGINX script stdout on error:\n%s", e.stdout.strip())
        if e.stderr:
            logger.error("NGINX script stderr on error:\n%s", e.stderr.strip())
        
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
        logger.info("Saved %d machines to configs/instances.json", len(machines))
    install_service()

if __name__ == "__main__":
    main()