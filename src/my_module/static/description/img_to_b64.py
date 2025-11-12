import base64


with open('tom.jpeg', 'rb') as img:
    print(base64.b64encode(img.read()).decode())
