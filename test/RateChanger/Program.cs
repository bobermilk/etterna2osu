using System.Globalization;
using RateChanger.AudioConvert;

namespace RateChanger;

class Program {

    static bool success = true;

    // osu file dir, osu file name, audio file path, rate
    static void Main(string[] args) {
        double rate = double.Parse(args[3], CultureInfo.InvariantCulture);
        OsuFileConverter converter = new OsuFileConverter();
        ConvertAudio(args[2], rate); //audiopath, rate
        converter.Start(args[0], args[1], rate, true);
    }

    private static void ConvertAudio(string audioFilePath, double rate) {
        // Convert .mp3 file to .wav
        Codec.MP3ToWave(audioFilePath + ".mp3", audioFilePath + ".wav");

        // Change either the tempo or the rate of the .wav
        string[] args = new string[] { audioFilePath + ".wav", audioFilePath + rate * 100 + ".wav" };
        float rateDeltaInProcent = ((float)rate * 100) - 100;
        bool keepPitch = false;
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
