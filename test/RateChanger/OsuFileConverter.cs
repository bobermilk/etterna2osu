using System.Globalization;

namespace RateChanger
{
    class OsuFileConverter
    {
        CultureInfo usCulture = CultureInfo.CreateSpecificCulture("en-US");
        private double _rate = 0.0;
        private int _audioOffset = 0;

        // Get line, rate-change one int property then return new line
        private string TimingConvert(string data, int index, char seperator)
        {
            string returnString = "";

            // Split string into ints, rate change and add offset
            string[] nums = data.Split(seperator);
            var i = (int)Math.Round(double.Parse(nums[index], usCulture) / _rate) + _audioOffset;
            nums[index] = i.ToString(usCulture);

            // Asigning overwritten data to new file
            for (int x = 0; x < nums.Length; x++)
            {
                if (x != 0) returnString += seperator;
                returnString += nums[x];
            }

            return returnString;
        }

        // Get line, rate-change one double property (no offset) then return new line
        private string TimingConvert(string data, int index, char seperator, bool isDouble)
        {
            if (!isDouble)
            {
                TimingConvert(data, index, seperator);
            }

            string returnString = "";

            // Split string into ints, rate change and add offset
            string[] nums = data.Split(seperator);
            var i = (double.Parse(nums[index], usCulture) / _rate);
            nums[index] = i.ToString(usCulture);

            // Asigning overwritten data to new file
            for (int x = 0; x < nums.Length; x++)
            {
                if (x != 0) returnString += seperator;
                returnString += nums[x];
            }

            return returnString;
        }

        // Get audio file name
        public string getAudioName(string filePath, double rate)
        {
            string audioName = "";

            string[] lines = File.ReadAllLines(@filePath);
            string line = lines.First(x => x.Contains("AudioFilename:"));
            audioName = line.Split(':')[1].Trim(' ');

            return audioName;
        }

        // Convert the .osu map, returns if successful
        public bool Start(string filePath, string fileName, double rate, string msd_overall, string msd_stream, string msd_jumpstream, string msd_handstream, string msd_stamina, string msd_jackspeed, string msd_chordjack, string msd_tech, bool useOffset)
        {
            _rate = rate;
            _audioOffset = useOffset ? 80 : 0;

            string[] lines = File.ReadAllLines(@filePath);
            string[] newLines = new string[lines.Length];
            string sections = "";
            string eventSection = "";
            string originalAudioFile = "error";
            int mode = 0;

            // Iterate through the whole file, line by line.
            for (int i = 0; i < lines.Length; i++)
            {
                var line = lines[i];
                var newLine = "";

                // Skip line if empty
                if (line == "")
                {
                    continue;
                }

                // Remember which section we have arrived in the file, then skip line
                if (line.StartsWith("["))
                {
                    sections = lines[i];
                    newLines[i] = lines[i];
                    continue;
                }

                switch (sections)
                {
                    case "[General]":
                        if (line.Contains("AudioFilename:"))
                        {
                            originalAudioFile = lines[i].Split(':')[1].Trim(' ');
                            string audioName = originalAudioFile.Remove(originalAudioFile.Length - 4);
                            newLine = "AudioFilename: " + audioName + "-" + rate * 100 + ".mp3";
                        }
                        if (line.Contains("PreviewTime:"))
                        {
                            string[] a = lines[i].Split(' ');
                            int b;
                            if (int.TryParse(a[1], out b))
                            {
                                b = (int)Math.Round(b / rate);
                            }
                            else
                            {
                                return false;
                            }
                            newLine = "PreviewTime: " + b.ToString(usCulture);
                        }
                        if (line.Contains("Mode:"))
                        {
                            string[] a = lines[i].Split(' ');
                            int b;
                            if (int.TryParse(a[1], out b))
                            {
                                mode = b;
                            }
                            else
                            {
                                return false;
                            }
                            newLine = "Mode: " + b.ToString(usCulture);
                        }
                        break;
                    case "[Editor]":
                        if (line.Contains("Bookmarks:"))
                        {
                            string[] bookmarks = line.Split(':')[1].Split(',');
                            newLine = "Bookmarks: ";
                            for (int x = 0; x < bookmarks.Length; x++)
                            {
                                if(bookmarks[x].Trim() == "")
                                {
                                    continue;
                                }

                                int book = int.Parse(bookmarks[x], usCulture);
                                if (x != 0) newLine += " ,";
                                newLine += (int)Math.Round(book / rate) + _audioOffset;
                            }
                        }
                        if (mode != 3)
                        {
                            if (lines[i].Contains("SliderMultiplier:"))
                            {
                                newLine = "SliderMultiplier:" + (double.Parse(lines[i].Split(':')[1], usCulture) * rate).ToString(usCulture);
                            }
                            else if (lines[i].Contains("ApproachRate:"))
                            {
                                newLine = "ApproachRate:" + (double.Parse(lines[i].Split(':')[1], usCulture) / rate).ToString(usCulture);
                            }
                            else if (lines[i].Contains("SliderTickRate:"))
                            {
                                newLine = "SliderTickRate:" + (double.Parse(lines[i].Split(':')[1], usCulture) / rate).ToString(usCulture);
                            }
                        }
                        break;
                    case "[Metadata]":
                        if (lines[i].Contains("Version:"))
                        {
                            if (rate != 1.0) {
                                string[] bleh = line.Split(null);
                                bleh[2] = rate + "x";
                                bleh[4] = msd_overall;
                                string last_bleh=bleh[bleh.Length-1];
                                if (last_bleh.Contains("(")) {
                                    string newSkillsetMsd = "(";
                                    if(last_bleh.Contains("Str")) {
                                        newSkillsetMsd += "Str:" + msd_stream+"|";
                                    }
                                    if(last_bleh.Contains("JS")) {
                                        newSkillsetMsd += "JS:" + msd_jumpstream+"|";
                                    }
                                    if(last_bleh.Contains("HS")) {
                                        newSkillsetMsd += "HS:" + msd_handstream+"|";
                                    }
                                    if(last_bleh.Contains("Sta")) {
                                        newSkillsetMsd += "Sta:" + msd_stamina+"|";
                                    }
                                    if(last_bleh.Contains("JaSp")) {
                                        newSkillsetMsd += "JaSp:" + msd_jackspeed+"|";
                                    }
                                    if(last_bleh.Contains("CJ")) {
                                        newSkillsetMsd += "CJ:" + msd_chordjack+"|";
                                    }
                                    if(last_bleh.Contains("Tech")) {
                                        newSkillsetMsd += "Tech:" + msd_tech+"|";
                                    }
                                    newSkillsetMsd=newSkillsetMsd.Substring(0, newSkillsetMsd.Length - 1);
                                    newSkillsetMsd += ")";
                                    bleh[bleh.Length - 1] = newSkillsetMsd;
                                }
                                newLine = String.Join(" ", bleh.Where(s => !String.IsNullOrEmpty(s)));
                            }
                            else
                            {
                                // Why would you do this?!
                                newLine = line;
                            }
                        }
                        else if (line.Contains("BeatmapSetID:"))
                        {
                            newLine = "BeatmapSetID:-1";
                        }
                        break;
                    case "[Events]":
                        if (line.StartsWith("//"))
                        {
                            // Save what undercategory we are in.
                            eventSection = line;
                        }
                        else
                        {
                            switch (eventSection)
                            {
                                case "//Break Periods":
                                    string[] breakPoints = lines[i].Split(',');
                                    int start = (int)Math.Round(int.Parse(breakPoints[1]) / rate);
                                    int end = (int)Math.Round(int.Parse(breakPoints[2]) / rate);
                                    newLine = "2, " + start + ", " + end;
                                    break;
                                case "//Storyboard Sound Samples":
                                    newLine = TimingConvert(line, 1, ',');
                                    break;
                                case "//Storyboard Layer 0 (Background)":
                                case "//Storyboard Layer 1 (Fail)":
                                case "//Storyboard Layer 2 (Pass)":
                                case "//Storyboard Layer 3 (Foreground)":

                                    // If line is an event
                                    if (line.StartsWith(" ") || line.StartsWith("_"))
                                    {
                                        // Change starttime
                                        newLine = TimingConvert(line, 2, ',');

                                        // Accomodates for the eventual shorthand ",," 
                                        if (newLine.Split(',')[3].Trim() != "")
                                        {
                                            // Change endtime
                                            newLine = TimingConvert(newLine, 3, ',');
                                        }
                                    }
                                    // If line is an declaration and an animation
                                    else if(line.Split(',')[0] == "Animation")
                                    {
                                        newLine = TimingConvert(newLine, 7, ',');
                                    }
                                    break;
                            }
                        }
                        break;
                    case "[TimingPoints]":
                        if (true)
                        {
                            string[] data = lines[i].Split(',');

                            // For every timingpoint
                            newLine = TimingConvert(line, 0, ',');

                            // If uninherited timingpoint
                            if (data[6] == "1")
                            {
                                newLine = TimingConvert(newLine, 1, ',', true);
                            }
                        }
                        break;
                    case "[HitObjects]":
                        if (true)
                        {
                            // Change timing on all hit objects
                            newLine = TimingConvert(line, 2, ',');

                            // Gather data from line
                            string[] data = newLine.Split(',');

                            // Change mania-sliders end-timings and... spinner end-timings somehow? Lol. 
                            if (!data[5].StartsWith("0") && !data[5].Contains("|"))
                            {
                                data[5] = TimingConvert(data[5], 0, ':');
                                newLine = "";

                                // Asigning overwritten data to the new line
                                for (int x = 0; x < data.Length; x++)
                                {
                                    if (x != 0) newLine += ",";
                                    newLine += data[x];
                                }
                            }
                        }
                        break;
                }

                newLines[i] = newLine;

                // If nothing else, just copy the line.
                if (newLines[i] == "")
                {
                    newLines[i] = lines[i];
                }

            }

            string newFileName;
            if (rate != 1.0)
            {
                newFileName = fileName.Remove(fileName.Length - 4) + " [" + rate + "x].osu";
            }
            else
            {
                newFileName = fileName.Remove(fileName.Length - 4) + " [" + rate + ".0x].osu";
            }
            DirectoryInfo songDir = Directory.GetParent(filePath);
            string pathString = Path.Combine(songDir.FullName, newFileName);

            // Check if file excists and if not creates a new one.
            if (!File.Exists(pathString))
            {
                using (FileStream fs = File.Create(pathString))
                {
                    for (byte i = 0; i < 100; i++)
                    {
                        fs.WriteByte(i);
                    }
                }
            }
            else
            {
                return false;
            }

            // Write the data in the new file
            File.WriteAllLines(pathString, newLines);

            return true;
        }
    }
}