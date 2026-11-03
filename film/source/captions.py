"""Create editable SRT + ASS word-highlight track from measured word times."""
from pathlib import Path
import json, shutil
from PIL import ImageFont
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'words.json').read_text())['words']
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',52)
# Phrase boundaries preserve syntax and stay short (one or two lines).
ends=[3,6,10,14,16,18,21,25,28,32,37,39,42,45,48,52,55,57,58,62,66,70,73,78,83,88]
def ass_time(t):
 n=round(t*100);return f'{n//360000}:{n//6000%60:02}:{n//100%60:02}.{n%100:02}'
def srt_time(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
head='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,52,&H00D3E4EB,&H00D3E4EB,&H00110F0C,&H00110F0C,0,0,0,0,100,100,0,0,1,1,0,7,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
events=[];srt=[];layouts=[];a=0
for num,b in enumerate(ends,1):
 group=words[a:b];a=b
 start=group[0]['start'];end=min(group[-1]['end']+.13,words[b]['start'] if b<len(words) else 39.967)
 lines=[[]]
 for w in group:
  text=' '.join(x['word'] for x in lines[-1]+[w])
  if font.getlength(text)>820 and lines[-1]:lines.append([])
  lines[-1].append(w)
 assert len(lines)<=2
 text='\n'.join(' '.join(x['word'] for x in line) for line in lines)
 srt.append(f'{num}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n')
 for row,items in enumerate(lines):
  width=sum(font.getlength(w['word']) for w in items)+font.getlength(' ')*(len(items)-1)
  x=(1080-width)/2;y=1440+row*73
  for w in items:
   pos=f'\\pos({x:.2f},{y})'
   def event(layer,s,e,sty):
    events.append(f'Dialogue: {layer},{ass_time(s)},{ass_time(e)},Default,,0,0,0,,{{{pos}{sty}}}'+w['word'])
   event(0,start,end,'\\fad(40,50)')
   event(1,w['start'],min(end,w['end']+.04),'\\1c&H99A1EE&\\fad(35,45)')
   layouts.append({'word':w['word'],'x':x,'y':y,'width':font.getlength(w['word']),'start':w['start'],'end':w['end']})
   x+=font.getlength(w['word']+' ')
(ROOT/'captions.ass').write_text(head+'\n'.join(events)+'\n')
(ROOT/'captions.srt').write_text('\n'.join(srt))
(ROOT/'caption-layout.json').write_text(json.dumps(layouts,ensure_ascii=False,indent=2))
for f in ['captions.srt','words.json']:
 shutil.copy(ROOT/f,ROOT.parent/'delivery'/('word-times.json' if f=='words.json' else f))
