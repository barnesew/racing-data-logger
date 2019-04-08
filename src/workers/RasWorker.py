import threading
import time


class RasWorker (threading.Thread):

    def __init__(self, output_stream):
        threading.Thread.__init__(self)
        self.output = output_stream

    def run(self):
        # While loop pushing on-board data
        while True:
            time.sleep(4)
            print("On-Board Data")
