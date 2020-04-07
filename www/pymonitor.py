#-*-coding:utf-8 -*-
__author__ = 'Vehicle Guo'

import os, sys, time, subprocess

from watchdog.observers import  Observer
from watchdog.events import FileSystemEventHandler


def log(s):
    print('[Monitor] %s' % s)

#检查.py文件是否有改动
class MyFileSystemEventHander(FileSystemEventHandler):

    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' % event.src_path)
            self.restart()

command = ['echo', 'ok']
process = None
#杀死进程
def kill_process():
    global process
    if process:
        log('Kill process [%s]...' % process.pid)
        process.kill()
        process.wait()
        log('Process ended with code %s.' % process.returncode)
        process = None
#启动服务
def start_process():
    global process, command
    log('Start process %s...' % ' '.join(command))
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
#重启操作
def restart_process():
    kill_process()
    start_process()

#逻辑代码 判断是否改动 改动则重启
def start_watch(path, callback):
    observer = Observer()
    observer.schedule(MyFileSystemEventHander(restart_process), path, recursive=True)
    observer.start()
    log('Watching directory %s...' % path)
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
#主程序
if __name__ == '__main__':
    argv = sys.argv[1:]
    print(argv)
    if not argv:
        print('Usage: ./pymonitor app.py')
        exit(0)
    argv.insert(0, 'python3')
    # if argv[0] != 'python3':
    #     argv.insert(0, 'python')
    # else:
    #     argv.insert(0, 'python3')
    command = argv
    path = os.path.abspath('.')
    start_watch(path, None)