import os
import subprocess

class Complier:

    @classmethod
    def complie(cls, source_path, complie_path):

        cmd = [
            'gcc', source_path,
            '-o',  complie_path
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()

        if err:
            err = err.decode()
            return err
        
        return 0
