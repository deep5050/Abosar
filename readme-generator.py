import pandas as pd
# from markdownTable import markdownTable
from tabulate import tabulate

# https://www.onnoalo.com/onnoalo
# https://www.anandabazar.com/rabibashoriyo

def get_rabibasariya():
    with open('rabibasariya', 'r') as f:
        rabibasariya = f.readlines()
        return rabibasariya

def get_onnoalo():
    with open('onnoalo', 'r') as f:
        onnoalo_arr = f.readlines()
        return onnoalo_arr

def make_readme():
    rabibasariya_arr = get_rabibasariya()
    onnoalo_arr = get_onnoalo()

    # first_column is always rabibasariya
    if len(rabibasariya_arr) > len(onnoalo_arr):
        first_column = rabibasariya_arr
        remaining_len = len(rabibasariya_arr) - len(onnoalo_arr)
        blank_array = [''] * remaining_len
        second_column = onnoalo_arr + blank_array
    else:
        second_column = onnoalo_arr
        remaining_len = len(onnoalo_arr) - len(rabibasariya_arr)
        blank_array = [''] * remaining_len
        first_column =  rabibasariya_arr + blank_array
    


    data = {'রবিবাসরীয়':  first_column,
            'অন্য আলো': second_column,
            }
    df = pd.DataFrame(data)
    markdown_table = tabulate(df, headers='keys', tablefmt='pipe', showindex=True)

    readme_header = """
<div align=center>
    <p align=center>
    <img align=center src=https://github.com/deep5050/random-shits-happen-here/assets/27947066/6c3e568c-d8c6-4f8f-9c79-18bbb68924cd width=400px>
    </p>
<p align=center>
<a href=https://t.me/rabibasariya> <img align=center src=https://user-images.githubusercontent.com/27947066/264323419-b5c9d0bd-2947-4322-adf7-13cb3f460e4c.png > </a>
</p>
<p align=center>
    <img align=center src=https://github.com/deep5050/Abosar/actions/workflows/automate.yml/badge.svg >
</p>
<p>
<h1 align=center > অবসর ( ABOSAR ) </h1>
</p>

**A collection of short Bengali stories web scraped from various Bengali
eMagazines and eNewspapers**

<h4> Stories are added here and on telegram, every Sunday at around 1:30 P.M 🕐 automatically</h4>

 <p align=center>
<img align=center width="500px" alt="UPI" src="https://user-images.githubusercontent.com/27947066/235618869-8c9d9bce-096d-469e-8f61-c29cc01eacc3.png">
</p>
</div>

## DISCLAIMER

The stories and images posted on this platform are not my own creations. All copyright and intellectual property rights are attributed to their original authors and creators. The contents are shared here for educational purposes only. No copyright infringement or strike is intended. If you are the original author or copyright holder of any content posted here and have concerns, please contact me at d.pal5050@gmail.com for appropriate credit or removal. Your rights and ownership will be respected and acknowledged.

Source & Copyright: www.anandabazar.com/rabibashoriyo/

## SOURCES

1. https://www.anandabazar.com/supplementary/rabibashoriyo/
2. https://www.prothomalo.com/onnoalo

(More will be added soon )
## INDEX"""

    new_readme_text = readme_header + "\n" + markdown_table

    with open('README.md','w') as f:
        f.write(new_readme_text)


make_readme()