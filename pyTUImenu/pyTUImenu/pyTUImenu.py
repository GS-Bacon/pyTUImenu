
from typing import Callable,Optional
from rich.padding import Padding
from rich import print
import rich
import os

type function_lists=list[tuple[str,Optional[function_lists|Callable],Optional[object]]]

class pyTUImenu():
    """メニュー表示をする
    """
    def __init__(
        self,
        function_list:function_lists,
        enable_level_display:bool=True,
        is_add_jump_top:bool=True,
        is_add_back:bool=True,
        top_menu_name='トップ',
        menu_name='アプリ'
        ) -> None:
        """_summary_

        Args:
            function_list (function_lists): メニュー用の関数のリスト
            enable_level_display (bool, optional): メニュー階層表示をするかどうか. Defaults to True.
            is_add_jump_top (bool, optional): トップにジャンプする項目を追加するかどうか. Defaults to True.
            is_add_back (bool, optional): 1つ前に戻るを項目を追加するかどうか. Defaults to True.
            top_menu_name (str, optional): トップメニューの名前. Defaults to 'トップ'.
            menu_name (str, optional): メニューの名前. Defaults to 'アプリ'.
        """
        self.__function_list=function_list
        self.__menu_headder:list=[]
        self.__menu_level:list[str]=[top_menu_name]
        self.__is_level_display=enable_level_display
        self.__is_jump_top=is_add_jump_top
        self.__is_back=is_add_back
        self.__optional_top_func:function_lists
        self.__is_optional_top_func:bool=False
        self.__backu_func=('1つ前に戻る',None,None)
        self.__jump_top_func=(top_menu_name+'に戻る',None,None)
        self.__exit_func=(menu_name+'を終了する',None,None)
        self.__end_message=None

    def add_headder(self,headder):
        """ヘッダーを追加する
        Args:
            headder (_type_): ヘッダー
        """
        self.__menu_headder.append(headder)
    def add_top_func(self,function_list:function_lists):
        self.__is_optional_top_func=True
        self.__optional_top_func=function_list
    def add_end_message(self,end_message):
        self.__end_message=end_message
    def start_menu(self):
        self.__MenuLoop(self.__function_list,False)
    def get_levels(self):
        a="メニュー階層："
        for l in self.__menu_level:
            a+=str(l)+"=>"
        return Padding(a,1)
    def __MenuLoop(self,function_list:function_lists,top_menu_name:str|bool=False):
        if isinstance(top_menu_name,str):
            self.__menu_level.append(top_menu_name)
        display_list:list=[]
        back_func_index=0
        jump_top_func_index=0
        exit_func_index=0
        if self.__is_optional_top_func:
            function_list+=self.__optional_top_func
        #FunctionList+=[('プログラム終了',ControlRRR.AutoRRR.theEnd,False)]
        if len(self.__menu_level)>=2:
            #一つ前にもどるコマンドを追加する
            if self.__is_back and not self.__backu_func in function_list:
                function_list.append(self.__backu_func)
                back_func_index=len(function_list)-1
            elif self.__backu_func in function_list:
                back_func_index=function_list.index(self.__backu_func)
            #トップに戻る
            if self.__is_jump_top and not self.__jump_top_func in function_list:
                function_list.append(self.__jump_top_func)
                jump_top_func_index=len(function_list)-1
            elif self.__jump_top_func in function_list:
                jump_top_func_index=function_list.index(self.__jump_top_func)
        elif not self.__exit_func in function_list:
            function_list.append(self.__exit_func)
            exit_func_index=len(function_list)-1
        elif self.__exit_func in function_list:
            exit_func_index=function_list.index(self.__exit_func)
        while True:
            display_list.clear()
            if self.__menu_headder!=None:
                for h in self.__menu_headder:
                    display_list.append(h)
            if self.__is_level_display:
                display_list.append(self.get_levels())
            display_list.append(Padding("機能を選択してください\n",(0,1),style='b'))
            for count,doc in enumerate(function_list,start=1):
                display_list.append(Padding('[blue]'+str(count)+'[/blue][white]'+':'+doc[0]+'[/white]',(0,1)))
            for t in display_list:
                print(t)
            mode=input('\n番号を入力=> ')
            os.system('cls')
            if mode.isdigit():
                mode=int(mode)-1
                #選択した番号が範囲内であれば
                if mode<=len(function_list)-1:
                    execute=function_list[mode][1]
                    #1つ前に戻る
                    if mode==back_func_index and not back_func_index==0:
                        del self.__menu_level[-1]
                        return len(self.__menu_level)
                    #トップに戻る
                    if mode==jump_top_func_index and not jump_top_func_index==0:
                        del self.__menu_level[-1]
                        return 1
                    #終了する
                    if mode==exit_func_index and not exit_func_index==0:
                        return
                    #関数が指定されていない場合
                    if function_list[mode][1] is None:
                        print("\n機能が未実装です\n")
                        continue
                    #関数が指定されていたら実行する
                    elif isinstance(execute,Callable):
                        print(function_list[mode][0]+"を実行します\n")
                        if len(function_list[mode])==3:
                            execute(function_list[mode][2])
                        else:
                            execute()
                        if self.__end_message is not None:
                            print(self.__end_message)
                        #return
                    elif isinstance(function_list[mode][1],list):
                        next_list=function_list[mode][1]
                        if next_list is not None and not isinstance(next_list,Callable):
                            next_leve=self.__MenuLoop(function_list=next_list,top_menu_name=function_list[mode][0])
                            if not next_leve==len(self.__menu_level):
                                del self.__menu_level[-1]
                                return len(self.__menu_level)
                                break
                    else:
                        return
                elif mode==str(len(function_list)+1):
                    return
def printNo(num:int):
    print(f'No.{num}')
if __name__ == '__main__':
    f_list:function_lists=[
        ("No.1",printNo,1),
        ("No.2",printNo,2),
        ("No.3",printNo,3),
        ("No.4",printNo,4),
        ("No.5~8",[
            ("No.5",printNo,5),
            ("No.6",printNo,6),
            ("No.7",printNo,7),
            ("No.8",printNo,8),
        ],None)
    ]
    menu=pyTUImenu(function_list=f_list)
    menu.add_headder("test menu")
    menu.start_menu()