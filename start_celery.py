import subprocess
import time
import platform
import sys

def run_command(command, background=False):
    if background:
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(command, shell=True)
        process.wait()

def start(os_type):
    processes = []

    if os_type == 'windows':
        # redis_command = "redis-server"
        beat_command = "celery -A PIB beat -l info"
        worker_command = "celery -A PIB worker -l info"
    else:
        redis_command = "redis-server --port 6322"
        beat_command = f"python -m celery -A PIB beat"
        worker_command = f"python -m celery -A PIB worker"

    # Start Redis in the background
        processes.append(run_command(redis_command, background=True))

    # Start Celery Beat in the background
    processes.append(run_command(beat_command, background=True))

    # Give some time for Redis and Celery Beat to start
    time.sleep(2)

    # Start Celery Worker
    worker_process = run_command(worker_command, background=False)

    # Add Celery Worker process to the list
    processes.append(worker_process)

    try:
        # Wait for Celery Worker to finish
        worker_process.wait()
    except KeyboardInterrupt:
        # Handle keyboard interrupt to terminate processes
        for process in processes:
            process.terminate()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python start_celery.py <os_type>")
        sys.exit(1)

    os_type = sys.argv[1].lower()
    start(os_type)