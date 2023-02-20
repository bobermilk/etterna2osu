using System.Globalization;
using RateChanger.AudioConvert;

namespace RateChanger;

class Program {

    static bool success = true;
    static void Main(string[] args) {
        bool is_audio = bool.Parse(args[0]);

        if (!is_audio) {
            // is_audio, osu file dir, osu file name, msd, rate
            double rate = double.Parse(args[11], CultureInfo.InvariantCulture);
            OsuFileConverter converter = new OsuFileConverter();
            double msd_overall = Math.Round(double.Parse(args[3], CultureInfo.InvariantCulture), 1);
            double msd_stream = Math.Round(double.Parse(args[4], CultureInfo.InvariantCulture), 1);
            double msd_jumpstream = Math.Round(double.Parse(args[5], CultureInfo.InvariantCulture), 1);
            double msd_handstream = Math.Round(double.Parse(args[6], CultureInfo.InvariantCulture), 1);
            double msd_stamina = Math.Round(double.Parse(args[7], CultureInfo.InvariantCulture), 1);
            double msd_jackspeed = Math.Round(double.Parse(args[8], CultureInfo.InvariantCulture), 1);
            double msd_chordjack = Math.Round(double.Parse(args[9], CultureInfo.InvariantCulture), 1);
            double msd_tech = Math.Round(double.Parse(args[10], CultureInfo.InvariantCulture), 1);

            converter.Start(args[1], args[2], rate,
                msd_overall.ToString(CultureInfo.InvariantCulture),
                msd_stream.ToString(CultureInfo.InvariantCulture),
                msd_jumpstream.ToString(CultureInfo.InvariantCulture),
                msd_handstream.ToString(CultureInfo.InvariantCulture),
                msd_stamina.ToString(CultureInfo.InvariantCulture),
                msd_jackspeed.ToString(CultureInfo.InvariantCulture),
                msd_chordjack.ToString(CultureInfo.InvariantCulture),
                msd_tech.ToString(CultureInfo.InvariantCulture),
                true); // last arg is true since we are converting audio files
        } else {
            // is_audio, audio file path, keep_pitch, rate
            bool keepPitch = bool.Parse(args[2]);
            List<double> rates = new List<double>();
            for (int i = 0; i < args.Length - 3; i++) {
                rates.Add(double.Parse(args[i+3], CultureInfo.InvariantCulture));
            }
            ConvertAudio(args[1], rates, keepPitch); // audiopath, rate
        }
    }

    private static void ConvertAudio(string audioFilePath, List<double> rates, bool keepPitch) {
        foreach (double rate in rates) {
            // Convert .mp3 file to .wav
            Codec.MP3ToWave(audioFilePath + ".mp3", audioFilePath + ".wav");

            // Change either the tempo or the rate of the .wav
            string[] args = new string[] { audioFilePath + ".wav", audioFilePath + rate * 100 + ".wav" };
            float rateDeltaInProcent = ((float)rate * 100) - 100;
            AudioStrech.Start(args, rateDeltaInProcent, keepPitch);

            // Convert .wav file to .mp3
            try {
                Codec.WaveToMP3(audioFilePath + rate * 100 + ".wav", audioFilePath + "-" + rate * 100 + ".mp3");
            }
            catch (Exception e) {
                success = false;
            }

            // Remove the .wav files
            File.Delete(audioFilePath + ".wav");
            File.Delete(audioFilePath + rate * 100 + ".wav");
        }
    }
}