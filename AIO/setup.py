import py2exe  # 这是必须的，导入distutils后，再导入py2exe，会将py2exe命令添加到distutils命令中
from distutils.core import setup  # 这是必须的

includes = ['encodings', 'encodings.*']
options = {'py2exe':
               {'compressed': 1,
                'optimize': 2,
                'ascii': 1,
                'includes': includes,
                'bundle_files': 1,
                'dll_excludes': ['MSVCP90.dll'],
                }
           }

setup(version='1.0.0',
      description='description words',
      name='name',
      options=options,
      zipfile=None,
      windows=[{'script': 'StartAIO.py'  # 需要打包的程序的主文件路径
        }],
      )