import os
import zipfile
import shutil
import re
import subprocess
import urllib.request, json 
from PIL import Image
from math import floor, ceil
from sys import platform, exit

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
    # fix win 10 colors
    if os.name == "nt":
        import ctypes
        kernel32 = ctypes.WinDLL('kernel32')
        hStdOut = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
        mode.value |= 4
        kernel32.SetConsoleMode(hStdOut, mode)
    else:
        exit("Only windows is supported for now")
    
    if platform != "win32":
        # we need wine 
        print(bcolors.OKCYAN+" "*int((TERMINAL_WIDTH()-73)/2)+"!"*86+bcolors.ENDC)
        print(bcolors.OKCYAN+" "*int((TERMINAL_WIDTH()-73)/2)+"!!! You need 32-bit wine installed to run this program on your system !!!")
        print(bcolors.OKCYAN+" "*int((TERMINAL_WIDTH()-73)/2)+"!"*86+bcolors.ENDC)
        print("You need 32-bit wine installed to run this program on your system")

    # check for updates
    try:
        with urllib.request.urlopen("https://api.github.com/repos/bobermilk/etterna2osu/releases") as url:
            data = json.load(url)
            if APP_VERSION < int(data[0]["name"][1:]):
                print(bcolors.OKCYAN+" "*int((TERMINAL_WIDTH()-78)/2)+"!"*86+bcolors.ENDC)
                print(bcolors.OKCYAN+" "*int((TERMINAL_WIDTH()-78)/2)+"!!! Update available at "+data[0]["html_url"]+" !!!")
                print(bcolors.OKCYAN+" "*int((TERMINAL_WIDTH()-78)/2)+"!"*86+bcolors.ENDC)
                print()
    except:
        pass

    if not os.path.isdir(TARGET_DIR):
        os.mkdir(TARGET_DIR)
        
    print(bcolors.HEADER+" "*int((TERMINAL_WIDTH()-27)/2)+f"etterna2osu v{APP_VERSION} by bobermilk"+bcolors.ENDC)
    print(bcolors.HEADER+" "*int((TERMINAL_WIDTH()-92)/2)+"DM milk#6867 on discord for any queries after reading FAQs at https://milkies.ml/etterna2osu"+bcolors.ENDC)
    print(bcolors.OKBLUE+" "*int((TERMINAL_WIDTH()-88)/2)+"Thank you demi, kangalio, guil, marc, chxu, senya, gonx, messica for helping me make this"+bcolors.ENDC)
    print()
    print(bcolors.FAIL+" "*int((TERMINAL_WIDTH()-96)/2)+"bobermilk is not liable for any distribution of the converted packs, only upload your own charts"+bcolors.ENDC)
    print()
    print(bcolors.HEADER+"You can obtain etterna packs zips at https://etternaonline.com/packs"+bcolors.ENDC)
    path = os.path.realpath(TARGET_DIR)
    try:
        os.startfile(path)
    except:
        pass
    input(bcolors.WARNING+"Place all the etterna pack zips you want in the folder {}, then press enter".format(TARGET_DIR)+bcolors.ENDC)
    print()
    #TODO: check for folder and non zips
    folder_content = lambda: [f for f in os.listdir(TARGET_DIR) if os.path.isfile(os.path.join(TARGET_DIR, f)) and os.path.splitext(os.path.join(TARGET_DIR, f))[1]==".zip"]
    while len(folder_content())==0:
        print(bcolors.FAIL+"No packs are in etterna_to_osu folder"+bcolors.ENDC)
        input(bcolors.WARNING+"Place all the etterna pack zips you want in the folder {}, then press enter".format(TARGET_DIR)+bcolors.ENDC)
        print()

    target_files=folder_content()

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
    try:
        remove_ln=str(input("Change short LNs to normal note? (hold duration <= 1/8) [y/n] >> ")).strip()
        if remove_ln=="y" or remove_ln=="Y":
            print("Short LNs will be changed to normal note")
            remove_ln=True
        else:
            print("Short LNs will remain")
            remove_ln=False
    except:
        print("Short LNs will remain")
        remove_ln=False
    print()
    creator=input("Enter the name you want as the creator of the converts >> ")
    if not creator:
        print("Invalid creator, defaulting to bobermilk")
        creator="bobermilk"
    print()
    print(bcolors.HEADER+"All the converted maps can have a constant offset error of ±15 miliseconds (human error + different setups)"+bcolors.ENDC)
    user_offset=input("Integer offset in milliseconds to be applied to all converted maps (use negative offset if song is coming earlier) >> ")
    if not user_offset:
        user_offset=0
    else:
        user_offset=user_offset.lstrip("-")
        if user_offset.isdigit():
            user_offset=int(user_offset)
            if user_offset in range(-1000,1001):
                global offset
                offset+=user_offset
            else:
                print("User offset too large, (max 1000 milliseconds)")
                user_offset=0
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
        print(bcolors.HEADER+bcolors.UNDERLINE+"Song (charter)"+bcolors.ENDC+" "*(TERMINAL_WIDTH()-21)+bcolors.HEADER+bcolors.UNDERLINE+"Status"+bcolors.ENDC+" ")
        msd={}
        for i, chart in enumerate(charts, 1):
            sm=[f for f in os.listdir(chart) if f.endswith(".sm")]
            # is there .sm?
            if len(sm)>0:
                sm=sm[0]
                os.chdir(chart)

                rate=1.0
                score_goal=0.93
                out=subprocess.run(["..\\..\\..\\tools\\win32\\minacalc.exe", sm, str(rate), str(score_goal)], stdout=subprocess.PIPE).stdout.splitlines()
                for line in out:
                    line=line.decode()
                    if "|" in line:
                        line=line.split("|")
                        msd[line[0].strip()+" "+str(rate) +"x - "]=list(map(float,line[1:]))

                if platform == "win32":
                    subprocess.run([f'..\\..\\..\\tools\\win32\\raindrop\\raindrop.exe', '-g', 'om', '-i', sm, '-o', '.'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.run(["wine", f'..\\..\\..\\tools\\win32\\raindrop\\raindrop.exe', '-g', 'om', '-i', sm, '-o', '.'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # converted files handle offset and sv and titles
                osues=[f for f in os.listdir(".") if f.endswith(".osu")]

                audio_filename=str(i)+".mp3"
                background_filename="foobaruwu"
                try:
                    for osu in osues:
                        with open(f"..\\{osu}", "a", encoding="utf8") as edit:
                            skip=False
                            with open(osu, encoding="utf8") as beatmap:
                                f=beatmap.readlines()
                                if len(f)==3:
                                    skip=True
                                beat_duration=0
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
                                    elif "Version:" in f[j]:
                                        diff_name=re.split("[: (]", f[j])[2]+" 1.0x - "
                                        if diff_name in msd:
                                            edit.write("Version: "+diff_name+str(round(msd[diff_name][0], 2)) + " MSD")
                                            edit.write("\n")
                                        else:
                                            edit.write(f[j])

                                    elif "AudioFilename:" in f[j]:
                                        audio=re.split("[:]", f[j])[-1].strip()
                                        if audio[0]==" ":
                                            audio=audio[1:]
                                        # is there a entry
                                        if "." in audio:
                                            stop=False
                                            if not os.path.isfile(f"..\\{audio_filename}"):
                                                if platform == "win32":
                                                    sample_rate=int(subprocess.run(["..\\..\\..\\tools\\win32\\sox\\sox.exe", "--i", "-r", audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
                                                    average_bitrate=subprocess.run(["..\\..\\..\\tools\\win32\\sox\\sox.exe", "--i", "-B", audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8").strip() 
                                                    channel_count=int(subprocess.run(["..\\..\\..\\tools\\win32\\sox\\sox.exe", "--i", "-c", audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
                                                    subprocess.run(["..\\..\\..\\tools\\win32\\sox\\sox.exe", "-v", "0.99", audio, "etterna_offset.raw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                                    # maybe try another codec instead of lame
                                                    # -qscale:a is for VBR higher quality, we use -b:a CBR cuz time sensitive
                                                    subprocess.run(["..\\..\\..\\tools\\win32\\ffmpeg.exe", "-f", "s16le",  "-ar", str(sample_rate) ,"-ac", str(channel_count), "-i", "etterna_offset.raw","-codec:a" ,"libmp3lame" ,"-b:a" , average_bitrate, "etterna_offset.mp3"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                                elif platform == "linux" or platform == "linux2":
                                                    sample_rate=int(subprocess.run(["wine","..\\..\\..\\tools\\win32\\sox\\sox.exe", "--i", "-r", audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
                                                    average_bitrate=subprocess.run(["wine","..\\..\\..\\tools\\win32\\sox\\sox.exe", "--i", "-B", audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8").strip() 
                                                    channel_count=int(subprocess.run(["wine","..\\..\\..\\tools\\win32\\sox\\sox.exe", "--i", "-c", audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
                                                    subprocess.run(["wine","..\\..\\..\\tools\\win32\\sox\\sox.exe", "-v", "0.99", audio, "etterna_offset.raw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                                    # maybe try another codec instead of lame
                                                    # -qscale:a is for VBR higher quality, we use -b:a CBR cuz time sensitive
                                                    subprocess.run(["..\\..\\..\\tools\\linux\\ffmpeg", "-f", "s16le",  "-ar", str(sample_rate) ,"-ac", str(channel_count), "-i", "etterna_offset.raw","-codec:a" ,"libmp3lame" ,"-b:a" , average_bitrate, "etterna_offset.mp3"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                                elif platform == "darwin":
                                                    sample_rate=int(subprocess.run(["..\\..\\..\\tools\\darwin\\sox\\sox", "--i", "-r", audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
                                                    average_bitrate=subprocess.run(["..\\..\\..\\tools\\darwin\\sox\\sox", "--i", "-B", audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8").strip() 
                                                    channel_count=int(subprocess.run(["..\\..\\..\\tools\\darwin\\sox\\sox", "--i", "-c", audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
                                                    subprocess.run(["..\\..\\..\\tools\\darwin\\sox\\sox", "-v", "0.99", audio, "etterna_offset.raw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                                    # maybe try another codec instead of lame
                                                    # -qscale:a is for VBR higher quality, we use -b:a CBR cuz time sensitive
                                                    subprocess.run(["..\\..\\..\\darwin\\win32\\ffmpeg", "-f", "s16le",  "-ar", str(sample_rate) ,"-ac", str(channel_count), "-i", "etterna_offset.raw","-codec:a" ,"libmp3lame" ,"-b:a" , average_bitrate, "etterna_offset.mp3"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


                                                shutil.move("etterna_offset.mp3", f"..\\{audio_filename}")
                                                os.remove("etterna_offset.raw")
                                                os.remove(audio)
                                                    
                                                # if oldext == ".mp3":
                                                #     audio_filename=str(i)+".mp3"
                                                #     subprocess.run([f"..\\..\\..\\tools\\test.exe", audio], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                                #     subprocess.run([f"..\\..\\..\\tools\\lame.exe", "-r", "etterna_offset.raw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                                #     os.remove("etterna_offset.raw")
                                                    
                                                #     # subprocess.call(f'ffmpeg -i "{audio[0]+oldext}" "{audio[0]+".wav"}"', shell=True)
                                                # else:
                                                #     audio_filename=str(i)+".wav"

                                                # try:
                                                #     if oldext==".mp3":
                                                #         shutil.move("etterna_offset.mp3", f"..\\{audio_filename}")
                                                #     else:
                                                #         shutil.move(audio, f"..\\{audio_filename}")
                                                # except:
                                                #     # specified file does not exist. moving on.
                                                #     stop=True
                                                #     pass

                                        edit.write("AudioFilename: "+audio_filename)
                                        edit.write("\n")
                                    elif "Tags:" in f[j]:
                                        tags=f"Tags: etterna etterna2osu etterna2osu_v{APP_VERSION}"
                                        if remove_ln:
                                            tags+=" no_shlongs"
                                        tags+="\n"
                                        f[j]=tags
                                        edit.write(f[j])
                                    elif "OverallDifficulty" in f[j]:
                                        edit.write(f"OverallDifficulty: {OD}")
                                        edit.write("\n")
                                    elif "HPDrainRate" in f[j]:
                                        edit.write(f"HPDrainRate: {HP}")
                                        edit.write("\n")
                                    elif "[Events]" in f[j]:
                                        edit.write(f[j])
                                        image=f[j+2].split(",")
                                        image_filename=image[-1][1:-2]
                                        image_ext=os.path.splitext(image_filename)[1]
                                        background_filename=str(i)+image_ext

                                        if not os.path.isfile(f"..\\{background_filename}"):
                                            if not os.path.isfile(image_filename):
                                                # specified file does not exist. attempting to get the largest res image from the directory
                                                max_area=0
                                                try:
                                                    for ff in os.listdir():
                                                        if ff.lower().endswith(('.png', '.jpg', '.jpeg')):
                                                            with Image.open(ff) as im:
                                                                width, height=im.size
                                                                if width*height>max_area:
                                                                    max_area=width*height
                                                                    image_filename=ff
                                                                    image_ext=os.path.splitext(image_filename)[1]
                                                                    background_filename=str(i)+image_ext
                                                except:
                                                    pass
                                            try:
                                                shutil.move(image_filename, f"..\\{background_filename}")
                                            except:
                                                pass

                                        image[-1]='"'+background_filename+'"\n'
                                        bg=""
                                        for a in image:
                                            bg+=a
                                            bg+=","
                                        bg=bg[:-1]
                                        f[j+2]=bg
                                    elif "[TimingPoints]" in f[j]:
                                        skip=True
                                        edit.write(f[j])
                                        while j<len(f) and "," not in f[j]:
                                            j+=1
                                        timing=f[j].split(",")
                                        beat_duration=float(timing[1])
                                        snap_offset=float(timing[0])
                                        if snap_offset-floor(snap_offset)<0.5:
                                            snap_offset=floor(snap_offset)
                                        else:
                                            snap_offset=ceil(snap_offset)
                                        timing[0]=str(snap_offset+offset)
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
                                            note_time=int(object_data[2])+offset
                                            object_data[2]=str(note_time)
                                            if len(object_data)==7:
                                                # ln detected 
                                                ln_release=int(object_data[-2])+offset
                                                if remove_ln and ln_release-note_time<=beat_duration/8:
                                                    object_data[3]=str(1)
                                                    # remove the 1/8 ln
                                                    del object_data[-2]
                                                else:
                                                    object_data[-2]=str(ln_release)
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
                except:
                    stop=True
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
