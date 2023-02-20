using System.Globalization;
using RateChanger.AudioConvert;

namespace RateChanger;

class Program {

    static bool success = true;

    // osu file dir, osu file name, audio file path, keep_pitch, rate, msd
    static void Main(string[] args) {
        bool keepPitch = bool.Parse(args[3]);
        double rate = double.Parse(args[4], CultureInfo.InvariantCulture);
        double msd = Math.Round(double.Parse(args[5], CultureInfo.InvariantCulture), 1);
        
        OsuFileConverter converter = new OsuFileConverter();
        ConvertAudio(args[2], rate, keepPitch); //audiopath, rate
        converter.Start(args[0], args[1], rate, true, msd);  //last arg is true since we are converting audio files
    }

    private static void ConvertAudio(string audioFilePath, double rate, bool keepPitch) {
        // Convert .mp3 file to .wav
        Codec.MP3ToWave(audioFilePath + ".mp3", audioFilePath + ".wav");

        // Change either the tempo or the rate of the .wav
        string[] args = new string[] { audioFilePath + ".wav", audioFilePath + rate * 100 + ".wav" };
        float rateDeltaInProcent = ((float)rate * 100) - 100;
        AudioStrech.Start(args, rateDeltaInProcent, keepPitch);

        // Convert .wav file to .mp3
        try {
            Codec.WaveToMP3(audioFilePath + rate * 100 + ".wav", audioFilePath + rate * 100 + ".mp3");
        }
        catch (Exception e) {
            success = false;
        }

        // Remove the .wav files
        File.Delete(audioFilePath + ".wav");
        File.Delete(audioFilePath + rate * 100 + ".wav");
    }
}