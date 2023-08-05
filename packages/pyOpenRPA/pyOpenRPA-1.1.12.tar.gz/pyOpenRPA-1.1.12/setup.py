from setuptools import setup, find_packages
import Version
import os
def LongDescriptionRead():
    with open('pyOpenRPA/README.md') as f:
        return f.read()

#Do pyOpenRPA package __init__ __version__ update
Version.pyOpenRPAVersionUpdate("..","pyOpenRPA/__init__.py")

datadir = "pyOpenRPA\\Resources"
datafiles = []
for d, folders, files in os.walk(datadir): 
    for f in files: 
        datafiles.append(os.path.join(d,f))
datadir = "pyOpenRPA\\Orchestrator\\Web"
for d, folders, files in os.walk(datadir): 
    for f in files: 
        datafiles.append(os.path.join(d,f))
datadir = "pyOpenRPA\\Studio\\Web"
for d, folders, files in os.walk(datadir): 
    for f in files: 
        datafiles.append(os.path.join(d,f))
datafile = "pyOpenRPA\\Tools\\RobotRDPActive\\Template.rdp"
datafiles = datafiles + [datafile]
datafile = "pyOpenRPA\\Tools\\RobotScreenActive\\ConsoleStart.bat"
datafiles = datafiles + [datafile]
setup(name='pyOpenRPA',
      version=Version.Get(".."),
      description='First open source RPA platform for business',
      long_description=LongDescriptionRead(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
      ],
      keywords='OpenRPA RPA Robot Automation Robotization',
      url='https://gitlab.com/UnicodeLabs/OpenRPA',
      author='Ivan Maslov',
      author_email='Ivan.Maslov@unicodelabs.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pywinauto>=0.6.6','WMI>=1.4.9','pillow>=6.0.0','keyboard>=0.13.3','pyautogui>=0.9.44','pywin32>=224', 'crypto>=1.4.1'
      ],
      include_package_data=True,
      #data_files = datafiles,
      #package_data = {"pyOpenRPA": datafiles},
      zip_safe=False)