import subprocess
import time
import platform
import sys

def run_command(command, background=False):
    if background:
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(command, shell=True)
        process.wait()

def start(os_type):
    if os_type == 'windows':
        redis_command = "redis-server --port 6322"
        beat_command = "celery -A PIB beat -l info"
        worker_command = "celery -A PIB worker -l info"

    else:
        redis_command = "redis-server --port 6322"
        beat_command = f"python -m celery -A PIB beat"
        worker_command = f"python -m celery -A PIB worker"

    run_command(redis_command, background=True)
    run_command(beat_command, background=True)

    time.sleep(2)

    worker_process = subprocess.Popen(worker_command, shell=True)
    worker_process.wait()

    output, error = worker_process.communicate()
    print("Command Output:")
    print(output.decode("utf-8"))
    print("Command Error:")
    print(error.decode("utf-8"))

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python start_celery.py <os_type>")
        sys.exit(1)

  
    os_type = sys.argv[1].lower()

   
    start(os_type)


