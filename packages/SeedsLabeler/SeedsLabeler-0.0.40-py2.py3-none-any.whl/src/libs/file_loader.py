import sys, os
from .ustr import ustr
from .image import Image
from .constants import XML_EXT, TXT_EXT
try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
class FileLoader(object):

    def __init__(self, project):
        self.project = project

    def scanAllImages(self):
        '''scans all images in the project data file and project directories
            if images from directory are in the file, load them from the file
            otherwise, create new image object
            split images in verified, non-veriffied. Just created images are non-verified.
        '''
        # import  pdb;
        # pyqtRemoveInputHook(); pdb.set_trace()
        extensions = ['.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        verified_images = {}
        non_verified_images = {}
        names = []
        print(self.project.all_image_names)
        for root, dirs, files in os.walk(self.project.path):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    path = os.path.join(root, file)
                    # print(path)
                    full_path = ustr(os.path.abspath(path))
                    relative_path = os.path.relpath(full_path, self.project.path) 
                    names.append(relative_path)
                    # print("Restored all image names length is", len(self.project.all_image_names))
                    print(path)
                    if relative_path not in self.project.all_image_names:
                        print("NEW IMAGE")
                        #we have a new image which is not in the project data file 
                        new_image = Image(full_path, relative_path) 
                        non_verified_images[relative_path] = new_image 
                    else:
                        #do lookup
                        retrieved_image, is_ver = self.project.get_image_from_name(relative_path)
                        retrieved_image.path = os.path.join(self.project.path, relative_path)

                        #if project was moved, we might need to change the absolute path
                        if retrieved_image.label_file and not os.path.exists(retrieved_image.label_file.path):
                            prefix = XML_EXT if self.project.is_VOC_format else TXT_EXT
                            basename = os.path.splitext(retrieved_image.path)[0]
                            print(basename)
                            
                            #if cannot find annotation, try to change path
                            if os.path.exists(os.path.join(basename + prefix)):
                                retrieved_image.label_file.path = os.path.join(basename + prefix)
                           
                            else:
                                #otherwise, set no label file
                                retrieved_image.label_file = None

                        if retrieved_image and is_ver and retrieved_image.label_file:
                            verified_images[relative_path] = retrieved_image
                        elif retrieved_image and not is_ver:
                            non_verified_images[relative_path] = retrieved_image
                            # non_verified_images.append(retrieved_image)
                        else:

                            #there is an error/inconsistency:
                            #image was moved and label file was lost
                            new_image = Image(full_path, relative_path) 
                            non_verified_images[relative_path] = new_image 

        self.project.non_verified_images = non_verified_images
        self.project.verified_images = verified_images
        self.project.all_image_names = names
        #TODO: sort them??
        # images.sort(key=lambda x: x.lower())

    def check_xml(self, filePath):
        pass
