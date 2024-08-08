from pyTUImenu import funcs
from pyTUImenu import pyTUImenu
from rich.padding import Padding
import os

if __name__=="__main__":
    f1=funcs('print1_1',print,'print1_1')
    f2=funcs('print1_2',print,'print1_2')
    f3=funcs('print1_3',print,'print1_3')
    f4=funcs('print1_4',print,'print1_4')
    f2_1=funcs('print2_1',print,'print2_1')
    f2_2=funcs('print2_2',print,'print2_2')
    f2_3=funcs('print2_3',print,'print2_3')
    f3_1=funcs('print3_1',print,'print3_1')
    f3_2=funcs('print3_2',print,'print3_2')
    f3_3=funcs('print3_3',print,'print3_3')
    pyui=pyTUImenu()
    headder=Padding("[green]"+os.getlogin()+"でログインしています[/green]",(0,1))
    pyui.add_headder(headder=headder)
    three=funcs('therd',pyui.start_menu,[f3_1,f3_2,f3_3])
    tow=funcs('next',pyui.start_menu,[f2_1,f2_2,f2_3,three])
    top=funcs('top',pyui.start_menu,[f1,f2,f3,f4,tow])
    pyui.start_menu(top)