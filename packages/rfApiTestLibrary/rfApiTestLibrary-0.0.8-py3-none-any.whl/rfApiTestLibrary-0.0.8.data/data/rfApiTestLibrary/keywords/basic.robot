*** Settings ***
Documentation  处理基础的关键字文件, 引用请使用Resource atBasicLibray/keywords/[ sc/basic.html | basic.robot]
Library   ../basic.py

*** Keywords ***
验证是None
    [Documentation]  功能:唯一一个参数[obj],如果是None,什么都不发生。如果不是None，报错。
    ...       英文关键字[ ../keywords/basic.doc.html#Should%20be%20none | Should be none ]。
    ...       具体代码请参考atBasicLibrary/basic.py的 [../library/basic.py.doc.html#At%20Should%20Be%20None | at_should_be_none]方法。
    [Arguments]              ${obj}   ${message}=${None}
    at should be none        ${obj}   ${message}

Should be none
    [Documentation]  功能:唯一一个参数[obj],如果是None,什么都不发生。如果不是None，报错。
    ...       中文关键字[ ../keywords/basic.doc.html#验证是None | 验证是None ]。
    ...       具体代码请参考atBasicLibrary/basic.py的 [../library/basic.py.doc.html#At%20Should%20Be%20None| at_should_be_none]方法。
    [Arguments]              ${obj}   ${message}=${None}
    at should be none        ${obj}   ${message}

验证不是None
    [Documentation]  唯一一个参数[obj],如果不是None,什么都不发生。如果是None，报错。
    ...       英文关键字[ ../keywords/basic.doc.html#Should%20not%20be%20none | Should not be none ]。
    ...       具体代码请参考atBasicLibrary/basic.py的 [../library/basic.py.doc.html#Assert%20Obj%20Is%20Not%20None | at_should_not_be_none]方法。
    [Arguments]              ${obj}   ${message}=${None}
    at should not be none    ${obj}   ${message}

Should not be none
    [Documentation]  唯一一个参数[obj],如果不是None,什么都不发生。如果是None，报错。
    ...       中文关键字[ ../keywords/basic.doc.html#验证不是None| 验证不是None ]。
    ...       具体代码请参考atBasicLibrary/basic.py的 [../library/basic.py.doc.html#Assert%20Obj%20Is%20Not%20None | at_should_not_be_none]方法。
    [Arguments]               ${obj}   ${message}=${None}
    at should not be none     ${obj}   ${message}