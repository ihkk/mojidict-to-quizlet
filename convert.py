import pdfplumber
import re
import pyperclip


def isKana(char):
    # \x00-\xff为半角字符，\x00-\xff全角字符，\u3000-\303F为符号，\u3040-\u309F为平假名，\u30a0-\u30ff为片假名，\uff00-\uffef为字符
    kana_c = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')
    if kana_c.search(char):
        return True
    else:
        return False


def same_kana(str1, str2):
    """
    This function takes two strings as input and checks if str1 is the hiragana present of str2.
    """
    if len(str1) != len(str2):
        return False
    for char in str1:
        if not isKana(char):
            return False
    for char in str2:
        if not isKana(char):
            return False
    return True


def main():
    file_path = ""
    words = []
    delete_duplicate_kana = False

    if not file_path:
        file_path = input("Enter your pdf path: ").strip('"')

    with pdfplumber.open(file_path) as pdf:
        pg_cnt = 0
        for page in pdf.pages:
            pg_cnt += 1
            lines = page.extract_text()
            if pg_cnt == 1:
                # 如果第三行不含"[]"，则删除4行
                if not re.search(r"\|", lines.split('\n')[3]):
                    lines = lines.split('\n')[4:-1]
                else:
                    lines = lines.split('\n')[3:-1]
            else:
                lines = lines.split('\n')[1:-1]
            # 清理错误行
            for line in lines:
                if line[0] == "|":
                    lines.remove(line)
            # 添加字典对
            for i in range(0, len(lines), 2):
                # 从列表中获取当前两项
                pair = [lines[i], lines[i + 1]]
                # 将这对项添加到字典中
                words.append(pair)
    print(f"Wordlist Count: {len(words)}\n")

    if input("Reverse list? (y/n) (n for default): ") == "y":
        words.reverse()

    delete_duplicate_kana = True
    if input("Delete duplicate kana? (y/n) (y for default): ") == "n":
        delete_duplicate_kana = False

    print("\n")

    for word in words:
        # 重组单词和假名
        word[0] = word[0].replace("undefined", "")
        word[0] = re.sub(" [◎①②③④⑤⑥⑦⑧⑨]*", "", word[0])
        kanji_kana_pair = re.findall(r"(.*?)\|(.*)", word[0])
        if kanji_kana_pair and delete_duplicate_kana:
            kanji, kana = kanji_kana_pair[0]
            if kanji == kana or same_kana(kanji, kana):
                word[0] = kanji
        word[0] = re.sub(r"(.*?)\|(.*)", r"\1（\2）", word[0])
        # 去除释义里的括号
        word[1] = re.sub(r"（.*）", "", word[1])
        word[1] = re.sub(r"（.*$", "", word[1])
        # 更改注释里的词性符号
        word[1] = word[1].replace("[", "（")
        word[1] = word[1].replace("]", "）")
        print(f"{word[0]}|{word[1]}")

    print("\n")
    
    # 复制wordlist到剪贴板
    pyperclip.copy("\n".join([f"{word[0]}|{word[1]}" for word in words]))
    print("Copied to clipboard.")


if __name__ == '__main__':
    main()
