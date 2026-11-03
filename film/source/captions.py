"""Phone-first bold ASS captions; original CTC word timings, no retiming audio."""
from pathlib import Path
import json, shutil
from PIL import ImageFont
ROOT=Path(__file__).resolve().parent
words=json.loads((ROOT/'words.json').read_text())['words']
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',74)
# Short semantic groups, including complete educational terms.
ends=[3,6,10,14,16,18,21,25,28,32,34,37,39,42,45,48,52,55,57,58,62,66,70,73,76,78,81,83,86,88]
def ass_time(t):
 n=round(t*100);return f'{n//360000}:{n//6000%60:02}:{n%6000//100:02}.{n%100:02}'
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
Style: Default,DejaVu Sans,74,&H00D3E4EB,&H00D3E4EB,&H00110F0C,&H00110F0C,-1,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
events=[];srt=[];layouts=[];a=0
for num,b in enumerate(ends,1):
 group=words[a:b];a=b
 start=group[0]['start'];end=min(group[-1]['end']+.10,words[b]['start'] if b<len(words) else 39.967)
 lines=[[]]
 for w in group:
  if font.getlength(' '.join(x['word'] for x in lines[-1]+[w]))>760 and lines[-1]:lines.append([])
  lines[-1].append(w)
 assert len(lines)<=2,(num,lines)
 text='\n'.join(' '.join(x['word'] for x in line) for line in lines)
 srt.append(f'{num}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n')
 for row,items in enumerate(lines):
  width=font.getlength(' '.join(w['word'] for w in items)); x=500-width/2;y=1440+row*100
  for w in items:
   ww=font.getlength(w['word']);cx=x+ww/2
   def event(s,e,sty,enter=False):
    if e<=s:return
    pos=f'\\move({cx:.2f},{y+12},{cx:.2f},{y},0,100)' if enter else f'\\pos({cx:.2f},{y})'
    events.append(f'Dialogue: 1,{ass_time(s)},{ass_time(e)},Default,,0,0,0,,{{{pos}{sty}}}'+w['word'])
   # Split base/highlight/base: no double glyphs beneath scaled words.
   event(start,w['start'],'\\fad(85,0)',True)
   ms=round((w['end']-w['start'])*1000)
   peak=110 if w['word'].strip('.,:…?') in ['podrażnienie','jedną','naraz','podstaw','wiedzieć'] else 106
   sty=f'\\1c&H99A1EE&\\fscx100\\fscy100\\t(0,{min(80,ms//2)},\\fscx{peak}\\fscy{peak})\\t({min(80,ms//2)},{ms},\\fscx100\\fscy100)'
   event(w['start'],w['end'],sty)
   event(w['end'],end,'')
   layouts.append({'word':w['word'],'x':x,'y':y,'width':ww,'scale_max':peak/100,'start':w['start'],'end':w['end']})
   x+=font.getlength(w['word']+' ')
(ROOT/'captions.ass').write_text(head+'\n'.join(events)+'\n')
(ROOT/'captions.srt').write_text('\n'.join(srt))
(ROOT/'caption-layout.json').write_text(json.dumps(layouts,ensure_ascii=False,indent=2))
(ROOT.parent/'delivery').mkdir(exist_ok=True)
for f in ['captions.srt','words.json']:
 shutil.copy(ROOT/f,ROOT.parent/'delivery'/('word-times.json' if f=='words.json' else f))
print(f'{len(srt)} phrases; {len(layouts)} timed words; bold 74px')
