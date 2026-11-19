from pathlib import Path
import os,uuid,json,re,copy,csv,math
import pcbnew as p
import sexpr as sx
sx.Path=Path;sx.re=re;sx.json=json;sx.copy=copy
from sexpr import symbol,tag,child,val,dump
R=Path(__file__).resolve().parents[1];os.chdir(R)
NAME='HPA_2CH'
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'HPA_2CH_INITIAL/'+s))
def v(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
parts=[]
RF='RF_Amplifier';RES='Resistor_SMD:R_0603_1608Metric';CAP='Capacitor_SMD:C_0603_1608Metric';IND='Inductor_SMD:L_0805_2012Metric';CONN='Connector_PinHeader_2.54mm';SMA='Connector_Coaxial:SMA_Amphenol_132134_Vertical'
def add(sheet,ref,lib,sym,value,fp,nets,sch,pcb,rot=0,dnp=False):
 parts.append(dict(sheet=sheet,ref=ref,lib=lib,sym=sym,value=value,fp=fp,nets={str(k):n for k,n in nets.items()},sch=sch,pcb=pcb,rot=rot,dnp=dnp,uuid=uid(ref)))
def resistor(sh,ref,value,n1,n2,sch,pcb,rot=0,dnp=False):add(sh,ref,'Device','R',value,RES,{1:n1,2:n2},sch,pcb,rot,dnp)
def cap(sh,ref,value,n1,n2,sch,pcb,rot=0):add(sh,ref,'Device','C',value,CAP,{1:n1,2:n2},sch,pcb,rot)
def conn(sh,ref,n,value,nets,sch,pcb):add(sh,ref,'Connector_Generic',f'Conn_01x{n:02d}',value,f'{CONN}:PinHeader_1x{n:02d}_P2.54mm_Vertical',nets,sch,pcb)
# MCU: physical names from official ST XML, no guessed pin numbering.
import xml.etree.ElementTree as E
ns={'x':'http://dummy.com'};xml=E.parse(R/'sources/STM32F405ZGTx.xml').getroot()
pm={re.match(r'P[A-Z]\d+',a.get('Name','')).group() if re.match(r'P[A-Z]\d+',a.get('Name','')) else a.get('Name'):a.get('Position') for a in xml.findall('x:Pin',ns)}
mp={}
for a in xml.findall('x:Pin',ns):
 nm=a.get('Name');num=a.get('Position')
 if nm in ['VDD','VBAT']:mp[num]='+3V3'
 if nm in ['VSS','VSSA']:mp[num]='GND'
 if nm in ['VDDA','VREF+']:mp[num]='VDDA'
 if nm.startswith('VCAP'):mp[num]=nm
for n in ['NRST','BOOT0']:mp[pm[n]]=n
for n in ['PH0','PH1']:mp[pm[n]]='HSE_IN' if n=='PH0' else 'HSE_OUT'
mp[pm['PB2']]='BOOT1'
for i,g in enumerate(['PE9','PE11','PE13','PE14','PC6','PC7','PC8','PC9','PD12','PD13'],1):mp[pm[g]]=f'FAN_PWM_{i}'
for i in range(10):mp[pm[f'PG{i}']]=f'FAN_TACH_{i+1}'
for g,n in [('PA5','SPI1_SCK'),('PA6','SPI1_MISO'),('PA7','SPI1_MOSI'),('PA4','SPI1_nCS'),('PG10','FPGA_IRQ'),('PG11','MCU_HEARTBEAT'),('PG12','SYSTEM_ARM'),('PG13','PA1_REQUEST'),('PG14','PA2_REQUEST'),('PG15','FPGA_RESET_N'),('PD0','PA1_PERMIT'),('PD1','PA2_PERMIT'),('PD8','UART_TX'),('PD9','UART_RX'),('PB8','I2C_SCL'),('PB9','I2C_SDA'),('PA13','SWDIO'),('PA14','SWCLK'),('PB3','SWO')]:mp[pm[g]]=n
for i,n in enumerate(['RF1_FWD_V','RF1_REV_V','RF2_FWD_V','RF2_REV_V']):mp[pm[f'PA{i}']]=n
for i,n in enumerate(['PA1_NTC','PA2_NTC','PA1_I_MON','PA2_I_MON','VIN_MON','VPA_MON']):mp[pm[f'PC{i}']]=n
add('MAIN_CONTROLLER','U1','MCU_ST_STM32F4','STM32F405ZGTx','STM32F405ZGT6','Package_QFP:LQFP-144_20x20mm_P0.5mm',mp,(85,145),(80,112))
conn('MAIN_CONTROLLER','JSWD',6,'SWD 3.3V + SWO',{1:'+3V3',2:'SWDIO',3:'GND',4:'SWCLK',5:'NRST',6:'SWO'},(180,50),(52,92))
conn('MAIN_CONTROLLER','JUART',4,'UART 3.3V',{1:'GND',2:'UART_TX',3:'UART_RX',4:'+3V3'},(180,85),(48,137))
conn('MAIN_CONTROLLER','JI2C',4,'I2C EXPANSION',{1:'GND',2:'+3V3',3:'I2C_SCL',4:'I2C_SDA'},(180,120),(110,137))
conn('MAIN_CONTROLLER','JCURR',4,'CURRENT 0..3.3V INPUTS',{1:'+3V3',2:'GND',3:'PA1_I_MON',4:'PA2_I_MON'},(180,155),(130,137))
fn={1:'+3V3',2:'GND',3:'SPI1_SCK',4:'SPI1_MISO',5:'SPI1_MOSI',6:'SPI1_nCS',7:'FPGA_IRQ',8:'MCU_HEARTBEAT',9:'SYSTEM_ARM',10:'PA1_REQUEST',11:'PA2_REQUEST',12:'FPGA_RESET_N',13:'GND',14:'+3V3',15:'PA1_PERMIT',16:'PA2_PERMIT'}
add('MAIN_CONTROLLER','JFPGA','Connector_Generic','Conn_02x08_Odd_Even','EXTERNAL FPGA INTERFACE - CHIP NOT PLACED',f'{CONN}:PinHeader_2x08_P2.54mm_Vertical',fn,(180,210),(114,101))
resistor('MAIN_CONTROLLER','R_RESET','10k','+3V3','NRST',(260,45),(60,128));cap('MAIN_CONTROLLER','C_RESET','100n','NRST','GND',(280,45),(56,128))
resistor('MAIN_CONTROLLER','R_BOOT0','10k','BOOT0','GND',(260,80),(67,94));resistor('MAIN_CONTROLLER','R_BOOT1','10k','BOOT1','GND',(280,80),(75,132))
add('MAIN_CONTROLLER','Y1','Device','Crystal_GND24','8MHz / CL18pF','Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm',{1:'HSE_IN',3:'HSE_OUT',2:'GND',4:'GND'},(260,120),(62,114.5))
cap('MAIN_CONTROLLER','C_X1','33p C0G TUNE','HSE_IN','GND',(250,145),(61,110));cap('MAIN_CONTROLLER','C_X2','33p C0G TUNE','HSE_OUT','GND',(275,145),(61,119))
cap('CORE_POWER','C_VCAP1','2.2u low ESR','VCAP_1','GND',(280,150),(95,127));cap('CORE_POWER','C_VCAP2','2.2u low ESR','VCAP_2','GND',(310,150),(99,104.5))
# Local decoupling positions derived from actual MCU footprint pad locations.
f=p.FootprintLoad('/usr/share/kicad/footprints/Package_QFP.pretty','LQFP-144_20x20mm_P0.5mm');f.SetPosition(v(80,112))
vpins=[a.get('Position') for a in xml.findall('x:Pin',ns) if a.get('Name')=='VDD']
for i,num in enumerate(vpins):
 pad=next(q for q in f.Pads() if q.GetNumber()==num);x=p.ToMM(pad.GetPosition().x);y=p.ToMM(pad.GetPosition().y)
 if abs(x-80)>abs(y-112):x+=-3.5 if x<80 else 3.5
 else:y+=-3.5 if y<112 else 3.5
 cap('CORE_POWER','C_VDD'+num,'100n','+3V3','GND',(35+(i%6)*35,100+(i//6)*35),(x,y))
add('CORE_POWER','FB1','Device','L_Ferrite','600R@100MHz - VERIFY',RES,{1:'+3V3',2:'VDDA'},(240,70),(58,124))
cap('CORE_POWER','C_ADDA','100n','VDDA','GND',(280,80),(61,124));cap('CORE_POWER','C_ADDB','1u','VDDA','GND',(310,80),(55,124))
conn('CORE_POWER','JPWR',2,'+5V CONTROL/FANS',{1:'+5V',2:'GND'},(35,35),(10,108))
add('CORE_POWER','UREG','Regulator_Linear','AMS1117-3.3','AMS1117-3.3','Package_TO_SOT_SMD:SOT-223-3_TabPin2',{3:'+5V',1:'GND',2:'+3V3'},(100,35),(30,110))
cap('CORE_POWER','C_IN','10u/10V','+5V','GND',(70,65),(23,110));add('CORE_POWER','C_OUT','Device','C_Polarized','10u TANT / ESR VERIFY','Capacitor_Tantalum_SMD:CP_EIA-3216-18_Kemet-A',{1:'+3V3',2:'GND'},(130,65),(37,110));cap('CORE_POWER','C_BULK','4.7u','+3V3','GND',(160,65),(37,117))
resistor('CORE_POWER','R_VIN_H','100k','+5V','VIN_MON',(250,200),(30,125));resistor('CORE_POWER','R_VIN_L','47k','VIN_MON','GND',(275,200),(34,125));cap('CORE_POWER','C_VINMON','100n','VIN_MON','GND',(300,200),(38,125))
# Fan signal drivers: MCU drives control input only; motors powered continuously.
for i in range(1,11):
 col=(i-1)//5;row=(i-1)%5;x=164+col*21;y=83+row*14;ssx=55+((i-1)%5)*150;ssy=80+((i-1)//5)*150;sh='FAN_CONTROL'
 conn(sh,f'JF{i}',4,f'FAN{i} 5V 4WIRE',{1:'GND',2:'+5V',3:f'TACH_RAW_{i}',4:f'PWM_OD_{i}'},(ssx+85,ssy),(x,y))
 add(sh,f'QF{i}','Transistor_FET','2N7002','2N7002','Package_TO_SOT_SMD:SOT-23',{1:f'FET_GATE_{i}',2:'GND',3:f'PWM_OD_{i}'},(ssx+45,ssy+20),(x-7,y+5))
 resistor(sh,f'RG{i}','100',f'FAN_PWM_{i}',f'FET_GATE_{i}',(ssx+10,ssy+10),(x-14,y+4))
 resistor(sh,f'RPD{i}','100k',f'FET_GATE_{i}','GND',(ssx+30,ssy+40),(x-14,y+8))
 resistor(sh,f'RTP{i}','10k','+3V3',f'TACH_RAW_{i}',(ssx+100,ssy+30),(x-4,y-3))
 resistor(sh,f'RTS{i}','1k',f'TACH_RAW_{i}',f'FAN_TACH_{i}',(ssx+100,ssy+55),(x-10,y-2))
 cap(sh,f'CT{i}','1n',f'FAN_TACH_{i}','GND',(ssx+65,ssy+60),(x-14,y-2))
# RF stages, bias tees and external laboratory supply headers. POWER LINKS DNP.
for ch,y in [(1,25),(2,60)]:
 sd=f'RF_DRIVER_CH{ch}';sp=f'RF_POWER_CH{ch}'
 add(sd,f'JRF_IN{ch}','Connector','Conn_Coaxial',f'RF INPUT CH{ch}',SMA,{1:f'RF_SRC_{ch}',2:'GND'},(35,60),(12,y))
 cap(sd,f'C_RFIN{ch}','22p C0G / RF TUNE',f'RF_SRC_{ch}',f'DRV_IN_{ch}',(75,60),(30,y))
 add(sd,f'UDRV{ch}',RF,'GVA-84','GVA-84 / UNVALIDATED', 'Package_TO_SOT_SMD:SOT-89-3',{1:f'DRV_IN_{ch}',2:'GND',3:f'DRV_OUT_{ch}'},(115,60),(50,y))
 add(sd,f'LDRV{ch}','Device','L','10n RF TUNE',IND,{1:f'DRV_FEED_{ch}',2:f'DRV_OUT_{ch}'},(115,100),(54,y-7),90)
 resistor(sd,f'R_DRV_PWR{ch}','0R DNP', '+5V',f'DRV_FEED_{ch}',(75,120),(46,y-10),dnp=True)
 cap(sd,f'C_DRVDC{ch}','100n',f'DRV_FEED_{ch}','GND',(150,110),(60,y-10))
 cap(sp,f'C_INTER{ch}','22p C0G / RF TUNE',f'DRV_OUT_{ch}',f'PA_IN_{ch}',(35,60),(77,y))
 pn={i:'GND' for i in range(1,34)}
 for i in [4,5]:pn[i]=f'PA_IN_{ch}'
 for i in [20,21]:pn[i]=f'PA_OUT_{ch}'
 add(sp,f'UPA{ch}',RF,'HMC8500PM5E','HMC8500PM5E / UNVALIDATED','Package_CSP:LFCSP-32-1EP_5x5mm_P0.5mm_EP3.1x3.1mm',pn,(100,60),(105,y))
 add(sp,f'LGATE{ch}','Device','L','10n RF TUNE',IND,{1:f'VGG_{ch}',2:f'PA_IN_{ch}'},(70,100),(96,y-7),90)
 conn(sp,f'JBIAS{ch}',2,'EXTERNAL NEGATIVE GATE BIAS',{1:f'VGG_{ch}',2:'GND'},(35,140),(85,y-14))
 cap(sp,f'C_GATE{ch}','100n',f'VGG_{ch}','GND',(70,140),(90,y-11))
 conn(sp,f'JPA{ch}',2,'EXTERNAL PA DRAIN - CHECK BIAS FIRST',{1:f'VPA_EXT_{ch}',2:'GND'},(155,140),(122,y-14))
 resistor(sp,f'R_PA_PWR{ch}','0R DNP',f'VPA_EXT_{ch}',f'PA_DRAIN_{ch}',(155,110),(115,y-10),dnp=True)
 add(sp,f'LDRAIN{ch}','Device','L','10n / >=1A RF TUNE',IND,{1:f'PA_DRAIN_{ch}',2:f'PA_OUT_{ch}'},(140,60),(114,y-4),90)
 cap(sp,f'C_PA_DC{ch}','100n/50V',f'PA_DRAIN_{ch}','GND',(190,140),(120,y-7))
 cap(sp,f'C_PA_B{ch}','10u/50V',f'PA_DRAIN_{ch}','GND',(220,140),(128,y-7))
 cap(sp,f'C_RFOUT{ch}','22p C0G / RF TUNE',f'PA_OUT_{ch}',f'RF_LOAD_{ch}',(180,60),(140,y))
 add(sp,f'JRF_OUT{ch}','Connector','Conn_Coaxial',f'RF OUTPUT CH{ch}',SMA,{1:f'RF_LOAD_{ch}',2:'GND'},(230,60),(185,y))
 add(sp,f'NTC{ch}','Device','Thermistor_NTC','10k B3950',RES,{1:f'PA{ch}_NTC',2:'GND'},(260,180),(105,y+6))
 resistor(sp,f'R_NTC{ch}','10k','+3V3',f'PA{ch}_NTC',(230,180),(130,y+10));cap(sp,f'C_NTC{ch}','100n',f'PA{ch}_NTC','GND',(290,180),(136,y+10))
# VPA monitor on CH1 external supply only, divided to ADC-safe nominal range.
resistor('CORE_POWER','R_VPA_H','330k','VPA_EXT_1','VPA_MON',(250,240),(40,140));resistor('CORE_POWER','R_VPA_L','33k','VPA_MON','GND',(275,240),(35,140));cap('CORE_POWER','C_VPAMON','100n','VPA_MON','GND',(300,240),(30,140))
# External RF sample ports replace unvalidated on-board directional couplers in this draft.
for i,n in enumerate(['RF1_FWD_V','RF1_REV_V','RF2_FWD_V','RF2_REV_V'],1):
 sh='RF_MONITORING';sx0=40+(i-1)*95;x=20+(i-1)*23;y=83
 add(sh,f'JMON{i}','Connector','Conn_Coaxial',f'EXTERNAL RF SAMPLE {i}',SMA,{1:f'DET_SAMPLE{i}',2:'GND'},(sx0,50),(x,y-10))
 cap(sh,f'C_DETIN{i}','22p C0G',f'DET_SAMPLE{i}',f'DET_INHI{i}',(sx0+30,50),(x,y-4))
 add(sh,f'UDET{i}',RF,'AD8313xRM','AD8313ARM','Package_SO:MSOP-8_3x3mm_P0.65mm',{1:'+5V',4:'+5V',6:'GND',5:'GND',2:f'DET_INHI{i}',3:f'DET_INLO{i}',7:n,8:n},(sx0+50,85),(x,y+4))
 cap(sh,f'C_DETLO{i}','1n',f'DET_INLO{i}','GND',(sx0+15,115),(x-4,y+6))
 cap(sh,f'C_DETV{i}','100n','+5V','GND',(sx0+45,125),(x+4,y+6))
 cap(sh,f'C_DETO{i}','1n',n,'GND',(sx0+70,115),(x,y+10))
# Assign ordinary numeric KiCad references; keep function labels in component metadata.
counts={}
for c in parts:
 c['function_ref']=c['ref']
 prefix='TH' if c['ref'].startswith('NTC') else 'FB' if c['ref'].startswith('FB') else c['ref'][0]
 counts[prefix]=counts.get(prefix,0)+1;c['ref']=prefix+str(counts[prefix]);c['uuid']=uid(c['ref'])
# Build hierarchical schematics, with actual global nets shared across sheets.

sheets=sorted(set(a['sheet'] for a in parts));root=uid('root')
notes={
 'MAIN_CONTROLLER':['DRAFT - external FPGA header only; MAX10 device not placed.','Current monitor inputs must remain within 0..3.3V.'],
 'CORE_POWER':['DRAFT: 5V supplies controller/fans. PA drain/bias converters NOT IMPLEMENTED.','VCAP capacitor/ESR and AMS1117 tantalum/thermal conditions require review.'],
 'FAN_CONTROL':['5V 4-wire fans; GPIO drives PWM signal, NOT motor current.','PWM inverter: MOSFET off => fan control high => full speed; verify fan model.'],
 'RF_MONITORING':['External directional coupler required. Sample ports are NOT 5W RF inputs.','Detector parts, values and calibration unverified.'],
 'RF_POWER_CH1':['DRAFT - NO VERIFIED MATCHING, BIAS OR THERMAL DESIGN.','R_PA_PWR1 DNP; use external drain/bias only after engineering verification.'],
 'RF_POWER_CH2':['DRAFT - NO VERIFIED MATCHING, BIAS OR THERMAL DESIGN.','R_PA_PWR2 DNP; use external drain/bias only after engineering verification.']}
def libkey(c):return c['lib']+':'+c['sym']
for sh in sheets:
 cs=[a for a in parts if a['sheet']==sh];schemuid=uid('schematic/'+sh);lib={}
 for c in cs:
  k=libkey(c)
  if k not in lib:
   
   try:a=symbol(c['lib'],c['sym'])
   except StopIteration:raise RuntimeError('Missing symbol '+k)
   a[1]=json.dumps(k);lib[k]=a
 if sh=='CORE_POWER':
  a=symbol('power','PWR_FLAG');a[1]='"power:PWR_FLAG"';lib['power:PWR_FLAG']=a
 page='A1' if sh=='FAN_CONTROL' else 'A3'
 out=[f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {schemuid}) (paper "{page}") (title_block (title "HPA 2CH / {sh} / INITIAL DRAFT") (rev "D0-NOT-FOR-FAB")) (lib_symbols']+[dump(a) for a in lib.values()]+[')']
 if sh=='CORE_POWER':
  for i,net in enumerate(['+5V','GND','VDDA']):cs.append(dict(ref='#FLG'+str(i+1),lib='power',sym='PWR_FLAG',value='PWR_FLAG',fp='',nets={'1':net},sch=(35+i*30,270),uuid=uid('flag'+str(i)),dnp=False))
 for c in cs:
  x,y=[round(a/1.27)*1.27 for a in c['sch']];k=libkey(c);pins=[p1 for sub in lib[k] if tag(sub)=='symbol' for p1 in sub if tag(p1)=='pin'];ref=c['ref']
  rx,ry=x-4,y-5;vx,vy=x+7,y+5
  if ref=='U1':rx,ry=x-10,y-95;vx,vy=x+25,y-95
  hide=' (hide yes)' if ref.startswith('#') else ''
  props=f'(property "Reference" "{ref}" (at {rx} {ry} 0) (effects (font (size 1 1)){hide})) (property "Value" "{c["value"]}" (at {vx} {vy} 0) (effects (font (size .9 .9)){hide})) (property "Footprint" "{c["fp"]}" (at {x} {y} 0) (effects (font (size 1 1)) (hide yes)))'
  if ref.startswith('#'):pcb='no';bom='no'
  else:pcb='yes';bom='yes'
  pinids=' '.join(f'(pin {child(p1,"number")[1]} (uuid {uid(ref+"pin"+val(child(p1,"number")[1]))}))' for p1 in pins)
  path='/'+root+'/'+uid('sheet/'+sh)
  out.append(f'(symbol (lib_id "{k}") (at {x} {y} 0) (unit 1) (in_bom {bom}) (on_board {pcb}) (dnp {"yes" if c.get("dnp") else "no"}) (uuid {c["uuid"]}) {props} {pinids} (instances (project "{NAME}" (path "{path}" (reference "{ref}") (unit 1)))))')
  used=set()
  for p1 in pins:
   num=val(child(p1,'number')[1]);at=child(p1,'at');px=round(x+float(at[1]),5);py=round(y-float(at[2]),5)
   if (px,py) in used:continue
   used.add((px,py));net=c['nets'].get(num)
   if net is None:out.append(f'(no_connect (at {px} {py}) (uuid {uid(ref+"NC"+num)}))');continue
   dx,dy={0:(-5.08,0),180:(5.08,0),90:(0,5.08),270:(0,-5.08)}[int(at[3])];ex=round(px+dx,5);ey=round(py+dy,5)
   out.append(f'(wire (pts (xy {px} {py}) (xy {ex} {ey})) (stroke (width 0) (type default)) (uuid {uid(ref+"W"+num)}))')
   out.append(f'(global_label "{net}" (shape bidirectional) (at {ex} {ey} 0) (effects (font (size .9 .9)) (justify left)) (uuid {uid(ref+"G"+num)}))')
 for i,t in enumerate(notes.get(sh,['INITIAL DRAFT - nominal values / layout not RF-validated.'])):out.append(f'(text "{t}" (at 20 {15+i*6} 0) (effects (font (size 1.3 1.3)) (justify left)) (uuid {uid(sh+"N"+str(i))}))')
 out.append(')');Path(sh+'.kicad_sch').write_text('\n'.join(out))
out=[f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {root}) (paper "A3") (title_block (title "HPA 2CH INITIAL DRAFT") (rev "D0-NOT-FOR-FAB")) (lib_symbols)']
for i,sh in enumerate(sheets):
 x=25+(i%3)*120;y=55+(i//3)*65
 out.append(f'(sheet (at {x} {y}) (size 90 40) (stroke (width .254) (type default)) (fill (color 0 0 0 0)) (uuid {uid("sheet/"+sh)}) (property "Sheetname" "{sh}" (at {x} {y-.7} 0) (effects (font (size 1.2 1.2)) (justify left bottom))) (property "Sheetfile" "{sh}.kicad_sch" (at {x} {y+40+.7} 0) (effects (font (size 1.1 1.1)) (justify left top))) (instances (project "{NAME}" (path "/{root}" (page "{i+2}")))))')
for i,t in enumerate(['INITIAL DRAFT: STM32 + FAN10 + 2x RF driver/PA sections + RF sample detectors.','FPGA DEVICE / INTEGRATED PA SUPPLY / DIRECTIONAL COUPLERS NOT IMPLEMENTED.','PCB placement and net assignment only. UNROUTED. NOT FOR FABRICATION OR POWER-UP.']):out.append(f'(text "{t}" (at 20 {15+8*i} 0) (effects (font (size 1.4 1.4)) (justify left)) (uuid {uid("TOPNOTE"+str(i))}))')
out.append(')');Path(NAME+'.kicad_sch').write_text('\n'.join(out))
# Actual six-layer PCB, with assigned nets and real footprints. No fictional FPGA pin numbers.
b=p.BOARD();b.SetCopperLayerCount(6);nets={}
for net in sorted({n for c in parts for n in c['nets'].values()}):q=p.NETINFO_ITEM(b,net) if hasattr(p,'NETINFO_ITEM') else p.NETINFO_ITEM(b,net);b.Add(q);nets[net]=q
for c in parts:
 lib,fp=c['fp'].split(':');f=p.FootprintLoad('/usr/share/kicad/footprints/'+lib+'.pretty',fp)
 if f is None:raise RuntimeError(c['fp'])
 f.SetReference(c['ref']);f.SetValue(c['value']);f.SetFPID(p.LIB_ID(lib,fp));f.SetPosition(v(*c['pcb']));f.SetOrientationDegrees(c['rot']);f.SetPath(p.KIID_PATH('/'+root+'/'+uid('sheet/'+c['sheet'])+'/'+c['uuid']));f.SetDNP(c['dnp']);b.Add(f)
 for pad in f.Pads():
  if pad.GetNumber() in c['nets']:pad.SetNet(nets[c['nets'][pad.GetNumber()]])
 f.Value().SetVisible(False);f.Reference().SetTextSize(v(.8,.8));f.Reference().SetTextThickness(p.FromMM(.12));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));f.Reference().SetPosition(f.GetPosition()+v(0,-2.5));
for a,z in [((0,0),(200,0)),((200,0),(200,160)),((200,160),(0,160)),((0,160),(0,0))]:
 s=p.PCB_SHAPE();s.SetShape(p.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*z));s.SetWidth(p.FromMM(.05));s.SetLayer(p.Edge_Cuts);b.Add(s)
for i,(x,y) in enumerate([(5,5),(195,5),(5,155),(195,155)]):
 f=p.FootprintLoad('/usr/share/kicad/footprints/MountingHole.pretty','MountingHole_3.2mm_M3');f.SetReference('H'+str(i+1));f.SetBoardOnly(True);f.SetPosition(v(x,y));f.Reference().SetVisible(False);f.Value().SetVisible(False);b.Add(f)
for text,x,y,size in [('HPA 2CH / INITIAL DRAFT',100,5,1.8),('UNROUTED - NOT FOR FAB / POWER-UP',92,154,1.4),('MAX10 RESERVED - NOT PLACED',135,95,1),('200 x 160mm / 6 COPPER LAYERS',95,158,.9),('EXT DRAIN / NEGATIVE BIAS REQUIRED',110,11,1),('FAN1-5',163,78,.8),('FAN6-10',185,78,.8)]:
 t=p.PCB_TEXT(b);t.SetText(text);t.SetPosition(v(x,y));t.SetTextSize(v(size,size));t.SetTextThickness(p.FromMM(.15));t.SetLayer(p.F_SilkS);b.Add(t)
for a,z in [((121,98),(150,98)),((150,98),(150,127)),((150,127),(121,127)),((121,127),(121,98))]:
 s=p.PCB_SHAPE();s.SetShape(p.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*z));s.SetWidth(p.FromMM(.15));s.SetLayer(p.Dwgs_User);b.Add(s)
# Internal ground reference areas; fill retained for the layout draft, not connectivity sign-off.
for layer in [p.In1_Cu,p.In4_Cu]:
 z=p.ZONE(b);z.SetLayer(layer);z.SetNet(nets['GND']);z.SetLocalClearance(p.FromMM(.25));z.SetMinThickness(p.FromMM(.2));z.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS);o=z.Outline();o.NewOutline()
 for x,y in [(.6,.6),(199.4,.6),(199.4,159.4),(.6,159.4)]:o.Append(p.FromMM(x),p.FromMM(y))
 b.Add(z)
# Unfilled zones intentionally retained for initial layout; no connectivity sign-off.
tb=b.GetTitleBlock();tb.SetTitle('HPA 2CH INITIAL DRAFT - UNROUTED');tb.SetRevision('D0');b.SetTitleBlock(tb)
p.SaveBoard(NAME+'.kicad_pcb',b)
# Reuse a valid project schema, with draft rules and actual file name.
proj=json.loads((R/'tools/project_template.json').read_text());proj['meta']['filename']=NAME+'.kicad_pro';proj['board']['design_settings']['rules'].update(min_clearance=.15,min_track_width=.15);Path(NAME+'.kicad_pro').write_text(json.dumps(proj,indent=2))
libs=sorted({c['lib'] for c in parts}|{'power'});Path('sym-lib-table').write_text('(sym_lib_table (version 7) '+''.join(f'(lib (name "{lib}") (type "KiCad") (uri "${{KICAD9_SYMBOL_DIR}}/{lib}.kicad_sym") (options "") (descr ""))' for lib in libs)+')')
Path('tools/components.json').write_text(json.dumps(parts,indent=2))
with Path('BOM_DRAFT.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['Reference','Function','Value','Footprint','DNP','Sheet']);w.writerows((c['ref'],c['function_ref'],c['value'],c['fp'],c['dnp'],c['sheet']) for c in parts)
print('Created',NAME,'with',len(parts),'components,',len(nets),'nets,',len(sheets),'child schematics, 6-layer PCB.')
