import os
import webview
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from enums.TemplatesNames import TemplatesNames
from enums.WindowProperties import WindowProperties
from log_parser import read_log, filter_logs_by_date
from datetime import datetime

TEMPLATE_FOLDER_PATH = Path('gui') / 'templates'
STATIC_FOLDER_PATH = Path('gui') / 'static'

app = Flask(
  __name__, 
  template_folder=TEMPLATE_FOLDER_PATH,
  static_folder=STATIC_FOLDER_PATH
  )

#Obiekt przechowujacy dane przez caly czas dzialanai programu
class AppState:
  def __init__(self):
    self.all_logs = []  #w tej liscie przechowywane sa wszystkie logi
    self.filtered_logs = [] #w tej sa przechowywane logi do wyswietlania
    self.curr_file_name = "Wybierz plik ..."
    self.LOG_LIST_SIZE = 1000
    self.start_date_str = ""
    self.end_date_str = ""

app_state = AppState()


# main view
@app.route("/")
def home():
  #przekazanie listy logów do szablonu HTML
  return render_template(TemplatesNames.INDEX.value , 
                          logs=app_state.filtered_logs[:app_state.LOG_LIST_SIZE], 
                          start_index=0, next_index=app_state.LOG_LIST_SIZE, 
                          total_count=len(app_state.filtered_logs), 
                          file_name=app_state.curr_file_name, 
                          start_date=app_state.start_date_str,
                          end_date=app_state.end_date_str)



@app.route("/detail/<int:log_id>")
def show_details(log_id):
  selected_log = app_state.filtered_logs[log_id]
  return render_template(TemplatesNames.DETAILS.value, log=selected_log)



@app.route("/read_file", methods=["POST"])
def read_file():
    #sprawdzenie czy plik został w ogóle przesłany (w index.html jest name="plik_logow")
    if "plik_logow" in request.files:
        file = request.files["plik_logow"]
        
        if file.filename != "":
            #tworzenie folderu 'uploads' jeśli nie istnieje i zapisanie pliku tymczasowo
            os.makedirs("uploads", exist_ok=True)
            saving_path = os.path.join("uploads", file.filename)
            file.save(saving_path)
            
            #zapisywanie danych do obiektu, do obu list
            logs = read_log(saving_path)
            app_state.all_logs = logs
            app_state.filtered_logs = logs
            app_state.curr_file_name = file.filename

            if os.path.exists(saving_path):
                os.remove(saving_path)  #usuwanie tymczasowego pliku z dysku
            
    return redirect("/") #przeladowanie strony glownej



@app.route("/filter", methods=["POST"])
def filter_log():
  start_str = request.form.get("date_start") or ""
  end_str = request.form.get("date_end") or ""
  app_state.start_date_str = start_str
  app_state.end_date_str = end_str

  app_state.filtered_logs = filter_logs_by_date(app_state.all_logs, start_str, end_str)

  return redirect("/")



@app.route("/load_more/<int:start_index>")
def load_more(start_index):
   next_index = start_index + app_state.LOG_LIST_SIZE
   next_logs = app_state.filtered_logs[start_index:next_index]

   return render_template(
      TemplatesNames.LOGS_BOX.value,
      logs = next_logs,
      start_index=start_index,
      next_index=next_index,
      total_count=len(app_state.filtered_logs)
   )




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