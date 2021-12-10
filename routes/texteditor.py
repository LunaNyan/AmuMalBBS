import routes.func as func

def reset_screen(title, trk, attention):
    func.screen_clear()
    # show title bar
    print(title)
    print("저장(@S), 줄 수정(@E[줄 번호]), 줄 삭제(@R[줄 번호])")
    if attention != "":
        print(attention)
    print("---------------")
    ln = 1
    if len(trk) >= 1:
        for t in trk:
            print(str(ln) + "\t | " + t)
            ln += 1
    return ln

def trk2str(truck):
    t = ""
    for i in truck:
        t += i + "\n"
    return t[:-2]

def editor(title, text=None):
    # generate text truck
    if text != None:
        trk = text.split("\n")
    else:
        trk = []
    # input
    attention = ""
    while True:
        ln = reset_screen(title, trk, attention)
        i = input(str(ln) + "\t | ")
        # Command parser
        if i == "@S":
            ip = input("저장하시겠습니까? (Y/N) 취소(아무 키) > ")
            if ip == "Y" or ip == "y":
                return trk2str(trk)
            elif ip == "N" or ip == "n":
                return False
            else:
                attention = "저장하지 않고 편집을 계속합니다."
                continue
        elif i.startswith("@E"):
            try:
                eln = int(i.replace("@E", ""))
                if eln <= 0 or eln >= len(trk):
                    attention = "잘못된 줄 번호입니다."
                    continue
                else:
                    print(str(eln) + "\t | " + trk[eln-1])
                    nt = input(str(eln) + "+\t | ")
                    trk[eln-1] = nt
                    attention = ""
                    continue
            except ValueError:
                attention = "@E[줄 번호] 형태로 입력해 주십시오. (예시 : @E1)"
                continue
        elif i.startswith("@R"):
            try:
                eln = int(i.replace("@R", ""))
                if eln <= 0 or eln >= len(trk):
                    attention = "잘못된 줄 번호입니다."
                    continue
                else:
                    del(trk[eln-1])
                    attention = ""
                    continue
            except ValueError:
                attention = "@R[줄 번호] 형태로 입력해 주십시오. (예시 : @R1)"
                continue
        else:
            trk.append(i)
            attention = ""
            continue
