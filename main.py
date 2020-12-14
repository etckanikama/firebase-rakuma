import eel 
import time
import firebasetool
import desktop

# フォルダ名
app_name = "html"
end_point = "index.html"
size = (700,600)

@eel.expose
def login(inp):
    firebasetool.login(inp)
    


desktop.start(app_name,end_point,size)