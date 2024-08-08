import logging
from typing import Callable,Optional
from rich.padding import Padding
from rich import print
from rich.logging import RichHandler

import os
from typing import NamedTuple

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler()]
    )
log = logging.getLogger("rich")

class funcs(NamedTuple):
    name:str
    func:Optional[Callable]
    arg:Optional[object|list]=None
class funcs_list():
    func_list:list=[]
    top_index:int|None=None
    back_index:int|None=None
    exit_index:int|None=None
    jump_index:int|None=None
class pyTUImenu():
    """メニュー表示をする
    """
    def __init__(
        self,
        enable_level_display:bool=True,
        is_add_jump_top:bool=True,
        is_add_back:bool=True,
        top_menu_name='',
        menu_name='アプリ',
        logger=log
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
        self.__menu_level:list[str]=[]
        self.__is_level_display=enable_level_display
        self.__is_jump_top=is_add_jump_top
        self.__is_back=is_add_back
        self.__optional_top_func:list[funcs]|funcs
        self.__is_optional_top_func:bool=False
        self.__backu_func=funcs('1つ前に戻る',None,None)
        self.__jump_top_func:funcs
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
    def __init_menu(self,ls:funcs_list):
        """オプションに合わせてメニューリストを初期化する
        """
        log.debug('start init menu')
        if self.__is_optional_top_func:
            if isinstance(self.__optional_top_func,list):
                ls.func_list+=self.__optional_top_func
            else: ls.func_list.append(self.__optional_top_func)
        #FunctionList+=[('プログラム終了',ControlRRR.AutoRRR.theEnd,False)]
        if len(self.__menu_level)>=2:
            if len(self.__menu_level)>=3:
            #一つ前にもどるコマンドを追加する
                log.debug('func_list>=2')
                if self.__is_back and not self.__backu_func in ls.func_list:
                    log.debug('setting back func')
                    ls.func_list.append(self.__backu_func)
                    ls.back_index=len(ls.func_list)-1
                elif self.__backu_func in ls.func_list:
                    ls.back_index=ls.func_list.index(self.__backu_func)
            #トップに戻る
            if self.__is_jump_top and not self.__jump_top_func in ls.func_list:
                ls.func_list.append(self.__jump_top_func)
                ls.top_index=len(ls.func_list)-1
                log.debug('add top')
            elif self.__jump_top_func in ls.func_list:
                ls.top_index=ls.func_list.index(self.__jump_top_func)
                log.debug('add top2')
        elif not self.__exit_func in ls.func_list:
            ls.func_list.append(self.__exit_func)
            ls.exit_index=len(ls.func_list)-1
        elif self.__exit_func in ls.func_list:
            ls.exit_index=ls.func_list.index(self.__exit_func)
        #log.debug(f'{ls.back_index=}')
    def __MenuLoop(self,ls:funcs_list):
        #self.__init_menu()
        display_list:list=[]
        while True:
            display_list.clear()
            if self.__menu_headder!=None:
                for h in self.__menu_headder:
                    display_list.append(h)
            if self.__is_level_display:
                display_list.append(self.get_levels())
            display_list.append(Padding("機能を選択してください\n",(0,1),style='b'))
            for count,doc in enumerate(ls.func_list,start=1):
                display_list.append(Padding('[blue]'+str(count)+'[/blue][white]'+':'+doc[0]+'[/white]',(0,1)))
            for t in display_list:
                print(t)
            mode=input('\n番号を入力=> ')
            os.system('cls')
            if mode.isdigit():
                mode=int(mode)-1
                #選択した番号が範囲内であれば
                if mode<=len(ls.func_list)-1:
                    execute=ls.func_list[mode][1]
                    #1つ前に戻る
                    if isinstance(ls.back_index,int):
                        if mode==ls.back_index and not ls.back_index==0:
                            del self.__menu_level[-1]
                            log.debug(f'{len(self.__menu_level)=}')
                            return len(self.__menu_level)
                    #トップに戻る
                    if mode==ls.top_index and not ls.top_index==0:
                        del self.__menu_level[-1]
                        return 1
                    #終了する
                    if mode==ls.exit_index and not ls.exit_index==0:
                        return
                    #関数が指定されていない場合
                    if ls.func_list[mode][1] is None:
                        print("\n機能が未実装です\n")
                        continue
                    #関数が指定されていたら実行する
                    elif isinstance(execute,Callable):
                        log.debug(f'{ls.func_list[mode].name=}')
                        if isinstance(ls.func_list[mode].arg,object):
                            log.debug(ls.func_list[mode].func)
                            if not ls.func_list[mode].func.__name__==pyTUImenu.start_menu.__name__:
                                print(ls.func_list[mode].name+"を実行します\n")
                                log.debug('execute function')
                                if ls.func_list[mode].arg==None:
                                    ls.func_list[mode].func()
                                else:
                                    ls.func_list[mode].func(ls.func_list[mode].arg)
                            else:
                                self.__menu_level.append(ls.func_list[mode].name)
                                next_level=ls.func_list[mode].func(ls.func_list[mode],self.__menu_level)
                                log.debug(f'{ls}')
                                if not next_level==len(self.__menu_level):
                                    del self.__menu_level[-1]
                                    return len(self.__menu_level)
                        else:
                            execute()
                        if self.__end_message is not None:
                            print(self.__end_message)
                        #return
                    elif isinstance(ls.func_list[mode][1],list):
                        next_list=ls.func_list[mode][1]
                        if next_list is not None and not isinstance(next_list,Callable):
                            pass
                            #if not next_leve==len(self.__menu_level):
                            #    del self.__menu_level[-1]
                            #    return len(self.__menu_level)
                            #    break
                    else:
                        return
                elif mode==str(len(ls.func_list)+1):
                    return
    def start_menu(self,func:funcs,level_list:list[str]|None=None):
        ls=funcs_list()
        if isinstance(func.arg,list):
            ls.func_list=func.arg
        if isinstance(level_list,list):
            log.debug(f'{level_list=}')
            self.__menu_level=level_list
        if self.__menu_level==[]:
            log.debug(f'add {func.name}')
            self.__menu_level.append(func.name)
        self.__jump_top_func=funcs(self.__menu_level[0]+'に戻る',None,None)
        self.__init_menu(ls)
        next_level=self.__MenuLoop(ls)

        self.__init_menu(ls)
        return next_level
