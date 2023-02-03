import os
import sys
import zipfile
import shutil
import re
import subprocess

APP_VERSION=1
TARGET_DIR="etterna2osu_song_packs"

offset=-26
failed=[]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def TERMINAL_WIDTH():
    return os.get_terminal_size().columns

def cleanup():
    target_folders = [f for f in os.listdir(".") if not os.path.isfile(f)]
    for folder in target_folders:
        shutil.rmtree(folder)

def main():
    # TODO: check with guil
    if os.name == "nt":
        import ctypes
        kernel32 = ctypes.WinDLL('kernel32')
        hStdOut = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
        mode.value |= 4
        kernel32.SetConsoleMode(hStdOut, mode)

    if not os.path.isdir(TARGET_DIR):
        os.mkdir(TARGET_DIR)
        
    print(bcolors.HEADER+" "*int((TERMINAL_WIDTH()-27)/2)+f"etterna2osu v{APP_VERSION} by bobermilk"+bcolors.ENDC)
    print(bcolors.HEADER+" "*int((TERMINAL_WIDTH()-39)/2)+"DM milk#6867 on discord for any queries"+bcolors.ENDC)
    print(bcolors.OKBLUE+" "*int((TERMINAL_WIDTH()-78)/2)+bcolors.UNDERLINE+"Thank you demi, guil, marc, chxu, senya, gonx, messica for helping me make this"+bcolors.ENDC)
    print()
    print("You can obtain etterna packs zips at https://etternaonline.com/packs")
    path = os.path.realpath(TARGET_DIR)
    os.startfile(path)
    input("Place all the etterna pack zips you want in the folder {}, then press enter".format(TARGET_DIR))
    print()
    #TODO: check for folder and non zips
    target_files = [f for f in os.listdir(TARGET_DIR) if os.path.isfile(os.path.join(TARGET_DIR, f)) and os.path.splitext(os.path.join(TARGET_DIR, f))[1]==".zip"]
    if len(target_files)==0:
        sys.exit("No packs are in etterna_to_osu folder, exiting")
    print("Detected files:")
    for i, file in enumerate(target_files, 1):
        print(f"    {i}. "+file)
    print()
    try:
        OD=int(input("What OD would you like? you can enter 1-10 >> "))
    except:
        print("Invalid OD, defaulting to OD 8")
        OD=8
    if OD not in range(1,11):
        print("Invalid OD, defaulting to OD 8")
        OD=8
    print()
    try:
        HP=int(input("What HP would you like? you can enter 1-10 >> "))
    except:
        print("Invalid HP, defaulting to HP 7")
        HP=7
    if HP not in range(1,11):
        print("Invalid HP, defaulting to HP 7")
        HP=7
    print()
    # creator=input("Enter the name you want as the creator of the converts >> ")
    # if not creator:
    #     print("Invalid creator, defaulting to bobermilk")
    #     creator="bobermilk"
    # print()
    creator="bobermilk"
    user_offset=input("Integer offset to be applied to all converted maps in milliseconds (positive offset means notes come later) >> ")
    if not user_offset:
        user_offset=0
    else:
        if user_offset.lstrip("-").isdigit():
            global offset
            user_offset=int(user_offset)
            offset+=user_offset
        else:
            user_offset=0

    print(f"{user_offset} milliseconds will be applied to all converted maps")
    print()
    input(bcolors.WARNING +"Press enter to start the conversions on all the song packs in the folder"+bcolors.ENDC)
    os.chdir(TARGET_DIR)
    cleanup()

    for pack_number, pack in enumerate(target_files, 1):
        print()
        print(bcolors.OKCYAN + f"Converting {pack} [{pack_number}/{len(target_files)} packs]"+ bcolors.ENDC)
        with zipfile.ZipFile(pack, 'r') as zip_ref:
            zip_ref.extractall(".")
        packfolder=[f for f in os.listdir(".") if not os.path.isfile(f)][0]
        # convert each chart
        os.chdir(packfolder)
        # clean extracted pack folder
        dirt=[f for f in os.listdir(".") if os.path.isfile(f)]
        for f in dirt:
            os.remove(f)
        charts=os.listdir(".")
        print()
        print(bcolors.HEADER+bcolors.UNDERLINE+"Song (charter)"+bcolors.ENDC+" "*(TERMINAL_WIDTH()-21)+bcolors.HEADER+bcolors.UNDERLINE+"Status"+bcolors.ENDC)
        for i, chart in enumerate(charts, 1):
            sm=[f for f in os.listdir(chart) if f.endswith(".sm")]
            # is there .sm?
            if len(sm)>0:
                sm=sm[0]
                os.chdir(chart)
                subprocess.run([f'..\\..\\..\\raindrop\\raindrop.exe', '-g', 'om', '-i', sm, '-o', '.'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # converted files handle offset and sv and titles
                osues=[f for f in os.listdir(".") if f.endswith(".osu")]

                for osu in osues:
                    with open(f"..\\{osu}", "a", encoding="utf8") as edit:
                        skip=False
                        with open(osu, encoding="utf8") as beatmap:
                            f=beatmap.readlines()
                            for j in range(0, len(f)):
                                if "Creator:" in f[j]:
                                    edit.write("Creator: "+ creator)
                                    edit.write("\n")
                                elif "Title:" in f[j]:
                                    title=re.split("[:]", f[j])
                                    del title[0]
                                    title=''.join(title).strip()
                                    edit.write("Title: "+packfolder+" - "+title)
                                    edit.write("\n")
                                elif "TitleUnicode:" in f[j]:
                                    title=re.split("[:]", f[j])
                                    del title[0]
                                    title=''.join(title).strip()
                                    edit.write("TitleUnicode: "+packfolder+" - "+title)
                                    edit.write("\n")
                                elif "AudioFilename:" in f[j]:
                                    audio=re.split("[:]", f[j])[-1].strip()
                                    if audio[0]==" ":
                                        audio=audio[1:]
                                    # is there a entry
                                    if "." in audio:
                                        stop=False
                                        audio=os.path.splitext(audio)
                                        # rename the audio file 
                                        oldext=audio[1].lower()
                                        audio_filename=str(i)+".mp3"
                                        try:
                                            sample_rate=int(subprocess.run(["..\\..\\..\\sox\\sox.exe", "--i", "-r", audio[0]+audio[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
                                            average_bitrate=subprocess.run(["..\\..\\..\\sox\\sox.exe", "--i", "-B", audio[0]+audio[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8").strip() 
                                            channel_count=int(subprocess.run(["..\\..\\..\\sox\\sox.exe", "--i", "-c", audio[0]+audio[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
                                            subprocess.run(["..\\..\\..\\sox\\sox.exe", "-v", "0.99", audio[0]+audio[1], "etterna_offset.raw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                            # maybe try another codec instead of lame
                                            # -qscale:a is for VBR higher quality, we use -b:a CBR cuz time sensitive
                                            a=subprocess.run(["..\\..\\..\\tools\\ffmpeg.exe", "-f", "s16le",  "-ar", str(sample_rate) ,"-ac", str(channel_count), "-i", "etterna_offset.raw","-codec:a" ,"libmp3lame" ,"-b:a" , average_bitrate, "etterna_offset.mp3"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                            shutil.move("etterna_offset.mp3", f"..\\{audio_filename}")
                                            os.remove("etterna_offset.raw")
                                        except Exception as e:
                                            stop=True
                                            
                                        # if oldext == ".mp3":
                                        #     audio_filename=str(i)+".mp3"
                                        #     subprocess.run([f"..\\..\\..\\tools\\test.exe", audio[0]+audio[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                        #     subprocess.run([f"..\\..\\..\\tools\\lame.exe", "-r", "etterna_offset.raw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                        #     os.remove("etterna_offset.raw")
                                            
                                        #     # subprocess.call(f'ffmpeg -i "{audio[0]+oldext}" "{audio[0]+".wav"}"', shell=True)
                                        # else:
                                        #     audio_filename=str(i)+".wav"

                                        # try:
                                        #     if oldext==".mp3":
                                        #         shutil.move("etterna_offset.mp3", f"..\\{audio_filename}")
                                        #     else:
                                        #         shutil.move(audio[0]+audio[1], f"..\\{audio_filename}")
                                        # except:
                                        #     # specified file does not exist. moving on.
                                        #     stop=True
                                        #     pass

                                    edit.write("AudioFilename: "+audio_filename)
                                    edit.write("\n")
                                elif "OverallDifficulty" in f[j]:
                                    edit.write(f"OverallDifficulty: {OD}")
                                    edit.write("\n")
                                elif "HPDrainRate" in f[j]:
                                    edit.write(f"HPDrainRate: {HP}")
                                    edit.write("\n")
                                elif "[Events]" in f[j]:
                                    edit.write(f[j])
                                    image=f[j+2].split(",")[-1][1:-2]
                                    try:
                                        shutil.copy2(image, "..")
                                    except:
                                        # specified file does not exist. moving on.
                                            pass
                                elif "[TimingPoints]" in f[j]:
                                    skip=True
                                    edit.write(f[j])
                                    while j<len(f) and "," not in f[j]:
                                        j+=1
                                    timing=f[j].split(",")
                                    timing[0]=str(int(timing[0])+offset)
                                    timing_point=""
                                    for pt in timing:
                                        timing_point+=pt
                                        timing_point+=","
                                    timing_point=timing_point[:-1]
                                    edit.write(timing_point) #write the first timing point
                                    edit.write("\n")
                                    while j<len(f) and "," in f[j]:
                                        j+=1
                                elif "[HitObjects]" in f[j]:
                                    skip=False
                                    edit.write(f[j])
                                    while j<len(f) and "," not in f[j]:
                                        j+=1
                                    while j<len(f) and "," in f[j]:
                                        # 1,1,1,1,1,hitsample
                                        # 1,1,1,1,1,1:hitsample
                                        object_data=f[j].split(",")
                                        object_data[2]=str(int(object_data[2])+offset)
                                        if len(object_data)==7:
                                            # ln detected 
                                            object_data[-2]=str(int(object_data[-2])+offset)
                                        note=""
                                        for x in object_data:
                                            note+=x
                                            note+=","
                                        note=note[:-1]
                                        edit.write(note)
                                        edit.write("\n")
                                        j+=1
                                    skip=True
                                elif not skip:
                                    edit.write(f[j])
                if not stop:
                    msg="[ Good ✓ ]"
                    print(chart+" "*(TERMINAL_WIDTH()-len(chart)-len(msg)-1)+bcolors.OKGREEN+msg+bcolors.ENDC)
                else:
                    failed.append(chart)
                    print(chart+"  "+bcolors.WARNING+"-"*(TERMINAL_WIDTH()-len(chart)-16)+">  "+bcolors.FAIL+"[ Fail ✗ ]"+bcolors.ENDC)
                os.chdir("..")
        # wrap things up and move them to output
        output=[f for f in os.listdir(".") if os.path.isfile(f)]
        print()
        print(bcolors.OKCYAN+f"Writing data to {packfolder}.osz"+bcolors.ENDC)
        with zipfile.ZipFile(f'..\{packfolder}.osz', 'w') as zip:        
            for file in output:
                zip.write(file, compress_type=zipfile.ZIP_DEFLATED)

        # move on to the next pack
        os.chdir("..")
        cleanup()
    if len(failed)>0:
        print()
        print("Charts that failed to convert:")
        for i, chart in enumerate(failed,1):
            print("    "+f"{i}. {chart}")
    print()
    print(f"Beatmaps files generated can be found in the {TARGET_DIR} folder")
    print(bcolors.OKGREEN+"All done! The converted files are all correctly timed :3"+bcolors.ENDC)

main()
