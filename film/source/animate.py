"""Klyde Vrene — original procedural character animation. Python 3 + Pillow.
All positions use a 1080x1920 canvas; times in seconds. No third-party artwork.
Run: python animate.py --render ../delivery/no-captions-silent.mp4
"""
import math, json, subprocess, argparse
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
W,H,FPS=1080,1920,30
BG=(12,15,17); RED=(208,64,76); LIGHT=(235,228,211); DIM=(90,101,103)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
class SmoothDraw:
 """Draw in logical coordinates on a 2x antialiasing canvas."""
 def __init__(self,im): self.d=ImageDraw.Draw(im)
 def __getattr__(self,name):
  def call(coords,*args,**kw):
   def twice(x): return [twice(v) for v in x] if isinstance(x,(list,tuple)) else x*2
   for key in ['width','radius']:
    if key in kw: kw[key]*=2
   if 'font' in kw: kw['font']=kw['font'].font_variant(size=kw['font'].size*2)
   return getattr(self.d,name)(twice(coords),*args,**kw)
  return call
def font(n): return ImageFont.truetype(FONT,n)
def ease(x):
 x=max(0,min(1,x)); return x*x*x*(x*(x*6-15)+10)
def ramp(t,a,b): return ease((t-a)/(b-a))
def lerp(a,b,u): return a+(b-a)*u
def blend(a,b,u): return tuple(lerp(x,y,u) for x,y in zip(a,b))
def wave(t,p=0): return math.sin(t*2.1+p)
def line(d,pts,fill=RED,w=15):
 d.line(pts,fill=fill,width=w,joint='curve'); r=w/2
 for x,y in pts: d.ellipse((x-r,y-r,x+r,y+r),fill=fill)
def txt(d,xy,s,size=32,fill=LIGHT,anchor='mm'):
 d.text(xy,s,font=font(size),fill=fill,anchor=anchor)
def ik(a,b,L1=100,L2=104,bend=1):
 dx,dy=b[0]-a[0],b[1]-a[1]; dist=max(.01,math.hypot(dx,dy))
 dist=min(dist,L1+L2-.1); ang=math.atan2(dy,dx)
 v=math.acos(max(-1,min(1,(L1*L1+dist*dist-L2*L2)/(2*L1*dist))))*bend
 return a[0]+L1*math.cos(ang+v),a[1]+L1*math.sin(ang+v)
def bottle(d,x,y,k=0,scale=1,alpha=1):
 # anchor is center at bottom; separate silhouettes, no invented product branding
 c=tuple(int(v*alpha+BG[i]*(1-alpha)) for i,v in enumerate(RED))
 def box(v): return tuple((x+v[i]*scale if i%2==0 else y+v[i]*scale) for i in range(4))
 if k%3==0:
  d.rounded_rectangle(box((-25,-115,25,0)),radius=8,outline=c,width=3)
  d.rectangle(box((-12,-133,12,-116)),outline=c,width=3)
  line(d,[(x,y-135*scale),(x,y-145*scale),(x+28*scale,y-145*scale)],c,3)
 elif k%3==1:
  d.rounded_rectangle(box((-22,-85,22,0)),radius=9,outline=c,width=3)
  d.rectangle(box((-10,-105,10,-85)),outline=c,width=3)
  d.ellipse(box((-7,-120,7,-104)),fill=c)
 else:
  d.polygon([(x-28*scale,y-110*scale),(x+28*scale,y-110*scale),(x+19*scale,y-13*scale),(x-19*scale,y-13*scale)],outline=c,width=3)
  d.rectangle(box((-19,-13,19,0)),outline=c,width=3)
 line(d,[(x-11*scale,y-50*scale),(x+11*scale,y-50*scale)],c,2)
def mirror(d,t,irritated=False):
 d.rounded_rectangle((652,550,900,1010),radius=112,outline=DIM,width=3)
 d.rounded_rectangle((665,563,887,997),radius=100,outline=(37,44,47),width=2)
 # reflected head subtly follows the protagonist's inspection
 x=772+5*wave(t); y=735+3*wave(t+.3)
 d.ellipse((x-44,y-53,x+44,y+53),outline=(145,53,64),width=6)
 line(d,[(x-58,912),(x-48,825),(x+40,825),(x+54,912)],(104,43,52),8)
 for dx in [-15,15]: d.ellipse((x+dx-3,y-9,x+dx+3,y-3),fill=LIGHT)
 if irritated:
  for dx,dy in [(-21,15),(-13,24),(22,19),(27,10)]:
   r=4+1.5*wave(t*2,dx); d.ellipse((x+dx-r,y+dy-r,x+dx+r,y+dy+r),fill=RED)
 line(d,[(x-12,y+26),(x+10,y+26)],(145,53,64),3)
 line(d,[(690,600),(705,584)],(67,76,77),2)
def character(d,t,x=410,gesture='inspect',weight=1):
 # Fully jointed limbs; targets interpolated with quintic easing, solved with IK.
 breath=3*wave(t); sway=4*wave(t*.55)
 hip=(x+sway,1058+breath); neck=(x+8*wave(t*.7),837+breath)
 shoulderL=(neck[0]-48,neck[1]+29); shoulderR=(neck[0]+48,neck[1]+29)
 left=(x-69+4*wave(t),1050+breath); right=(x+80,1012+breath)
 tilt=-.06+.025*wave(t)
 if gesture=='inspect':
  u=.5+.5*wave(t*.8); right=(x+48+4*u,810+5*wave(t)); left=(x-84,1016+8*wave(t))
 elif gesture=='place':
  i=min(2,int(max(0,t)/1.05)); u=ramp(t,i*1.05,i*1.05+.8)
  bx=lerp(565,610+i*56,u); by=lerp(1110,1037,u)-55*math.sin(math.pi*u)
  right=(bx-15,by-85); left=(x-69,1040+4*wave(t)); tilt=.04*u
  if t-i*1.05>.8 and i<2:
   right=blend(right,(550,1025),ramp(t-i*1.05,.8,1.05))
 elif gesture=='confused':
  u=ramp(t,0,.8); left=blend(left,(x-133,898+12*wave(t)),u)
  right=blend(right,(x+135,891-12*wave(t)),u); tilt=.08*wave(t*.75)
 elif gesture=='remove':
  cyc=t%1.9; u=ramp(cyc,.1,.8)*(1-ramp(cyc,1.2,1.9))
  right=blend((x+64,1010),(x+188,905),u); left=(x-87,985)
 elif gesture=='observe':
  right=(x+91,875+4*wave(t)); left=(x-53,1035); tilt=-.03
 elif gesture=='basics':
  right=(x+141+12*wave(t*.7),902+15*wave(t)); left=(x-98,997+8*wave(t))
 elif gesture=='read':
  right=(x+112,899+3*wave(t)); left=(x+36,938+4*wave(t)); tilt=.12
 # legs have stable feet and moving knees rather than rigid rotating sticks
 for side in [-1,1]:
  a=(hip[0]+side*24,hip[1]+4); foot=(x+side*49,1260)
  knee=ik(a,foot,102,103,-side)
  line(d,[a,knee,foot],RED,25)
  line(d,[foot,(foot[0]+side*15,foot[1]+2)],RED,25)
 # tapered torso with softly rounded shoulders
 d.rounded_rectangle((neck[0]-52,neck[1]+14,neck[0]+52,hip[1]+12),radius=44,fill=RED)
 for a,b,bend in [(shoulderL,left,-1 if gesture=='confused' else 1),(shoulderR,right,-1 if gesture=='place' else 1)]:
  elbow=ik(a,b,100,104,bend); line(d,[a,elbow,b],RED,22)
  d.ellipse((b[0]-12,b[1]-12,b[0]+12,b[1]+12),fill=RED)
 # head follows breathing and attention, with eyes looking toward task
 hx=neck[0]+tilt*65; hy=neck[1]-57
 d.ellipse((hx-48,hy-55,hx+48,hy+53),fill=RED)
 blink=abs(math.sin(t*1.25))<.06
 eye_shift=7 if gesture in ['inspect','read','observe','place'] else 0
 for dx in [-16,16]:
  ex=hx+dx+eye_shift; ey=hy-5+tilt*dx
  if blink: line(d,[(ex-5,ey),(ex+5,ey)],BG,3)
  else: d.ellipse((ex-4,ey-5,ex+4,ey+4),fill=BG)
 if gesture=='confused':
  d.arc((hx-14,hy+16,hx+15,hy+36),180,350,fill=BG,width=3)
  line(d,[(hx-23,hy-21),(hx-10,hy-26)],BG,3)
 else: d.arc((hx-13,hy+8,hx+17,hy+29),5,165,fill=BG,width=3)
 return left,right

def shelf(d,t,count=3,remove=False):
 line(d,[(565,1040),(924,1040)],DIM,3)
 for i in range(count):
  x=610+i*56
  if remove and i>0:
   u=ramp(t,(i-1)*.8,(i-1)*.8+1.1)
   x=lerp(x,1070+i*50,u); y=lerp(1037,1140,u)
   bottle(d,x,y,i,alpha=1-u)
  else:
   u=ramp(t,i*1.05,i*1.05+.8)
   bottle(d,lerp(565,x,u),lerp(1110,1037,u)-55*math.sin(math.pi*u),i,alpha=u)

def symbol(d,x,y,k,t):
 c=LIGHT
 if k==0:
  pts=[]
  for i in range(61):
   a=i*math.pi*2/60
   pts.append((x+30*math.sin(a)*(1-math.cos(a))*.65,y-35*math.cos(a)))
  line(d,pts,c,4)
 elif k==1:
  d.rounded_rectangle((x-31,y-21,x+31,y+29),radius=9,outline=c,width=3)
  line(d,[(x-34,y-28),(x+34,y-28)],c,4)
  line(d,[(x-16,y+4),(x+16,y+4)],c,2)
 else:
  d.ellipse((x-21,y-21,x+21,y+21),outline=c,width=3)
  for i in range(8):
   a=i*math.pi/4+t*.03
   line(d,[(x+31*math.cos(a),y+31*math.sin(a)),(x+42*math.cos(a),y+42*math.sin(a))],c,3)

SCENES=[(0,5.85,'mirror'),(5.85,9.40,'products'),(9.40,14.04,'irritation'),(14.04,23.12,'one'),(23.12,28.80,'basics'),(28.80,36.88,'read'),(36.88,40.0,'cover')]

def scene(t,name):
 im=Image.new('RGB',(W*2,H*2),BG); d=SmoothDraw(im)
 # Permanent quiet stage: content deliberately kept above subtitle region.
 d.ellipse((180,1260,930,1300),fill=(17,21,23))
 line(d,[(155,1290),(925,1290)],(43,50,52),2)
 if name=='mirror':
  mirror(d,t); character(d,t,gesture='inspect')
 elif name=='products':
  shelf(d,t-5.85,3); character(d,t-5.85,x=480,gesture='place')
 elif name=='irritation':
  mirror(d,t,True); shelf(d,10,3)
  character(d,t-9.4,gesture='confused')
  for i in range(3):
   u=ramp(t,11+i*.6,11.7+i*.6); x=300+i*83
   txt(d,(x,620+7*wave(t,i)),'?',34,tuple(int(v*u+BG[j]*(1-u)) for j,v in enumerate(LIGHT)))
 elif name=='one':
  shelf(d,t-14.04,3,True); character(d,t-14.04,gesture='remove' if t<17.3 else 'observe')
  if t>20:
   u=ramp(t,20,21)
   d.arc((566,847,655,993),230,300,fill=tuple(int(v*u+BG[j]*(1-u)) for j,v in enumerate(LIGHT)),width=3)
 elif name=='basics':
  character(d,t,gesture='basics')
  for i,label in enumerate(['OCZYSZCZANIE','NAWILŻANIE','OCHRONA SPF']):
   starts=[24.3,25.9,27.0]; u=ramp(t,starts[i],starts[i]+.6)
   tile=Image.new('RGB',(W*2,H*2),BG); td=SmoothDraw(tile)
   x=300+i*240; y=610+30*(1-u)
   symbol(td,x,y,i,t); txt(td,(x,y+90),label,20)
   # merge only top section to preserve figure
   region=Image.blend(im,tile,u).crop(((x-112)*2,1020,(x+112)*2,1440))
   im.paste(region,((x-112)*2,1020)); d=SmoothDraw(im)
 elif name=='read':
  _,hand=character(d,t,x=455,gesture='read'); bottle(d,hand[0]+8,hand[1]+12,0,.7)
  # readable symbolic label magnification, gently growing from the product
  u=ramp(t,28.8,30.2)
  line(d,[(615,878),(681,817)],(56,65,64),2)
  d.rounded_rectangle((665,640,900,820),radius=18,outline=DIM,width=2)
  for i,l in enumerate([142,166,119]): line(d,[(695,685+i*34),(695+l*u,685+i*34)],LIGHT if i==0 else DIM,3)
  if t>32:
   u=ramp(t,32,33); line(d,[(731,930),(747,946),(780,909)],tuple(int(v*u+BG[j]*(1-u)) for j,v in enumerate(LIGHT)),4)
 elif name=='cover':
  cover=Image.open(ROOT/'assets/cover.png').convert('RGB')
  u=ramp(t,36.88,39.6); h=int(790+22*u); w=int(h*cover.width/cover.height)
  cover=cover.resize((w*2,h*2),Image.Resampling.LANCZOS)
  im.paste(cover,((W-w),920-int(8*u)*2))
  d=SmoothDraw(im); txt(d,(540,1326),'Klyde Vrene',29,(195,185,163))
 return im.resize((W,H),Image.Resampling.LANCZOS)

def frame(t):
 idx=max(i for i,(a,b,n) in enumerate(SCENES) if t>=a)
 a,b,n=SCENES[idx]; im=scene(t,n)
 if idx>0 and t<a+.65:
  prev=scene(t,SCENES[idx-1][2]); im=Image.blend(prev,im,ramp(t,a,a+.65))
 return im

def frame_bytes(i): return frame(i/FPS).tobytes()
def render(path,duration=40):
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(path)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 with ProcessPoolExecutor(max_workers=3) as pool:
  for i,data in enumerate(pool.map(frame_bytes,range(round(duration*FPS)),chunksize=3)):
   p.stdin.write(data)
   if i%150==0: print(f'{i/FPS:.0f}/{duration}s',flush=True)
 p.stdin.close()
 if p.wait(): raise RuntimeError('FFmpeg render failed')
if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('--render'); ap.add_argument('--still',type=float); args=ap.parse_args()
 if args.render: render(args.render)
 else: frame(args.still or 0).save(ROOT/'preview.png')
