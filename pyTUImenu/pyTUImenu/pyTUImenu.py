
from typing import Callable,Optional
from rich.padding import Padding
from rich import print
import os
from typing import NamedTuple

class funcs(NamedTuple):
    name:str
    func:Optional[Callable]
    arg:Optional[object|list]
class funcs_list():
    func_list:list=[]
    top_index:int
    back_index:int
    exit_index:int
class pyTUImenu():
    """メニュー表示をする
    """
    def __init__(
        self,
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
        self.__list:funcs_list=funcs_list()
        self.__menu_headder:list=[]
        self.__menu_level:list[str]=[top_menu_name]
        self.__is_level_display=enable_level_display
        self.__is_jump_top=is_add_jump_top
        self.__is_back=is_add_back
        self.__optional_top_func:list[funcs]|funcs
        self.__is_optional_top_func:bool=False
        self.__backu_func=funcs('1つ前に戻る',None,None)
        self.__jump_top_func=funcs(top_menu_name+'に戻る',None,None)
        self.__exit_func=(menu_name+'を終了する',None,None)
        self.__end_message=None

    def add_headder(self,headder):
        """ヘッダーを追加する
        Args:
            headder (_type_): ヘッダー
        """
        self.__menu_headder.append(headder)
    def add_top_func(self,function_list:list[funcs]|funcs):
        """常に一番上に表示する機能を追加する

        Args:
            function_list (function_lists): _description_
        """
        self.__is_optional_top_func=True
        self.__optional_top_func=function_list
    def add_end_message(self,end_message):
        self.__end_message=end_message
    def get_levels(self):
        a="メニュー階層："
        for l in self.__menu_level:
            a+=str(l)+"=>"
        return Padding(a,1)
    def __init_menu(self):
        """オプションに合わせてメニューリストを初期化する
        """
        if self.__is_optional_top_func:
            if isinstance(self.__optional_top_func,list):
                self.__list.func_list+=self.__optional_top_func
            else: self.__list.func_list.append(self.__optional_top_func)
        #FunctionList+=[('プログラム終了',ControlRRR.AutoRRR.theEnd,False)]
        if len(self.__menu_level)>=2:
            #一つ前にもどるコマンドを追加する
            if self.__is_back and not self.__backu_func in self.__list.func_list:
                self.__list.func_list.append(self.__backu_func)
                self.__list.back_index=len(self.__list.func_list)-1
            elif self.__backu_func in self.__list.func_list:
                self.__list.back_index=self.__list.func_list.index(self.__backu_func)
            #トップに戻る
            if self.__is_jump_top and not self.__jump_top_func in self.__list:
                self.__list.append(self.__jump_top_func)
                jump_top_func_index=len(self.__list)-1
            elif self.__jump_top_func in self.__list:
                jump_top_func_index=self.__list.index(self.__jump_top_func)
        elif not self.__exit_func in self.__list:
            self.__list.append(self.__exit_func)
            exit_func_index=len(self.__list)-1
        elif self.__exit_func in self.__list:
            exit_func_index=self.__list.index(self.__exit_func)
    def __MenuLoop(self):
        display_list:list=[]
        back_func_index=0
        jump_top_func_index=0
        exit_func_index=0
        while True:
            display_list.clear()
            if self.__menu_headder!=None:
                for h in self.__menu_headder:
                    display_list.append(h)
            if self.__is_level_display:
                display_list.append(self.get_levels())
            display_list.append(Padding("機能を選択してください\n",(0,1),style='b'))
            for count,doc in enumerate(self.__list,start=1):
                display_list.append(Padding('[blue]'+str(count)+'[/blue][white]'+':'+doc[0]+'[/white]',(0,1)))
            for t in display_list:
                print(t)
            mode=input('\n番号を入力=> ')
            os.system('cls')
            if mode.isdigit():
                mode=int(mode)-1
                #選択した番号が範囲内であれば
                if mode<=len(self.__list)-1:
                    execute=self.__list[mode][1]
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
                    if self.__list[mode][1] is None:
                        print("\n機能が未実装です\n")
                        continue
                    #関数が指定されていたら実行する
                    elif isinstance(execute,Callable):
                        print(self.__list[mode][0]+"を実行します\n")
                        if len(self.__list[mode])==3:
                            execute(self.__list[mode][2])
                        else:
                            execute()
                        if self.__end_message is not None:
                            print(self.__end_message)
                        #return
                    elif isinstance(self.__list[mode][1],list):
                        next_list=self.__list[mode][1]
                        if next_list is not None and not isinstance(next_list,Callable):
                            next_leve=self.__MenuLoop(self.__function_list=next_list,top_menu_name=self.__list[mode][0])
                            if not next_leve==len(self.__menu_level):
                                del self.__menu_level[-1]
                                return len(self.__menu_level)
                                break
                    else:
                        return
                elif mode==str(len(self.__list)+1):
                    return
    def start_menu(self,funcs:funcs):
        if isinstance(funcs.arg,list):
            self.__list=funcs.arg
        self.__init_menu()
        self.__MenuLoop(self.__list,False)

if __name__=="__main__":
    f1=funcs('print1',print,'print1')
    f2=funcs('print1',print,'print1')
    f3=funcs('print1',print,'print1')
    f4=funcs('print1',print,'print1')
    f5=funcs('print1',print,'print1')
    top=funcs('top',pyTUImenu().start_menu,[f1,f2,f3,f4,f5])
    pyui=pyTUImenu()
    pyui.start_menu(top)