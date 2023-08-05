import pickle
import os
import sys


class ProjectData(object):
    def __init__(self,  project, rel_path):
        self.project  = project
        self.data = {} 
        self.rel_path = rel_path
        full_path = os.path.join(self.project.path, rel_path)
        # if not os.path.exists(full_path):
        #     raise ValueError(f'not a valid path {full_path}')
        self.path = full_path

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def get(self, key, default=None):
        if key in self.data:
            return self.data[key]
        return default

    def save(self):
        if self.path:
            try:
                with open(self.path, 'wb') as f:
                    print(self.path)
                    pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
                    return True
            except:
                print('Writing setting failed')
        else:
            print('Save path does not exists')
        return False

    def load(self):
        try:
            print(self.path)
            if os.path.exists(self.path):
                with open(self.path, 'rb') as f:
                    print("Opening proj")
                    self.data = pickle.load(f)
                    print('Loading the data ', self.path)
                    return True
            else:
                print('Load path does not exists')
        except Exception as e:
            print('Loading setting failed ', e )
        return False

    def reset(self):
        if os.path.exists(self.path):
            os.remove(self.path)
            print('Remove setting pkl file ${0}'.format(self.path))
        self.data = {}
        self.path = None
