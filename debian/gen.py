from __future__ import print_function
import sys

# args, consts
simd = sys.argv[1]
cudaver='0-0'
if len(sys.argv) >= 3:
    cudaver = sys.argv[2]
pkgver='0.2.0~xenial'
pkg_name = 'libsqaodc-{simd}'.format(simd=simd)
lib='libsqaodc.so.0'

# control template

control='''
Source: sqaod
Priority: optional
Maintainer: Shinya Morino <shin.morino@gmail.com>
Build-Depends: debhelper (>=9),autotools-dev
Standards-Version: 3.9.6
Section: libs
Homepage: https://github.com/shinmorino/sqaod
Vcs-Git: https://github.com/shinmorino/sqaod.git
Vcs-Browser: https://github.com/shinmorino/sqaod.git

'''[1:]

# virtual package template

control_vpkg = '''
Package: libsqaodc
Provides: libsqaodc.so.0
Section: libs
Architecture: any
Depends: libsqaodc-sse2:amd64 (>= {pkgver}), libsqaodc-avx2:amd64 (>= {pkgver})
Description: sqaodc library

'''[1:].format(pkgver=pkgver)

# libsqaodc-simd

control_lib = '''
Package: libsqaodc-{simd}
Provides: libsqaodc.so.0
Section: libs
Architecture: amd64
Depends:  libgomp1:amd64, libstdc++6:amd64, ${{shlibs:Depends}}
Description: sqaodc library (simd opt = {simd} ).

'''[1:].format(pkgver=pkgver, simd=simd)

# libsqaodc-cuda-x-x

control_cuda='''
Package: libsqaodc-cuda-{cudaver}
Provides: libsqaodc-cuda.so.0
Section: libs
Architecture: amd64
Depends: libsqaodc (>= {pkgver}), cuda-cublas-{cudaver}:amd64, cuda-cudart-{cudaver}:amd64, cuda-curand-{cudaver}:amd64, ${{shlibs:Depends}}
Description: sqaodc CUDA library

'''[1:].format(pkgver=pkgver, cudaver=cudaver)

if simd == 'sse2' :
    # build virtual libsqaodc.
    control += control_vpkg
control += control_lib
if simd == 'sse2' :
     # build libsqaodc-cuda-x-x.
    control += control_cuda

# control
with open('control', 'w') as file:
    file.write(control)

# postinst template

postinst_tmpl='''
#! /bin/sh

set -e
update-alternatives --install /usr/lib/{lib} {lib} /usr/lib/{package}/{lib} {priority}

# dh_installdeb will replace this with shell code automatically
# generated by other debhelper scripts.

#DEBHELPER#

exit 0
'''[1:]

# prerm template
prerm_tmpl='''
#!/bin/sh

set -e

if [ "$1" != "upgrade" ]
then
    update-alternatives --remove {lib} \
    /usr/lib/{package}/{lib}
fi

#DEBHELPER#

exit 0
'''[1:]


# *.install
install='usr/lib/*/libsqaodc.so.* usr/lib/{name}/'.format(name=pkg_name)
with open(pkg_name + '.install', 'w') as file:
    file.write(install)
# *.postinst
with open(pkg_name + '.postinst', 'w') as file:
    priority = 50 if simd == 'sse2' else 20
    postinst=postinst_tmpl.format(package=pkg_name, lib=lib, priority=priority)
    file.write(postinst)
# *.prerm
with open(pkg_name + '.prerm', 'w') as file:
    prerm=prerm_tmpl.format(package=pkg_name, lib=lib)
    file.write(prerm)

# CUDA package
if simd == 'sse2' :
    pkg_name = 'libsqaodc-cuda-{cudaver}'.format(cudaver=cudaver)
    lib='libsqaodc_cuda.so.0'
    
    # install
    install='usr/lib/*/libsqaodc_cuda.so.* usr/lib/{name}'.format(name=pkg_name)
    with open(pkg_name + '.install', 'w') as file:
        file.write(install)

    # *.postinst
    with open(pkg_name + '.postinst', 'w') as file:
        postinst=postinst_tmpl.format(package=pkg_name, lib=lib, priority=30)
        file.write(postinst)
        
    # *.prerm
    with open(pkg_name + '.prerm', 'w') as file:
        prerm=prerm_tmpl.format(package=pkg_name, lib=lib)
        file.write(prerm)
