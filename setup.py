from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    This function returns a list of requirements from a requirements file.
    """
    requirements = []
    try:
        with open(file_path) as file_obj:
            requirements = file_obj.readlines()
            requirements = [req.strip() for req in requirements if req.strip()]  # Strip whitespace and remove empty lines
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

    # Debug: Print the requirements list
    print(f"Requirements read from file: {requirements}")

    return requirements

# Path to the requirements file
requirements_file_path = 'C:/Users/sachi/OneDrive/Documents/BOTS/nnfx_bot/requirements.txt'

# Path to the wheel file
wheel_file_path = 'file:///C:/Users/sachi/OneDrive/Documents/BOTS/nnfx_bot/TA_Lib-0.4.28-cp311-cp311-win_amd64.whl'

setup(
    name='Forexbot_1',
    version='0.0.2',
    author='Sacheen',
    author_email='sachin.shrestha42@gmail.com',
    packages=find_packages(),
    dependency_links=[wheel_file_path],
    install_requires=get_requirements(requirements_file_path)
)
