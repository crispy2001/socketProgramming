# socketProgramming

**git repo :** https://github.com/yenchia189929/socketProgramming

## 五子棋遊戲go game
### 介紹
顧名思義我用socket寫了一個五子棋的遊戲：Ｄ
![](https://i.imgur.com/CETQXNq.png)
先連線的是先手（黑子），第二個連線的是白子

### 語言
python3
- 使用套件：
    - pygame(繪製UI)
    - socket

### run
有需要的話可以修改在client和server檔案中的ip和port，此處為了方便demo都適用localhost
```
python3 game_server.py
python3 game_client.py
```
### function介紹
server端
- start_server()
    - 啟用server
- start_client()
    - 去accept兩個player
- start_game()
    - 開始遊戲，判斷是誰下棋去呼叫get_input做receive
- get_input()
    - 從現在下棋的player接收他下哪裡，再把這個位置也傳給另一個人
- check_winner()
    - 確認遊戲是否結束

client端
- start_client()
    - 連線到server
- start_game()
    - draw_a_chessboard()
        - 畫棋盤
    - draw_a_chessman()
        - 如果這是你的turn的話就可以下棋，然後呼叫此function畫黑子白子，若否則向server端請求另一個人下棋的位置再畫
    - end_of_game()
        - 如果確定遊戲結束就呼叫他，會印出"you win!"或"you lose"兩個字樣

---

## FTP
### 介紹
用socket來創造一個簡單的ftp server。支援多個(最多10個)client同時執行此ftp。 
可使用的指令：

### 語言
python3
- 使用套件：
    - socket
    - os(bash基礎指令)
    - _thread(支援多個client同時連線)
    - hashlib(確認檔案雜湊值是相等的)

### 功能指令介紹
- DOWNLOAD : 下載server資料夾的檔案
- UPLOAD : 上傳client端的檔案
- CLIENT + 基礎的terminal指令(ls, cat...): 對本機端的當個資料夾操作
- SERVER + 基礎的terminal指令(ls, cat...): 對server端資料夾做操作
- 若輸入非以上的指令，則輸出invalid input
 
### run
有需要的話可以修改在client和server檔案中的ip和port，此處為了方便demo都適用localhost
```
python3 server.py
python3 client.py
```








<!-- 
# 五子棋go game


## 寫的過程中遇到的error

### thread 
***import 問題***
use `import _thread` instead of `import thread` in python3

***tuple***
https://stackoverflow.com/questions/6474509/thread-module-question/6474552
error msg: 
```
_thread.start_new_thread(clientThread, (conn)) ....
TypeError: 2nd arg ust be a tuple
```
- tuple寫法是要(a, b, ....)，如果以只有一個參數(conn)，我依舊要寫成(conn,)才會過
 -->

<!-- 
### 
## reference
https://shengyu7697.github.io/python-tcp-socket/
https://shengyu7697.github.io/python-socketserver/
https://www.796t.com/article.php?id=10143
[五子棋](https://www.itread01.com/content/1541644693.html)

 -->

