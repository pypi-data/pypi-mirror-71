from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget
import sys
from os.path import dirname, join, exists
import pathlib
# from .detection_client import SingleThreadedClient
from .detection_flask import FlaskClient
class InferenceApi(QWidget):
 
    objectFound = pyqtSignal(list, str)  # (list, str) as [x,y,w,h]] and label
    objectsFound = pyqtSignal(tuple)  # tuple of (list, list) with BB and corresponding labels
    errorWithInference = pyqtSignal(str, str) #error message

    def __init__(self, host, port, project,*args, **kwargs):
        super(InferenceApi, self).__init__(*args, **kwargs)
        self.host = host
        self.port = port
        self.project = project


    def setHost(self, value):
        self.host = value
        # print("self.host", self.host)

    def setPort(self, value):
        self.port = value

    def setProject(self, value):
        self.project = value
        # print("self.port", self.port)
        #
    def detectObjects(self, image_path):
        print('detectObjects is called')
        # start_time = time.time()
        if image_path is None:
            self.errorWithInference.emit(u'Could not detect boxes', 'Image path is None' )
            return
        # client = SingleThreadedClient( self.host, self.port)
        client = FlaskClient(self.host, self.port, self.project)
        tup = client.sendDetectionImage(image_path)
        if not tup:
            self.errorWithInference.emit(u'Could not detect boxes', 'Server stopped replying ' )
            return
        (boxes, labels_words, scores) =  tup
        self.objectsFound.emit((boxes, labels_words, scores))
        # else:
            # self.errorWithInference.emit(u'Could not detect boxes', 'Server is broken' )
        # print("Time: {:.2f} s / img".format(time.time() - start_time))

        return
