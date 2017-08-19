#!/usr/bin/python

import os
import os.path
import shutil
import subprocess

def checkout_or_update(dir):
	urls = [
		[ "http://llvm.org/svn/llvm-project/llvm/trunk"        ,"." ],
		[ "http://llvm.org/svn/llvm-project/cfe/trunk"         ,"./tools/clang" ],
		[ "http://llvm.org/svn/llvm-project/lld/trunk"         ,"./tools/lld" ],
		[ "http://llvm.org/svn/llvm-project/polly/trunk"       ,"./tools/polly" ],
		[ "http://llvm.org/svn/llvm-project/compiler-rt/trunk" ,"./projects/compiler-rt" ],
		[ "http://llvm.org/svn/llvm-project/libcxx/trunk"      ,"./projects/libcxx" ],
		[ "http://llvm.org/svn/llvm-project/libcxxabi/trunk"   ,"./projects/libcxxabi" ],
	]

	for url in urls:
		checkout_dir = os.path.normpath(os.path.join(dir, url[1]))
		svn_dir = os.path.normpath(os.path.join(checkout_dir, ".svn"))
		
		if os.path.isdir(svn_dir):
			command = " ".join(['svn', 'up ', checkout_dir])
		else:
			command = " ".join(['svn', 'co ', url[0], checkout_dir])
		print command
		result = subprocess.call(command, shell=True)

def get_builddir(prefix, buildmethod, cpuarch):
	elements = []
	if prefix:
		elements.append(prefix)
	if buildmethod:
		elements.append(buildmethod)
	if cpuarch:
		elements.append(cpuarch)
		
	builddir = "-".join(elements)
	return os.path.normpath(builddir)
	
def run_cmake():
	cmake_path = "/Applications/CMake.app/Contents/bin/cmake"

	command = " ".join([cmake_path, ".."])
	print command
	result = subprocess.call(command, shell=True)
	
def run_make():
	command = " ".join(["make", "-j 4"])
	print command
	result = subprocess.call(command, shell=True)

def main():
	dir = "llvm"
	prefix = "build"
	buildmethod = "make"
	cpuarch = "x86"

	checkout_or_update(dir)
	
	os.chdir(dir)

	builddir = get_builddir(prefix, buildmethod, cpuarch)
	if os.path.isdir(builddir):
		shutil.rmtree(builddir)
	
	os.makedirs(builddir)
	os.chdir(builddir)
	
	run_cmake()
	run_make()

main()
