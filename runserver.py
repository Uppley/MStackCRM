import os
from os import path
from celery import Celery
from angular_flask import app

extra_dirs = ['angular_flask/static',]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)

def runserver():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, extra_files=extra_files, debug=True)

if __name__ == '__main__':
    runserver()
