import os
import ffmpeg
import patoolib
import shutil

from django.conf import settings
from django.shortcuts import render,redirect
# Create your views here.
        
def add_subtitles(request):
    if request.method=='POST':
        input_vid= request.FILES.get("input_vid")
        subs=request.FILES.get("input_subs")

        sub_name=subs.name
        file_extension = sub_name.split('.')[-1].lower()
        if file_extension not in ['srt', 'sub', 'vtt', 'txt', 'ass', 'ssa', 'xml', 'idx', 'pgs','dfxp','ttml']:
            return redirect('add_subtitles')
        
        vid_name=input_vid.name
        video_content = input_vid.read()
        original_video_path = os.path.join(settings.BASE_DIR, 'inputs', 'vids', 'add_subs', vid_name)
        with open(original_video_path, 'wb') as file:
            file.write(video_content)

        sub_content=subs.read()
        sub_path=f"inputs\\others\\subs\\{sub_name}"
        with open(sub_path, 'wb') as file:
            file.write(sub_content)

        output_path = os.path.join(settings.BASE_DIR, 'outputs', 'add_subs', vid_name)
        
        ffmpeg_vid = ffmpeg.input(original_video_path)
        ffmpeg_audio = ffmpeg_vid.audio
        ffmpeg.concat(ffmpeg_vid.filter("subtitles", sub_path), ffmpeg_audio, v=1, a=1).output(output_path).run()

        return redirect('add_subtitles')
    return render(request,'add_sub.html')

def to_audio(request):
    if request.method=="POST":
        input_vid=request.FILES.get("input_vid")
        vid_name_full=input_vid.name
        vid_name=vid_name_full.split('.')[0]

        vid_content=input_vid.read()
        orignal_vid_path=os.path.join(settings.BASE_DIR, 'inputs', 'vids', 'to_audio', vid_name_full)
        with open(orignal_vid_path,'wb') as file:
            file.write(vid_content)
        
        output_path=os.path.join(settings.BASE_DIR, 'outputs', 'audio', vid_name+'.mp3')
        (
            ffmpeg.input(orignal_vid_path)
            .output(output_path)
            .run()
        )
        return redirect('add_subtitles')
    
    return render(request,"to_audio.html")

def change_format(request):
    if request.method == 'POST':
        selected_format = request.POST.get('format')
        input_vid=request.FILES.get("input_vid")
        vid_name_full=input_vid.name
        vid_name=vid_name_full.split('.')[0]

        vid_content=input_vid.read()
        orignal_vid_path=os.path.join(settings.BASE_DIR, 'inputs', 'vids', 'convert', vid_name_full)
        with open(orignal_vid_path,'wb') as file:
            file.write(vid_content)
        
        output_path=os.path.join(settings.BASE_DIR, 'outputs', 'convert', vid_name+selected_format)
        (
            ffmpeg.input(orignal_vid_path)
            .output(output_path)
            .run()
        )
        return redirect('change_format')

    return render(request,'change_format.html')

def extract_frames(request):
    if request.method == 'POST':
        input_vid = request.FILES.get("input_vid")
        vid_name_full = input_vid.name
        vid_name=vid_name_full.split('.')[0]

        vid_content = input_vid.read()
        original_vid_path = os.path.join(settings.BASE_DIR, 'inputs', 'vids', 'extract_frames', vid_name_full)
        with open(original_vid_path, 'wb') as file:
            file.write(vid_content)
        
        os.mkdir(os.path.join(settings.BASE_DIR, 'outputs', 'extract_frames', f'{vid_name}'))
        output_path = os.path.join(settings.BASE_DIR, 'outputs', 'extract_frames', f'{vid_name}')
        
        ffmpeg.input(original_vid_path).output(os.path.join(output_path, 'frame%d.png')).run()

        zip_path=f"outputs\\extract_frames\\{vid_name}"
        
        shutil.make_archive(zip_path,'zip',output_path)
        return redirect('extract_frames')

    return render(request, 'extract_frames.html')