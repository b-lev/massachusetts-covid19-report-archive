

import os
import sys

def nonum(string):
  return("".join([x for x in string if not (x >= '0' and x <= '9')]))


COUNTIES = ['Barnstable', 'Berkshire','Bristol', 'Dukes','Essex','Franklin', 'Hampden', 'Hampshire','Middlesex', 'Nantucket','Norfolk', 'Plymouth','Suffolk', 'Worcester','Unknown']

GENDERS = {'Female':"Gender_Female",'Male':"Gender_Male",'Unknown':"Gender_unknown"}

DEATHS = {'Attributed to COVID-19':'Deaths'}

AGE = {'≤19 years of age':'age_0-19', '20-29 years of age':'age_20-29', '30-39 years of age':'age_30-39', '40-49 years of age':'age_40-49', '50-59 years of age':'age_50-59', '60-69 years of age':'age_60-69', '70-79 years of age':'age_70-79', '≥ 80 years of age':'age_80-', 'Unknown':'age_unknown'}

LTCF = {'Residents/Healthcare workers of Long-Term Care Facilities':'LTCF_Residents',
'Long-Term Care Facilities Reporting At Least One Case of COVID-19':'LTCF_one_plus_case', 'Deaths Reported in Long-Term Care Facilities':'LTCF_deaths'}

HOSP ={ 'Patient was hospitalized':'Hospitalized_yes', 'Patient was not hospitalized':'Hospitalized_no', 'Under Investigation':'Hospitalized_under_investigation'}

RACE = {'Hispanic':'hispanic', 'Non-Hispanic White':'white', 'Non-Hispanic Black/African American':'black/african american', 'Non-Hispanic Asian':'asian', 'Non-Hispanic Other':'other', 'Unknown':'unknown', 'Missing':'missing'}

columns={}
for key in COUNTIES+list(GENDERS.values())+ list(AGE.values())+ list(LTCF.values())+ list(DEATHS.values())+ list(RACE.values()):
  columns[key]=0

file = sys.argv[1]
print(os.system('textutil -convert txt %s' % file))
with open('%s.txt' % file[:-5],'r') as fd:
  lines = fd.read().split('\n')
  cnt = 0

  while (lines[cnt][0:6]!="As of "):
    print(lines[cnt])
    cnt+=1
  date = lines[cnt][6:]
  print(date)
  while (lines[cnt] != "Sex"):
    if lines[cnt].strip() in COUNTIES:
      columns[lines[cnt].strip()]=lines[cnt+1]
      cnt+=2
    else:
      print(lines[cnt])
      cnt+=1
  assert lines[cnt] == "Sex"

  while (lines[cnt] != "Age Group"):
    if lines[cnt].strip() in GENDERS:
      idx= GENDERS[lines[cnt].strip()]
      columns[idx]=lines[cnt+1]
      cnt+=2
    else:
      print(lines[cnt])
      cnt+=1
  assert lines[cnt] == "Age Group"

  while (lines[cnt] != "Deaths"):
    if lines[cnt].strip() in AGE.keys():
      idx= AGE[lines[cnt].strip()]
      columns[idx]=lines[cnt+1]
      cnt+=2
    else:
      cnt+=1
  assert lines[cnt] == "Deaths"

  assert lines[cnt+1] =='Attributed to COVID-19'
  cnt+=2
  while (lines[cnt].strip()==""):
      cnt+=1
  columns['Deaths'] = lines[cnt]
  print("Deaths:",columns['Deaths'])
  cnt+=1
  while (lines[cnt])=="":
    cnt+=1
  assert lines[cnt] == 'COVID-19 Cases in Long-Term Care Facilities*', print("got: ["+lines[cnt]+"]")
  #
  # cnt+=1
  # while (lines[cnt] != "Total Cases and Deaths by Race/Ethnicity"):
  #   if nonum(lines[cnt].strip()) in HOSP.keys():
  #     idx = HOSP[nonum(lines[cnt].strip())]
  #     columns[idx]=lines[cnt+1]
  #     cnt+=2
  #   else:
  #     if lines[cnt].strip()!="":
  #       print("H no parse: ["+lines[cnt]+"]")
  #   cnt+=1


  cnt+=1
  while (lines[cnt].strip() != "Confirmed Cases"):
    if lines[cnt].strip() in LTCF.keys():
      idx = LTCF[lines[cnt].strip()]
      columns[idx]=lines[cnt+1]
      cnt+=2
    else:
      print("LTCF no parse: ["+lines[cnt]+"]")
      cnt+=1

  assert lines[cnt] == 'Confirmed Cases', print("got: ["+lines[cnt]+"]")
  cnt+=4
  while (lines[cnt] != "Total"):
    if nonum(lines[cnt].strip()) in RACE.keys():
      race = RACE[nonum(lines[cnt].strip())]
      idx = "race_confirmed_%s" % race
      value = lines[cnt+1]
      columns[idx]=value[0:value.index(" ")]
      idx = "race_deaths_%s" % race
      value = lines[cnt+2]
      columns[idx]=value[0:value.index(" ")]
      cnt+=3
    else:
      if lines[cnt].strip()!="":
        print("Race not in keys: ["+lines[cnt]+"]", " ",nonum(lines[cnt]))
      cnt+=1

  assert lines[cnt]=='Total'
  columns['confirmed']=lines[cnt+1]
  print("Confirmed:",columns['confirmed'])
  assert lines[cnt+2]==columns['Deaths'],print("\ndeaths not lining up with", columns['Deaths'],"-->",lines[cnt+2])
  cnt+=3

  while lines[cnt].find("Reported Deaths")==-1:
    # print("RD:",lines[cnt])
    cnt+=1
  assert lines[cnt+1]=='Sex'
  assert lines[cnt+2]=='Age'
  assert lines[cnt+3]=='County'
  assert lines[cnt+4]=='Preexisting Conditions'
  assert lines[cnt+5]=='Hospitalized'
  cnt+=5
  print("Start of deaths:",lines[cnt+1])
  deaths=[]
  while lines[cnt+1] in ['Female','Male','Unknown'] :
    print(lines[cnt+1:cnt+6])
    deaths+=[[lines[cnt+1],lines[cnt+2],lines[cnt+3],lines[cnt+4],lines[cnt+5]]]
    assert lines[cnt+1] in ['Female','Male','Unknown'] , print(lines[cnt+1])
    cnt+=5

  print("Deaths:" , len(deaths))

  #skip lab data
  while lines[cnt].find('Total Patients Tested*')!=0:
    cnt+=1
  cnt+=1

  assert lines[cnt]==columns['confirmed'], print("expecting ",columns['confirmed'])
  columns['Test_positive']=lines[cnt]
  columns['Test_negative']=lines[cnt+1]
  columns['date']=file[-15:-5]

  with open(file[:-5]+".deaths.csv",'w') as fd:
    for x in deaths:
     fd.write(columns['date']+","+",".join(x)+"\n")

  cols = [key for key in list(["date",'confirmed'])+ COUNTIES+list(GENDERS.values())+ list(AGE.values())+list(DEATHS.values())+  list(LTCF.values())+ list(["race_confirmed_"+ x for x in RACE.values()]) + list(["race_deaths_"+ x for x in RACE.values()])+ list(['Test_positive','Test_negative'])]
  with open('MA-stats.csv','a') as fd:
    fd.write(",".join([columns[col] for col in cols]))
    fd.write("\n")
