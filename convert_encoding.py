import codecs

file_path = "daily_learning.py"

# UTF-8 (BOM 제거)로 변환
with codecs.open(file_path, "r", encoding="utf-8-sig") as f:
    content = f.read()

with codecs.open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 파일을 UTF-8 (without BOM)으로 변환 완료!")
