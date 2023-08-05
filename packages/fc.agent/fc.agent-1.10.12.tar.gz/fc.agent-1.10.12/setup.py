from setuptools import setup, find_packages

setup(
    name='fc.agent',
    version='1.10.12',
    author='Flying Circus',
    author_email='mail@flyingcircus.io',
    url='http://github.com/flyingcircusio/fc.agent',
    description=('Local configuration utilities and helper APIs for '
                 'flyingcircus.io system configuration.'),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
    ],
    license='BSD',
    namespace_packages=['gocept'],
    install_requires=[
        'configobj==4.7.2',
        'ipaddress==1.0.14',
        'iso8601==0.1.10',
        'lz4==1.1.0',
        'nagiosplugin==1.2.4',
        'netaddr==0.7.10',
        'python-ldap==2.4.19',
        'pytz==2017.2',
        'PyYaml==5.3.1',
        'requests==2.11.1',
        'setuptools',
        'six==1.10.0',
        'shortuuid==0.4.2',
    ],
    extras_require={
        'test': [
            'freezegun>=0.3'
            'mock>=3.0',
            'pytest>=3.6',
            'pytest-cov',
            'pytest-runner>=2.11,<3dev',
            'pytest-timeout',
        ],
    },
    entry_points={
        'console_scripts': [
            'list-maintenance = gocept.net.maintenance.script:list',
            'localconfig-backy = gocept.net.configure.backy:configure',
            'localconfig-bacula-purge = gocept.net.configure.bacula:purge',
            'localconfig-box-exports = gocept.net.configure.box:exports',
            'localconfig-box-mounts = gocept.net.configure.box:mounts',
            'localconfig-ceph-volumes = gocept.net.configure.ceph:volumes',
            'localconfig-dhcpd = gocept.net.configure.dhcpd:main',
            'localconfig-iptables-rules = gocept.net.configure.iptables:rules',
            'localconfig-kibana = gocept.net.configure.kibana:main',
            'localconfig-kvm-init = gocept.net.configure.kvm:ensure_vms',
            'localconfig-nagios-nodes = gocept.net.configure.nagios:nodes',
            'localconfig-nagioscontacts'
            ' = gocept.net.configure.nagios:contacts',
            'localconfig-postfix-master = '
            'gocept.net.configure.postfix:master',
            'localconfig-puppetmaster'
            '= gocept.net.configure.puppetmaster:main',
            'localconfig-resize2fs-vmroot'
            '= gocept.net.configure.resize2fs:check_grow',
            'localconfig-users = gocept.net.configure.users:main',
            'localconfig-vm-images = gocept.net.configure.vmimages:update',
            'localconfig-zones = gocept.net.configure.zones:update',
            'rbd-clean-old-snapshots '
            '= gocept.net.ceph.utils:clean_old_snapshots',
            'rbd-images = gocept.net.ceph.utils:list_images',
            'request-maintenance = gocept.net.maintenance.script:request',
            'run-maintenance = gocept.net.maintenance.script:run',
            'schedule-maintenance = gocept.net.maintenance.script:schedule',
        ],
    },
)
