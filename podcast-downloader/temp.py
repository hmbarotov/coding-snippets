import os

string = "Django 6.0 - Natalia Bidart"
extension = ".mp3"

filename = "".join(c for c in string if c.isalnum() or c in " -_.#&").strip()
filename = f"{filename}{extension}"

print(filename)
print(os.path.splitext(filename))
