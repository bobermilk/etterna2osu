###############################################################################
# madlldlib.dll makefile                               (c) 2004 J.A. Robson
#
# Description: Generates a DLL based on the madlld source
#              (http://www.bsd-dk.dk/~elrond/audio/madlld/)
#
# Instructions:
#	-Download and compile 'libmad' as a Release build (as opposed to Debug).
#	 Read libmad's documentation for details about how to do this.
#
#	-Modify the LIBMAD* variables in the source below to point to the 
#	 approrpriate locations. LIBMADH = directory that 'mad.h' resides in,
#	 LIBMADLIB = path to the compiled libmad library, 'libmad.lib'.
#
#	-You will need nmake (which you can obtain via the Windows .NET SDK).
#	 In the directory of this Makefile, type 'nmake' or 'nmake test' at a 
#	 command-line.
###############################################################################

CPP=cl.exe
LIBEXE=lib.exe

#set these directories to where mad.h and libmad.lib reside
# note: first download libmad source and follow instructions to compile
# using Visual Studio
LIBMADH="libmad\msvc++"
LIBMADLIB="libmad\msvc++\Release\libmad.lib"

#default target (just an alias)
all: madlldlib.dll

#this target relies on bstdfile.lib
madlldlib.dll: bstdfile.lib
	$(CPP) madlldlib.cpp /I$(LIBMADH) /LD /ML $(LIBMADLIB) bstdfile.lib

#create bstdfile library for supporting madlldlib.dll
bstdfile.lib: 
	$(CPP) bstdfile.cpp /ML /c
	$(LIBEXE) bstdfile.obj

#compile test (depends on 'all')
test: all
	$(CPP) test.cpp /I"." /I$(LIBMADH) /ML madlldlib.lib

#compile named pipe example
armslen: all
	$(CPP) armslen.cpp -O2 /I"." /I$(LIBMADH) /ML madlldlib.lib
	$(CPP) armslen_test.cpp -O2

#remove all compiled/unneeded files
clean:
	-@echo Removing compiled/unneeded files...
	-@del bstdfile.lib
	-@del bstdfile.obj
	-@del madlldlib.dll
	-@del madlldlib.exp
	-@del madlldlib.lib
	-@del madlldlib.obj
	-@del test.exe
	-@del test.obj
	-@del armslen.exe
	-@del armslen.obj
	-@del armslen_test.exe
	-@del armslen_test.obj
	-@del *.h~
	-@del *.cpp~

