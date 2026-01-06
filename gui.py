import threading
from gui import *
from client import *
from interface import *

if __name__ == "__main__":

    app = QApplication()
    window = WindowGui()
    window.show()

    signal = ReceiveSignals()
    signal.new_message.connect(window.display_received)

    threading.Thread(target = initconnection, daemon = True).start()
    threading.Thread(target = qreceive_listener, args = (signal,receive_queue), daemon = True).start()

    
