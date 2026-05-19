import webview
from flask import Flask, render_template
from pathlib import Path
from enums.TemplatesNames import TemplatesNames
from enums.WindowProperties import WindowProperties

TEMPLATE_FOLDER_PATH = Path('gui') / 'templates'
STATIC_FOLDER_PATH = Path('gui') / 'static'

app = Flask(
  __name__, 
  template_folder=TEMPLATE_FOLDER_PATH,
  static_folder=STATIC_FOLDER_PATH
  )

# testing logs for 
logi_baza = {
  "1": {"ip": "192.168.1.1", "data": "2019-01-22", "status": 200, "metoda": "GET", "uri": "/index.html"},
  "2": {"ip": "10.0.0.5", "data": "2019-01-22", "status": 404, "metoda": "POST", "uri": "/login.php"},
}

# main view
@app.route("/")
def home():
  # Przekazujemy listę logów do szablonu HTML
  return render_template(TemplatesNames.INDEX.value , logi=logi_baza)

@app.route("/detail/<log_id>")
def show_details(log_id):
  pojedynczy_log = logi_baza.get(log_id)
  return render_template(TemplatesNames.DETAILS.value, log=pojedynczy_log)

if __name__ == '__main__':
  webview.create_window(
    WindowProperties.NAME.value, 
    app,        
    width=WindowProperties.WIDTH.value,
    height=WindowProperties.HEIGHT.value,
    resizable=WindowProperties.RESIZABLE.value,
    min_size=WindowProperties.MIN_SIZE.value
    )
  webview.start()