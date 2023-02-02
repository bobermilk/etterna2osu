using ManagedBass;
using ManagedBass.Enc;

namespace OffsetCalculator;

class Program {
    private static string target;
    static void Main(string[] args)
    {

        // this likely doesn't help us but also doesn't seem to cause any issues or any cpu increase.
        Bass.UpdatePeriod = 5;

        // reduce latency to a known sane minimum.
        Bass.DeviceBufferLength = 10;
        Bass.PlaybackBufferLength = 100;

        // ensure there are no brief delays on audio operations (causing stream stalls etc.) after periods of silence.
        Bass.DeviceNonStop = true;

        // without this, if bass falls back to directsound legacy mode the audio playback offset will be way off.
        Bass.Configure(ManagedBass.Configuration.TruePlayPosition, 0);

        // For iOS devices, set the default audio policy to one that obeys the mute switch.
        Bass.Configure(ManagedBass.Configuration.IOSMixAudio, 5);

        // Always provide a default device. This should be a no-op, but we have asserts for this behaviour.
        Bass.Configure(ManagedBass.Configuration.IncludeDefaultDevice, true);

        // Enable custom BASS_CONFIG_MP3_OLDGAPS flag for backwards compatibility.
        Bass.Configure((ManagedBass.Configuration)68, 1);

        // Disable BASS_CONFIG_DEV_TIMEOUT flag to keep BASS audio output from pausing on device processing timeout.
        // See https://www.un4seen.com/forum/?topic=19601 for more information.
        Bass.Configure((ManagedBass.Configuration)70, false);
        if (Bass.Init())
        {
            const BassFlags flags = BassFlags.Decode;

            if (args.Length == 0) {
                target = "audio.mp3";
            } else {
                target = Path.GetFullPath(args[0]);           
            }
        //https://github.com/Quaver/Quaver/blob/ui-redesign/Quaver.Shared/Screens/Edit/UI/Playfield/Waveform/EditorPlayfieldWaveform.cs#L113
        if (File.Exists(target))
        {
            int Stream = Bass.CreateStream(target, 0, 0, flags);
            //long TrackByteLength = Bass.ChannelGetLength(Stream);
            //double TrackLengthMiliSeconds = Bass.ChannelBytes2Seconds(Stream, TrackByteLength) * 1000.0;
            //string audioext = Path.GetExtension(target);


            BassEnc.EncodeStart(Stream, CommandLine: "osu_offset.raw", EncodeFlags.PCM | EncodeFlags.AutoFree, null);
            var buffer = new byte[16 * 1024];
            while (Bass.ChannelGetData(Stream, buffer, buffer.Length) > -1)
            {
            }
            Bass.StreamFree(Stream);
        }
        else
        {
            Console.Write(-1);
        }
        Bass.Free();
    } 
    else
    {
        Console.WriteLine("BASS failed to initialize... unpog :(");
    }
}
}