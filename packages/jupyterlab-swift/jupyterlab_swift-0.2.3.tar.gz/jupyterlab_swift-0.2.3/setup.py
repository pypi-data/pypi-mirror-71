"""
Setup module for the jupyterlab_swift proxy extension
"""
from setuptools import setup, find_packages

setup_args = dict(
    name             = 'jupyterlab_swift',
    description      = 'A Jupyter Notebook server extension which acts a proxy for a Swift API.',
    version          = '0.2.3',
    author           = 'University of Chicago',
    author_email     = 'dev@chameleoncloud.org',
    url              = 'https://www.chameleoncloud.org',
    license          = 'BSD',
    platforms        = 'Linux, Mac OS X, Windows',
    keywords         = ['jupyter', 'jupyterlab', 'openstack', 'swift'],
    classifiers      = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    packages = find_packages(),
    include_package_data = True,
    data_files = [
        ('etc/jupyter/jupyter_notebook_config.d', [
            'jupyter-config/jupyter_notebook_config.d/jupyterlab_swift.json'
        ]),
    ],
    zip_safe = True,
    install_requires = [
        'notebook'
    ]
)

if __name__ == '__main__':
    setup(**setup_args)
