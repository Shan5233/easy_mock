import sys
import os
import multiprocessing
path_of_current_file=os.path.abspath(__file__)
path_of_current_dir=os.path.split(path_of_current_file)[0]
_file_name=os.path.basename(__file__)
sys.path.insert(0,path_of_current_dir)

worker_class='sync'
workers=multiprocessing.cpu_count()
chdir=path_of_current_dir
worker_connections=1000
timeout=30
max_requests=2000
graceful_timeout=30
loglevel='info'

reload=True
debug=False
daemon = False
bind="%s:%s"%("172.28.27.133",8888)
access_log_format="%(h)s|%(l)s|%(u)s|%(t)s|%(r)s|%(s)s|%(b)s|%(f)s|%(a)s"
pidfile='%s/run/%s.pid'%(path_of_current_dir,_file_name)
errorlog='%s/logs/%s_error.log'%(path_of_current_dir,_file_name)
accesslog='%s/logs/%s_access.log'%(path_of_current_dir,_file_name)

if __name__=='__main__':
    print(workers)
