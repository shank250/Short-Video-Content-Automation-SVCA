import threading
import time
import sys

def processing(stop_event):
    while not stop_event.is_set():
        for c in "\ /":
            sys.stdout.write('\r' + "Processing " + c)
            sys.stdout.flush()
            time.sleep(0.1)

def do_calculation():
    time.sleep(5)

stop_event = threading.Event()
processing_thread = threading.Thread(target=processing, args=(stop_event,))
processing_thread.start()

do_calculation()
stop_event.set()
print("\nDone!")