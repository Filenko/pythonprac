import shutil
import glob
DOIT_CONFIG = {"default_tasks": ["html"]}


def task_html():
    """Make HTML documentation."""
    return {
            'actions': ['sphinx-build -M html docs/source docs/build']
           }


def task_wheel_server():
    return {
        'actions': ['python3 -m build -n -w moodserver'],
        }


def task_wheel_client():
    return {
        'actions': ['python3 -m build -n -w moodclient'],
        }


def task_wheels():
    return {
        'actions': [],
        'task_dep': ['wheel_server', 'wheel_client'],
        }