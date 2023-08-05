"""Resize root filesystem if needed."""

from __future__ import print_function
import os
import re
import subprocess


def log_call(cmdline, **kw):
    print('exec:', ' '.join(cmdline))
    kw.setdefault('stdout', subprocess.PIPE)
    kw.setdefault('stderr', subprocess.PIPE)
    p = subprocess.Popen(cmdline, **kw)
    (out, err) = p.communicate()
    if out:
        print('stdout:', out.strip())
    if err:
        print('stderr:', err.strip())
    if p.returncode > 0:
        raise RuntimeError('returncode', p.returncode, cmdline)
    return out, err


class Disk(object):
    # This part of the resizing code does not know or care about the intended
    # size of the disk. It only checks what size the disk has and then
    # aligns the partition table and filesystems appropriately.
    #
    # The actual sizing of the disk is delegated to the KVM host management
    # utilities and happens independently.

    # 5G disk size granularity -> 2.5G sampling in 512 byte sectors
    FREE_SECTOR_THRESHOLD = int(2.5 * (1 << 30) / 512)

    def __init__(self, dev):
        self.dev = dev

    r_free1 = re.compile(r'largest of which is (\d+) \(.*\) in size')
    r_free2 = re.compile(r'\s(\d+) free sectors')

    def free_sectors(self):
        sgdisk_out = log_call(['sgdisk', '-v', self.dev])[0]
        if 'Problem: The secondary' in sgdisk_out:
            log_call(['sgdisk', '-e', self.dev])
            sgdisk_out = log_call(['sgdisk', '-v', self.dev])[0]
        free = self.r_free1.search(sgdisk_out)
        if not free:
            free = self.r_free2.search(sgdisk_out)
        if not free:
            raise RuntimeError('unable to determine number of free sectors',
                               sgdisk_out)
        return(int(free.group(1)))

    def repartition(self, first_sector):
        log_call([
            'sgdisk', self.dev,
            '-d', '1',
            '-n', '1:{}:0'.format(first_sector),
            '-c', '1:root',
            '-t', '1:8300',
        ])

    def grow_partition(self):
        partx = log_call(['partx', '-rg', self.dev])[0]
        (_npart, first, _last, _sectors, _size, name, _uuid) = \
            partx.splitlines()[0].split()
        if first not in ['4096', '8192', '16384'] or name != 'root':
            raise RuntimeError('Failed to locate root partition', partx)
        self.repartition(int(first))

    def resize_filesystem(self):
        print('Resizing filesystem')
        partx = log_call(['partx', '-rg', self.dev])[0]
        size = int(partx.splitlines()[0].split()[3])   # sectors
        print('New size: {} GiB'.format(size * 512 / (1 << 30)))
        log_call(['resizepart', self.dev, '1', str(size)])
        log_call(['resize2fs', '{}1'.format(self.dev)])

    def grow(self):
        free = self.free_sectors()
        if free > self.FREE_SECTOR_THRESHOLD:
            print('Resize: {} free sectors on {}'.format(free, self.dev))
            self.grow_partition()
            self.resize_filesystem()


def check_grow():
    # expects /etc/local/boot.conf to be sourced into the environment
    d = Disk(os.environ['SYSDISK'])
    d.grow()
