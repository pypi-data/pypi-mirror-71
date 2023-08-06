from setuptools import setup
setup(
  name = 'superQuery',         
  packages = ['superQuery'],   
  version = '2.61',
  license='MIT',       
  description = 'The Python interface to superQuery',  
  author = 'Eben du Toit',                 
  author_email = 'eben@superquery.io',     
  url = 'https://github.com/superquery/superPy',  
  download_url = 'https://github.com/superquery/superPy/archive/v2.6.tar.gz',    
  keywords = ['DATA', 'SUPERQUERY', 'BIGQUERY'],
  install_requires=[            
      'pymysql',
      'pandas', 
      'IPython',
      'PyDrive'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',    
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
