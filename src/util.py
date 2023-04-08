import os
import zipfile
import shutil
import re
import subprocess
from PIL import Image
from math import floor, ceil
from sys import platform, exit

APP_VERSION=4
TARGET_DIR="etterna2osu_song_packs"
TARGET_DIR_SINGLE="etterna2osu_song_single"

no_sm_detected=True
failed=[]
diff_name_skillset_msd_titles=("Str", "JS", "HS", "Sta", "JaSp", "CJ", "Tech")

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

def get_calc_version():
    try:
        out=subprocess.run(["tools\\win32\\minacalc.exe"], stdout=subprocess.PIPE).stdout
        return out.decode()
    except:
        return "472"
calc_version=get_calc_version()

def rateChangeMap(rate, osu, s0, s1, s2, s3, s4, s5, s6, s7):
    subprocess.run(["..\\..\\..\\tools\\win32\\RateChanger\\RateChanger.exe", 
                    str(False),
                    os.path.join(os.getcwd(), osu), 
                    str(osu), 
                    s0, s1, s2, s3, s4, s5, s6, s7, str(rate)], shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def rateChangeAudio(rates, i, keep_pitch):
    cmd=["..\\..\\..\\tools\\win32\\RateChanger\\RateChanger.exe", 
                    str(True),
                    os.path.join(os.path.dirname(os.getcwd()), str(i)), 
                    str(keep_pitch)]
    for rate in rates:
        cmd.append(str(rate))
    subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def cleanup():
    target_folders = [f for f in os.listdir(".") if not os.path.isfile(f)]
    for folder in target_folders:
        shutil.rmtree(folder)

def main(OD, HP, offset, creator, additional_tags, rates, msd_bounds, remove_ln, diff_name_skillset_msd, keep_pitch):
    # print(OD)
    # print(HP)
    # print(offset)
    # print(creator)
    # print(additional_tags)
    # print(rates)
    # print(msd_bounds)
    # print(remove_ln)
    # print(diff_name_skillset_msd)
    # print(keep_pitch)

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

    if not os.path.isdir(TARGET_DIR):
        os.mkdir(TARGET_DIR)
        
    if not os.path.isdir(TARGET_DIR_SINGLE):
        os.mkdir(TARGET_DIR_SINGLE)

    print()
    print(bcolors.OKGREEN+" "*int((TERMINAL_WIDTH()-48)/2)+"Configuration successful. Conversion will begin."+bcolors.ENDC)
    print()

    one_file_mode=False
    sm=[f for f in os.listdir(TARGET_DIR_SINGLE) if f.endswith(".sm")]
    if len(sm)>0:
        x=f"!!!     Only {sm[0]} in folder etterna2osu_song_single will be converted    !!!"
        one_file_mode=True
        print(bcolors.OKCYAN+" "*int((TERMINAL_WIDTH()-len(x))/2)+"!"*len(x)+bcolors.ENDC)
        print(bcolors.OKCYAN+" "*int((TERMINAL_WIDTH()-len(x))/2)+x)
        print(bcolors.OKCYAN+" "*int((TERMINAL_WIDTH()-len(x))/2)+"!"*len(x)+bcolors.ENDC)

        try:
            if os.path.isfile(f"{TARGET_DIR}\\{TARGET_DIR_SINGLE}.zip"):
                os.remove(f"{TARGET_DIR}\\{TARGET_DIR_SINGLE}.zip")
            os.chdir(TARGET_DIR_SINGLE)
            # chart dir
            tmpdirname=sm[0][:-3]
            try:
                shutil.rmtree(tmpdirname)
            except:
                pass
            os.mkdir(tmpdirname)
            items=[x for x in os.listdir() if os.path.isfile(x)]
            for item in items:
                shutil.copy2(item, tmpdirname)
            os.chdir("..")

            with zipfile.ZipFile(f"{TARGET_DIR}\\{TARGET_DIR_SINGLE}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(f"{TARGET_DIR_SINGLE}\\{tmpdirname}"):
                    for file in files:
                        zipf.write(os.path.join(root, file), 
                                os.path.relpath(os.path.join(root, file), 
                                                os.path.join(f"{TARGET_DIR_SINGLE}\\{tmpdirname}", "..", "..")))
            shutil.rmtree(os.path.join(TARGET_DIR_SINGLE, tmpdirname))
        except Exception as e:
            print("Something failed, report this bug to milk#6867")

    print()
    if not one_file_mode:
        print(bcolors.HEADER+"You can obtain etterna packs zips at https://etternaonline.com/packs"+bcolors.ENDC)
        path = os.path.realpath(TARGET_DIR)
        try:
            os.startfile(path)
        except:
            pass
        input(bcolors.WARNING+"Place all the etterna pack zips you want in the folder {}, then press enter".format(TARGET_DIR)+bcolors.ENDC)
    else:
        input(bcolors.WARNING+f"Press enter to start converting {sm[0]}"+bcolors.ENDC)

    if not one_file_mode:
        print()
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

        input(bcolors.WARNING +"Press enter to start the conversions on all the song packs in the folder"+bcolors.ENDC)
    else:
        target_files=[f'{TARGET_DIR_SINGLE}.zip']

    os.chdir(TARGET_DIR)
    cleanup()

    for pack_number, pack in enumerate(target_files, 1):
        if not one_file_mode:
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
        for i, chart in enumerate(charts, 1):
            stop=0
            msd={}
            msd[1.0]={}
            sm=[f for f in os.listdir(chart) if f.endswith(".sm")]
            # is there .sm?
            if len(sm)>0:
                global no_sm_detected
                no_sm_detected=False
                sm=sm[0]
                os.chdir(chart)
                score_goal=0.93
                all_chart_rates=[rates[0]+rates[1]*x for x in range(0, rates[2])]
                # we force 1.0x msd to be calculated
                if 1.0 not in all_chart_rates:
                    all_chart_rates.append(1.0)

                for _rate in all_chart_rates:
                    rate=round(_rate,2)
                    diff_names={}
                    out=subprocess.run(["..\\..\\..\\tools\\win32\\minacalc.exe", sm, str(rate), str(score_goal)], stdout=subprocess.PIPE).stdout.splitlines()
                    for line in out:
                        line=line.decode()
                        if "skipping" in line:
                            break
                        if "|" in line:
                            line=line.split("|")
                            skillset_msd=[round(x, 1) for x in list(map(float,line[1:]))]
                            name=line[0].strip()
                            # always write diff name for later
                            diff_names[name]=skillset_msd
                            # skip this rate or not
                            if ((msd_bounds[0]!=-1.0 and msd_bounds[0]<=skillset_msd[0]) or msd_bounds[0]==-1) and ((msd_bounds[1]!=-1.0 and skillset_msd[0]<=msd_bounds[1]) or msd_bounds[1]==-1) or rate==1.0:
                                msd[rate]=diff_names

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
                        with open(f"{osu}.tmp", "a", encoding="utf8") as edit:
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
                                        with open(sm, "r", encoding="utf-8") as g:
                                            title_unicode=re.findall("(?<=#TITLETRANSLIT:).*(?=;)", g.read())
                                        if len(title_unicode[0].strip())==0:
                                            title=re.split("[:]", f[j])
                                            del title[0]
                                            title_unicode=''.join(title).strip()
                                        edit.write("TitleUnicode: "+packfolder+" - "+title_unicode)
                                        edit.write("\n")
                                    elif "Version:" in f[j]:
                                        diff_name=re.split("[: (]", f[j])[2]
                                        if diff_name in msd[1.0]:
                                            skillset_msd=msd[1.0][diff_name]
                                            skillset_msd_text="("
                                            for skillset_msd_title, skillset_msd_value, skillset_msd_commit in zip(diff_name_skillset_msd_titles, skillset_msd[1:], diff_name_skillset_msd):
                                                if skillset_msd_commit:
                                                    skillset_msd_text+=f"{skillset_msd_title}:{skillset_msd_value}"
                                                    skillset_msd_text+="|"
                                            skillset_msd_text=skillset_msd_text[:-1]
                                            if skillset_msd_text:
                                                edit.write("Version: "+diff_name+ " 1.0x - "+str(skillset_msd[0]) +" MSD " + skillset_msd_text + ")")
                                            else:
                                                edit.write("Version: "+diff_name+ " 1.0x - "+str(skillset_msd[0]) +" MSD")
                                            edit.write("\n")
                                        else:
                                            edit.write(f[j].split("(")[0]+" 1.0x - ??? MSD")
                                            edit.write("\n")

                                    elif "AudioFilename:" in f[j]:
                                        audio=re.split("[:]", f[j])[-1].strip()
                                        if audio[0]==" ":
                                            audio=audio[1:]
                                        # is there a entry
                                        if "." in audio:
                                            if not os.path.isfile(f"..\\{audio_filename}"):
                                                if not os.path.isfile(audio):
                                                    audios=[x for x in os.listdir() if x.endswith(('.mp3','.mp4','.ogg','.wav'))]
                                                    if len(audios)>0:
                                                        audio=audios[0]
                                                    else:
                                                        stop=1
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
                                        tags=f"Tags: etterna etterna2osu etterna2osu_v{int(APP_VERSION)}minacalc_v{calc_version} {additional_tags}"
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

                    # double checking
                    if os.path.isfile(f"..\{audio_filename}"):
                        try:
                            for osu in osues:
                                os.remove(osu)
                            osues=[f for f in os.listdir(".") if f.endswith(".tmp")]
                            for osu in osues:
                                os.rename(osu, osu[:-4])
                            osues=[f for f in os.listdir(".") if f.endswith(".osu")]
                            msd_rates=msd.keys()
                            tasks_audio=[]
                            tasks_maps=[]
                            for rate in msd_rates:
                                if rate != 1.0: # check if minacalc didn't fail and give us a empty dict of skillset_msd
                                    for osu in osues:
                                            diff_name=re.findall("\[(.*?)\]",osu)[-1].split("(")[0]
                                            s=list(map(str, msd[rate][diff_name]))
                                            tasks_maps.append((rate, osu, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]))
                                    tasks_audio.append(rate)

                            # pool.starmap(rateChangeMap, tasks_maps)
                            for t in tasks_maps:
                                rateChangeMap(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9])
                            if len(tasks_audio)>0:
                                rateChangeAudio(tasks_audio, i, keep_pitch)
                                    
                            osues=[f for f in os.listdir(".") if f.endswith(".osu") or f.endswith(".mp3")]
                            for osu in osues:
                                shutil.move(osu, "..")
                        except Exception as e:
                            stop=2
                except Exception as e:
                    # import sys
                    # exc_type, exc_obj, exc_tb = sys.exc_info()
                    # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    # print(exc_type, fname, exc_tb.tb_lineno)
                    stop=1
                if stop==0:
                    msg="[ Good ✓ ]"
                    print(chart+" "*(TERMINAL_WIDTH()-len(chart)-len(msg)-1)+bcolors.OKGREEN+msg+bcolors.ENDC)
                else:
                    if stop==1:
                        stop_err="[ Chart Fail ✗ ]"
                        stop_err_color=bcolors.FAIL
                    else:
                        stop_err="[ Uprate Fail ✗ ]"
                        stop_err_color=bcolors.WARNING
                        audios=[x for x in os.listdir("..") if x.endswith(('.wav'))]
                        for audio in audios:
                            if audio[0] == str(i):
                                os.remove(f"..\\{audio}")
                    failed.append((chart, stop_err))
                    print(chart+"  "+bcolors.WARNING+"-"*(TERMINAL_WIDTH()-len(chart)-(len(stop_err)+6))+">  "+stop_err_color+stop_err+bcolors.ENDC)
                os.chdir("..")
        # wrap things up and move them to output
        output=[f for f in os.listdir(".") if os.path.isfile(f)]
        print()
        if not no_sm_detected:
            print(bcolors.OKCYAN+f"Writing data to {packfolder}.osz"+bcolors.ENDC)
            with zipfile.ZipFile(f'..\{packfolder}.osz', 'w') as osz:        
                for file in output:
                    osz.write(file, compress_type=zipfile.ZIP_DEFLATED)
        else:
            print(bcolors.FAIL+f"There are no charts to convert!"+bcolors.ENDC)
        
        # move on to the next pack
        os.chdir("..")
        cleanup()
    if len(failed)>0:
        print()
        print("Charts that failed to convert:")
        for i, chart in enumerate(failed,1):
            print("    "+f"{i}. {chart[0]} - {chart[1]}")
    else:
        if one_file_mode:
            os.remove(f"{TARGET_DIR_SINGLE}.zip")
            x=f"{TARGET_DIR_SINGLE}.osz"
            if os.path.isfile(os.path.join("..", TARGET_DIR_SINGLE, x)):
                os.remove(os.path.join("..", TARGET_DIR_SINGLE, x))
            shutil.move(x, f"..\\{TARGET_DIR_SINGLE}\\{tmpdirname}.osz")

    print()
    print(f"Beatmaps files generated can be found in the {TARGET_DIR} folder")
    print(bcolors.OKGREEN+"All done! The converted files are all correctly timed :3"+bcolors.ENDC)
