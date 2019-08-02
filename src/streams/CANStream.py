import threading
import time


class CanWorker (threading.Thread):

    def __init__(self, output_stream):
        threading.Thread.__init__(self)
        self.output = output_stream

    def run(self):
        # While loop pushing CAN data
        while True:
            time.sleep(1)
            print("CAN Data")
