/****************************************************************************
 * test                                               (c) 2004 J. A. Robson
 * 
 * test.cpp -- Primary example to using the madlldlib.dll interface
 *
 * This is an extremely simple example that defines a callback, handles a 
 * few command line parameters (i.e. file to convert, output format), and
 * calls the DLL's main function CbMpegAudioDecoder() to process the MP3 
 * file. See the inline comments for details. For more details about 
 * CbMpegAudioDecoder, see comments in madlldlib.cpp.
 *
 * To compile, see 'Makefile' comments.
 ****************************************************************************/

#include <stdio.h>
#include <string.h>
#include <madlldlib.h>

/*
 * The callback function is used for reporting purposes and
 * garnering information about the source MP3 file. This callback 
 * simply prints information to STDOUT, but it usually would be 
 * used to increment a counter, calculate a percentage, or advance
 * a status bar.
 */
void __stdcall mycb (unsigned long fcnt, unsigned long bcnt, struct mad_header *mhdr) {

	/*
	 * If this is the first iteration (frame count is one)
	 * then print out the MP3 layer information. Using this logic
	 * one can retrieve information about the MP3 file, such as 
	 * channels, layer, etc., that might be useful to the calling
	 * code.
	 */	
	if (fcnt == 1) {
		printf("frame:%d, tot. bytes:%d, layer:%d, mode:%d\n",
				fcnt,
				bcnt,
				mhdr->layer, 
				mhdr->mode);
	}
	else {
		printf("frame:%d, tot. bytes:%d\n",fcnt,bcnt);
	}
	
}

/* 
 * Program entry point
 * note: argv error checking is minimal (to say the least) 
 */
void main(int argc, char *argv[]) {

	
	/* used for concatentating the appropriate 
	 * extension to output file */
	char *outf;
	char *outfx;
	outf="";
	outfx=".";
	
	/* statun/error reporting */
	char statmsg[256];
	int status;
	
	/* call the decoding function with input file,
	 * output file, and callback (defined above). 
	 *
	 * Note on return values: CbMpegAudioDecoder() 
	 * returns 0 if successful, non-zero if it has 
	 * problems opening/reading the files passed. 
	 * libmad, the library concerned with the actual 
	 * MP3 decoding, passes detailed error information 
	 * specific to the MP3 conversion, which gets 
	 * set into the string statmsg. 
	 * (CbMpegAudioDecoder() returns a non-zero 
	 * status at this time as well.) So the upshot 
	 * of this is that both indicators handle 
	 * slightly overlapping but different events,
	 * and are hence both useful. */

	//wav use 1
	//pcm use 0
	status = CbMpegAudioDecoder(argv[1], "etterna_offset.raw", 0, statmsg, mycb);


	/* relay any errors */	
	printf("%s", statmsg);		

	return;	

}



