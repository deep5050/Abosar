import pandas as pd
from markdownTable import markdownTable
from tabulate import tabulate

# https://www.onnoalo.com/onnoalo
# https://www.anandabazar.com/rabibashoriyo

def get_rabibasariya():
    with open('rabibasariya', 'r') as f:
        rabibasariya = f.readlines()
        return rabibasariya

def get_onnoalo():
    get_first_column_length = len(get_rabibasariya())
    # generate blank array for now
    blank_array = [''] * get_first_column_length
    return blank_array

rabibasariya_arr = get_rabibasariya()
onnoalo_arr = ['a','b']

data = {'রবিবাসরীয়':  get_rabibasariya(),
        'অন্য আলো': get_onnoalo(),
        }
df = pd.DataFrame(data)
markdown_table = tabulate(df, headers='keys', tablefmt='pipe', showindex=True)
# print(markdown_table)

readme_header = """
<div align=center>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
  <path fill="#273036" fill-opacity="1" d="M0,256L21.8,240C43.6,224,87,192,131,197.3C174.5,203,218,245,262,234.7C305.5,224,349,160,393,117.3C436.4,75,480,53,524,64C567.3,75,611,117,655,133.3C698.2,149,742,139,785,133.3C829.1,128,873,128,916,138.7C960,149,1004,171,1047,149.3C1090.9,128,1135,64,1178,48C1221.8,32,1265,64,1309,106.7C1352.7,149,1396,203,1418,229.3L1440,256L1440,0L1418.2,0C1396.4,0,1353,0,1309,0C1265.5,0,1222,0,1178,0C1134.5,0,1091,0,1047,0C1003.6,0,960,0,916,0C872.7,0,829,0,785,0C741.8,0,698,0,655,0C610.9,0,567,0,524,0C480,0,436,0,393,0C349.1,0,305,0,262,0C218.2,0,175,0,131,0C87.3,0,44,0,22,0L0,0Z"></path>
</svg>
  
<img src="metadata/images/rabibasariya/abosar.png" title="(c) Absurd Design"  height="400px" width="400px" align=center>

<p>
<h1 align=center > অবসর ( ABOSAR ) </h1>
</p>

**A Collection Of Short Bengali Stories Web Scraped From Various Bengali
eMagazines And eNewspapers**

<h4> stories are added every Sunday on 8 A.M. automatically ( CRON jobs and Github CI) </h4>
</div>

## SOURCES ![GitHub CI](https://github.com/deep5050/Abosar/workflows/GitHub%20CI/badge.svg)

<img src=onnoalo.svg width=200px >


<img src=anandabazar.png width=200px>

1. https://www.anandabazar.com/supplementary/rabibashoriyo/
2. https://www.prothomalo.com/onnoalo

( more will be added soon )

## INDEX"""

new_readme_text = readme_header + "\n" + markdown_table

with open('README.md','w') as f:
    f.write(new_readme_text)
