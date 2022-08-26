import json
import subprocess
import json

from django.conf import settings

JUDGER_PATH = settings.BASE_DIR + '/temp/judger'
# ANSWER_PATH = 1


class Judger:

    @classmethod
    def judge(cls, exe_path, config):
        result = {}
        option = [
            JUDGER_PATH,
            '-i', config['input_path'],
            '-o', config['output_path'],
            '-a', config['answer_path'],
            '-t', str(config['cpu_time_limit']),
            '-T', str(config['real_time_limit']),
            '-m', str(config['memory_limit']),
            exe_path
        ]
        # 新建子进程运行OJ进行评测，并且重定向输入输出
        proc = subprocess.Popen(option, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if err:
            result['msg'] = err.decode()
            result['state'] = False
        else:
            out = out.decode()
            result = json.loads(out)

            if result['result'] == 'Accepted':
                result['state'] = True
            else:
                result['state'] = False
            
            with open(config['output_path'], 'r') as f:
                result['msg'] = f.read()
        return result
