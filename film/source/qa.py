"""Full-file decode, timing/layout checks and contact sheets of exported video."""
import json,subprocess,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
V=R.parent/'delivery/Klyde-Vrene-TikTok.mp4'
OUT=R.parent/'inspection/final'; OUT.mkdir(parents=True,exist_ok=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',str(V)]))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
assert (video['width'],video['height'],video['r_frame_rate'])==(1080,1920,'30/1')
p=subprocess.Popen(['ffmpeg','-v','error','-i',str(V),'-vf','scale=108:192','-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
frames=[]
while True:
 b=p.stdout.read(108*192*3)
 if not b:break
 assert len(b)==108*192*3
 frames.append(np.frombuffer(b,dtype=np.uint8).reshape(192,108,3).copy())
err=p.stderr.read().decode();assert p.wait()==0 and not err,err
assert len(frames)==1200
black=[i for i,f in enumerate(frames) if f.max()<30]
assert not black
diff=[float(np.abs(a.astype(float)-b.astype(float)).mean()) for a,b in zip(frames,frames[1:])]
# Voice must remain byte-identical after decoding to the accepted baseline.
base=R.parent/'Klyde-Vrene-TikTok.mp4'
if not base.is_file():
 # Support the onboarding build copy outside the checkout.
 base=Path('/workspace/klydevrene/film/Klyde-Vrene-TikTok.mp4')
audio={}
for key,path in [('base',base),('new',V)]:
 audio[key]=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-f','hash','-hash','sha256','-']).decode().strip()
assert audio['base']==audio['new'], 'Narration differs from the accepted baseline'
(R.parent/'delivery/audio-check.json').write_text(json.dumps({'decoded_audio_hash':audio,'identical':True},indent=2))
words=json.loads((R/'words.json').read_text())['words'];layouts=json.loads((R/'caption-layout.json').read_text())
assert len(words)==len(layouts)==88
assert all(0<=w['start']<w['end']<=40 for w in words)
assert all(w['end']<=v['start']+.001 for w,v in zip(words,words[1:]))
assert all(110<=x['x']-(x['scale_max']-1)*x['width']/2 and x['x']+x['width']*(1+(x['scale_max']-1)/2)<=900 and 1440<=x['y']<=1540 for x in layouts)
ass=(R/'captions.ass').read_text();assert ass.count('\\1c&H99A1EE&')==88
highlights=[line for line in ass.splitlines() if '\\1c&H99A1EE&' in line]
def seconds(s):
 h,m,v=s.split(':');return int(h)*3600+int(m)*60+float(v)
for w,line in zip(words,highlights):
 fields=line.split(',',9)
 assert abs(seconds(fields[1])-w['start'])<.011
 assert abs(seconds(fields[2])-w['end'])<.011
 assert fields[9].split('}',1)[1]==w['word']
 assert '\\fscx' in fields[9] and '\\t(' in fields[9]

for page in range(4):
 sheet=Image.new('RGB',(1080,2400),(12,15,17)); d=ImageDraw.Draw(sheet)
 for cell in range(20):
  t=page*10+cell*.5; f=frames[round(t*30)]
  thumb=Image.fromarray(f).resize((270,480),Image.Resampling.LANCZOS)
  x=cell%4*270;y=cell//4*480;sheet.paste(thumb,(x,y));d.text((x+8,y+8),f'{t:.1f}s',fill='white')
 sheet.save(OUT/f'contact-{page}.jpg')
stats={'video':{'width':1080,'height':1920,'fps':30,'decoded_frames':len(frames),'duration':float(probe['format']['duration']),'codec':video['codec_name'],'pix_fmt':video['pix_fmt']},'black_frames':black,'adjacent_frame_difference':{'min':min(diff),'max':max(diff),'mean':sum(diff)/len(diff),'identical_frame_pairs':sum(v==0 for v in diff)},'subtitle_words':88,'subtitle_phrases':len((R/'captions.srt').read_text().strip().split('\n\n')),'highlight_events':88,'subtitle_layout_checks':'passed including maximum word scale; left>=110, right<=900, centers y=1440..1540; camera stage ends y=1325','sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'decode_errors':err}
(R.parent/'delivery/qa-metrics.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
