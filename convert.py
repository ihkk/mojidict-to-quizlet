import pdfplumber
import re

file_path = ""
words = []

if not file_path:
    file_path = input("Enter your pdf path: ").strip('"')

with pdfplumber.open(file_path) as pdf:
    pg_cnt = 0
    for page in pdf.pages:
        pg_cnt += 1
        lines = page.extract_text()
        if pg_cnt == 1:
            lines = lines.split('\n')[3:-1]
        else:
            lines = lines.split('\n')[1:-1]
        # 清理错误行
        for line in lines:
            if line[0] == "|": lines.remove(line)
        # 添加字典对
        for i in range(0, len(lines), 2):
            # 从列表中获取当前两项
            pair = [lines[i], lines[i + 1]]
            # 将这对项添加到字典中
            words.append(pair)
print(f"Wordlist Count: {len(words)}\n")

if input("Reverse list? (y/n) (n for default): ") == "y":
    words.reverse()

print("\n")

for word in words:
    # 重组单词和假名
    word[0] = word[0].replace("undefined", "")
    word[0] = re.sub(" [◎①②③④⑤⑥⑦⑧⑨]*", "", word[0])
    word[0] = re.sub(r"(.*?)\|(.*)", r"\1（\2）", word[0])
    # 去除释义里的括号
    word[1] = re.sub(r"（.*）", "", word[1])
    word[1] = re.sub(r"（.*$", "", word[1])
    # 更改注释里的词性符号
    word[1] = word[1].replace("[", "（")
    word[1] = word[1].replace("]", "）")
    print(f"{word[0]}|{word[1]}")

print("\n")
