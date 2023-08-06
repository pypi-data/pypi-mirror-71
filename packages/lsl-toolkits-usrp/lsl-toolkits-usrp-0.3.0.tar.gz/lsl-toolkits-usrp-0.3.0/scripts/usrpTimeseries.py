#!/usr/bin/env python

"""
Given a USRP file, plot the time series I and Q data as a function of time.
"""

# Python2 compatibility
from __future__ import print_function, division, absolute_import
 
import os
import sys
import math
import time
import numpy
import argparse

import lsl_toolkits.USRP as usrp
import lsl.reader.errors as errors
from lsl.misc import parser as aph

import matplotlib.pyplot as plt


def main(args):
    fh = open(args.filename, "rb")
    usrp.FRAME_SIZE = usrp.get_frame_size(fh)
    nFramesFile = os.path.getsize(args.filename) // usrp.FRAME_SIZE
    junkFrame = usrp.read_frame(fh)
    srate = junkFrame.sample_rate
    t0i, t0f = junkFrame.time
    fh.seek(-usrp.FRAME_SIZE, 1)
    
    beams = usrp.get_beam_count(fh)
    tunepols = usrp.get_frames_per_obs(fh)
    tunepol = tunepols[0] + tunepols[1] + tunepols[2] + tunepols[3]
    beampols = tunepol

    # Offset in frames for beampols beam/tuning/pol. sets
    offset = int(round(args.skip * srate / junkFrame.payload.data.size * beampols))
    offset = int(1.0 * offset / beampols) * beampols
    fh.seek(offset*usrp.FRAME_SIZE, 1)
    
    # Iterate on the offsets until we reach the right point in the file.  This
    # is needed to deal with files that start with only one tuning and/or a 
    # different sample rate.  
    while True:
        ## Figure out where in the file we are and what the current tuning/sample 
        ## rate is
        junkFrame = usrp.read_frame(fh)
        srate = junkFrame.sample_rate
        t1i, t1f = junkFrame.time
        tunepols = usrp.get_frames_per_obs(fh)
        tunepol = tunepols[0] + tunepols[1] + tunepols[2] + tunepols[3]
        beampols = tunepol
        fh.seek(-usrp.FRAME_SIZE, 1)
        
        ## See how far off the current frame is from the target
        tDiff = t1i - (t0i + args.skip) + (t1f - t0f)
        
        ## Half that to come up with a new seek parameter
        tCorr = -tDiff / 2.0
        cOffset = int(tCorr * srate / junkFrame.payload.data.size * beampols)
        cOffset = int(1.0 * cOffset / beampols) * beampols
        offset += cOffset
        
        ## If the offset is zero, we are done.  Otherwise, apply the offset
        ## and check the location in the file again/
        if cOffset is 0:
            break
        fh.seek(cOffset*usrp.FRAME_SIZE, 1)
    
    # Update the offset actually used
    args.skip = t1i - t0i + t1f - t0f
    offset = int(round(args.skip * srate / junkFrame.payload.data.size * beampols))
    offset = int(1.0 * offset / beampols) * beampols

    # Make sure that the file chunk size contains is an intger multiple
    # of the beampols.
    maxFrames = int(19144/beampols)*beampols

    # Number of frames to integrate over
    toClip = False
    oldAverage = args.plot_range
    if args.plot_range < junkFrame.payload.data.size/srate:		
        toClip = True
        args.plot_range = junkFrame.payload.data.size/srate
    nFrames = int(args.plot_range * srate / junkFrame.payload.data.size * beampols)
    nFrames = int(1.0 * nFrames / beampols) * beampols
    args.plot_range = 1.0 * nFrames / beampols * junkFrame.payload.data.size / srate

    # Number of remaining chunks
    nChunks = int(math.ceil(1.0*(nFrames)/maxFrames))

    # File summary
    print("Filename: %s" % args.filename)
    print("Beams: %i" % beams)
    print("Tune/Pols: %i %i %i %i" % tunepols)
    print("Sample Rate: %i Hz" % srate)
    print("Frames: %i (%.3f s)" % (nFramesFile, 1.0 * nFramesFile / beampols * junkFrame.payload.data.size / srate))
    print("---")
    print("Offset: %.3f s (%i frames)" % (args.skip, offset))
    print("Plot time: %.3f s (%i frames; %i frames per beam/tune/pol)" % (args.plot_range, nFrames, nFrames / beampols))
    print("Chunks: %i" % nChunks)

    # Sanity check
    if nFrames > (nFramesFile - offset):
        raise RuntimeError("Requested integration time+offset is greater than file length")

    # Align the file handle so that the first frame read in the
    # main analysis loop is from tuning 1, polarization 0
    junkFrame = usrp.read_frame(fh)
    b,t,p = junkFrame.id
    while 2*(t-1)+p != 0:
        junkFrame = usrp.read_frame(fh)
        b,t,p = junkFrame.id
    fh.seek(-usrp.FRAME_SIZE, 1)

    # Master loop over all of the file chuncks
    standMapper = []
    for i in range(nChunks):
        # Find out how many frames remain in the file.  If this number is larger
        # than the maximum of frames we can work with at a time (maxFrames),
        # only deal with that chunk
        framesRemaining = nFrames - i*maxFrames
        if framesRemaining > maxFrames:
            framesWork = maxFrames
        else:
            framesWork = framesRemaining
        print("Working on chunk %i, %i frames remaining" % (i, framesRemaining))
        
        count = {0:0, 1:0, 2:0, 3:0}
        tt = numpy.zeros((beampols,framesWork//beampols), dtype=numpy.int64) - 1
        data = numpy.zeros((beampols,framesWork*junkFrame.payload.data.size//beampols), dtype=numpy.csingle)
        
        # Inner loop that actually reads the frames into the data array
        print("Working on %.1f ms of data" % ((framesWork*junkFrame.payload.data.size/beampols/srate)*1000.0))
        t0 = time.time()
        
        for j in range(framesWork):
            # Read in the next frame and anticipate any problems that could occur
            try:
                cFrame = usrp.read_frame(fh, Verbose=False)
            except:
                break
                
            beam,tune,pol = cFrame.id
            aStand = 2*(tune-1) + pol
            
            tt[aStand, count[aStand]] = cFrame.payload.timetag
            if args.instantaneous_power:
                data[aStand, count[aStand]*cFrame.payload.data.size:(count[aStand]+1)*cFrame.payload.data.size] = numpy.abs(cFrame.payload.data)**2
            else:
                data[aStand, count[aStand]*cFrame.payload.data.size:(count[aStand]+1)*cFrame.payload.data.size] = cFrame.payload.data
            
            # Update the counters so that we can average properly later on
            count[aStand] += 1
            
        # The plots:  This is setup for the current configuration of 20 beampols
        fig = plt.figure()
        figsX = int(round(math.sqrt(beampols)))
        figsY = beampols // figsX

        samples = int(oldAverage * srate)
        if toClip:
            print("Plotting only the first %i samples (%.3f ms) of data" % (samples, oldAverage*1000.0))
            
        sortedMapper = sorted(standMapper)
        for i in range(data.shape[0]):
            ax = fig.add_subplot(figsX,figsY,i+1)
            if args.instantaneous_power:
                limits = (-10, 70000)
                if toClip:
                    ax.plot(args.skip + numpy.arange(0,samples)/srate, data[i,0:samples])
                else:
                    ax.plot(args.skip + numpy.arange(0,data.shape[1])/srate, data[i,:])
            else:
                limits = (-32768, 32768)
                if toClip:
                    ax.plot(args.skip + numpy.arange(0,samples)/srate, data[i,0:samples].real, label='I')
                    ax.plot(args.skip + numpy.arange(0,samples)/srate, data[i,0:samples].imag, label='Q')
                else:
                    ax.plot(args.skip + numpy.arange(0,data.shape[1])/srate, data[i,:].real, label='I')
                    ax.plot(args.skip + numpy.arange(0,data.shape[1])/srate, data[i,:].imag, label='Q')
                ax.legend(loc=0)

            if args.mark_frames:
                for j in range(0, samples-cFrame.payload.data.size, cFrame.payload.data.size):
                    ax.vlines(float(j)/srate, limits[0], limits[1], color='k', label='%i' % tt[i,j/cFrame.payload.data.size])

            ax.set_ylim(limits)
            ax.set_title('Beam %i, Tune. %i, Pol. %i' % (beam, i//2+1,i%2))
            ax.set_xlabel('Time [seconds]')
            if args.instantaneous_power:
                ax.set_ylabel('I$^2$ + Q$^2$')
            else:
                ax.set_ylabel('Output Level')
        plt.show()

        # Save image if requested
        if args.output is not None:
            fig.savefig(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='read in USRP files and create a collection of timeseries (I/Q) plots', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument('filename', type=str, 
                        help='filename to plot')
    parser.add_argument('-s', '--skip', type=aph.positive_float, default=0.0, 
                        help='skip period in seconds between chunks')
    parser.add_argument('-p', '--plot-range', type=aph.positive_float, default=0.01, 
                        help='number of seconds of data to show in the I/Q plots')
    parser.add_argument('-i', '--instantaneous-power', action='store_true', 
                        help='plot I*I + Q*Q instead of the raw samples')
    parser.add_argument('-m', '--mark-frames', action='store_true', 
                        help='mark the frame bounaries in time')
    parser.add_argument('-q', '--quiet', dest='verbose', action='store_false', 
                        help='run %(prog)s in silent mode')
    parser.add_argument('-o', '--output', type=str, 
                        help='output file name for timeseries image')
    args = parser.parse_args()
    main(args)
    
