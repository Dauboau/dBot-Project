import multiprocessing
import subprocess
import sys
import os
from dotenv import load_dotenv

## .env
load_dotenv()

# SSL
try:
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
except ImportError:
    pass

def run_bot(folder_name):
    
    print(f"[{folder_name}] Starting bot...")
    
    # Configure logging and environment variables
    # Using sys.executable ensures the same Python runtime (.venv) is used
    try:
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=os.path.join(os.getcwd(), folder_name),
            env=os.environ.copy()
        )
        process.communicate()
    except Exception as e:
        print(f"[{folder_name}] Critical Error: {e}")

if __name__ == '__main__':
    
    bot_folders = ['dbot_rpg', 'dbot_mod']
    processes = []
    
    multiprocessing.set_start_method('spawn', force=True)

    # Start a background process for each bot
    for folder in bot_folders:
        p = multiprocessing.Process(target=run_bot, args=(folder,))
        p.start()
        processes.append(p)

    try:
        # Keep the main script alive waiting for child processes
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\nTurning all bots off...")
        for p in processes:
            p.terminate()
            p.join()
        print("All bots turned off.")