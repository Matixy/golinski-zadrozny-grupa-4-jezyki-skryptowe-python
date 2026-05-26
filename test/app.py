import sys
import datetime
from dataclasses import dataclass
from typing import List, Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QPushButton, QLineEdit, QSpinBox, 
    QDateTimeEdit, QGroupBox, QFormLayout, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QDateTime

# =====================================================================
# CZĘŚĆ 1: LOGIKA APLIKACJI (Oparta na Twoim kodzie)
# =====================================================================

@dataclass
class LogEntry:
    raw_line: str  # Surowa linia do wyświetlania na liście (Master)
    timestamp: datetime.datetime
    uid: str
    orig_h: str
    orig_p: int
    resp_h: str
    resp_p: int
    method: str
    host: str
    uri: str
    status_code: int

class LogModel:
    def __init__(self):
        self.all_logs: List[LogEntry] = []
        self.filtered_logs: List[LogEntry] = []

    def load_logs(self, filepath: str) -> bool:
        """Twój kod read_log zmodyfikowany do czytania z pliku"""
        self.all_logs.clear()
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    cleaned_line = line.strip()

                    if cleaned_line == "":
                        continue

                    list_from_line = cleaned_line.split("\t")

                    if len(list_from_line) != 27:
                        continue

                    try:
                        # Twoja konwersja typów
                        ts = datetime.datetime.fromtimestamp(float(list_from_line[0]))
                        uid = list_from_line[1]
                        orig_h = list_from_line[2]
                        orig_p = int(list_from_line[3])
                        resp_h = list_from_line[4]
                        resp_p = int(list_from_line[5])
                        method = list_from_line[7]
                        host = list_from_line[8]
                        uri = list_from_line[9]
                        status_code = int(list_from_line[14])

                        # Pakowanie do obiektu LogEntry zamiast krotki
                        entry = LogEntry(
                            raw_line=cleaned_line,
                            timestamp=ts, uid=uid, orig_h=orig_h, orig_p=orig_p,
                            resp_h=resp_h, resp_p=resp_p, method=method, 
                            host=host, uri=uri, status_code=status_code
                        )
                        self.all_logs.append(entry)

                    except (ValueError, IndexError):
                        continue
                        
            self.filtered_logs = self.all_logs.copy()
            return True
            
        except Exception as e:
            print(f"Błąd otwarcia pliku: {e}")
            return False

    def filter_logs(self, start: datetime.datetime, end: datetime.datetime):
        """Twój kod get_entries_in_time_range"""
        self.filtered_logs = []
        for log in self.all_logs:
            ts = log.timestamp
            # Zastosowany Twój warunek: start <= ts < end
            if start <= ts and ts < end:
                self.filtered_logs.append(log)

    def get_log(self, index: int) -> Optional[LogEntry]:
        if 0 <= index < len(self.filtered_logs):
            return self.filtered_logs[index]
        return None

# =====================================================================
# CZĘŚĆ 2: INTERFEJS GRAFICZNY (Zaktualizowany o nowe pola)
# =====================================================================

class MainWindow(QMainWindow):
    def __init__(self, model: LogModel):
        super().__init__()
        self.model = model
        self.setWindowTitle("Przeglądarka Logów HTTP")
        self.resize(1000, 600)
        
        self._init_ui()

    def _init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # --- PANEL MASTER (Lista) ---
        left_panel = QVBoxLayout()
        self.btn_load = QPushButton("Wczytaj plik z logami")
        self.btn_load.clicked.connect(self._load_file)
        left_panel.addWidget(self.btn_load)
        
        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self._on_log_selected)
        left_panel.addWidget(self.list_widget)
        main_layout.addLayout(left_panel, stretch=1)

        # --- PANEL DETAIL (Szczegóły) ---
        right_panel = QVBoxLayout()

        # Filtrowanie
        filter_group = QGroupBox("Filtrowanie po dacie i czasie")
        filter_layout = QFormLayout()
        
        self.dt_start = QDateTimeEdit(QDateTime.currentDateTime())
        self.dt_start.setCalendarPopup(True)
        self.dt_end = QDateTimeEdit(QDateTime.currentDateTime())
        self.dt_end.setCalendarPopup(True)
        
        self.btn_filter = QPushButton("Zastosuj filtr")
        self.btn_filter.clicked.connect(self._apply_filter)
        
        filter_layout.addRow("Od (>=):", self.dt_start)
        filter_layout.addRow("Do (<):", self.dt_end)
        filter_layout.addRow("", self.btn_filter)
        filter_group.setLayout(filter_layout)
        right_panel.addWidget(filter_group)

        # Szczegóły Loga dopasowane do Twoich pól
        detail_group = QGroupBox("Szczegóły wybranego wpisu")
        detail_layout = QFormLayout()
        
        self.val_time = QDateTimeEdit(); self.val_time.setReadOnly(True)
        self.val_uid = QLineEdit(); self.val_uid.setReadOnly(True)
        self.val_client = QLineEdit(); self.val_client.setReadOnly(True)
        self.val_server = QLineEdit(); self.val_server.setReadOnly(True)
        self.val_method = QLineEdit(); self.val_method.setReadOnly(True)
        self.val_host = QLineEdit(); self.val_host.setReadOnly(True)
        self.val_uri = QLineEdit(); self.val_uri.setReadOnly(True)
        
        self.val_status = QSpinBox()
        self.val_status.setReadOnly(True)
        self.val_status.setMaximum(999)
        
        detail_layout.addRow("Data i czas (ts):", self.val_time)
        detail_layout.addRow("UID sesji:", self.val_uid)
        detail_layout.addRow("Klient (orig_h:orig_p):", self.val_client)
        detail_layout.addRow("Serwer (resp_h:resp_p):", self.val_server)
        detail_layout.addRow("Metoda HTTP:", self.val_method)
        detail_layout.addRow("Host docelowy:", self.val_host)
        detail_layout.addRow("Ścieżka URI:", self.val_uri)
        detail_layout.addRow("Kod statusu:", self.val_status)
        
        detail_group.setLayout(detail_layout)
        right_panel.addWidget(detail_group)

        # Nawigacja
        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton("<< Poprzedni")
        self.btn_next = QPushButton("Następny >>")
        self.btn_prev.clicked.connect(self._go_prev)
        self.btn_next.clicked.connect(self._go_next)
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_next)
        right_panel.addLayout(nav_layout)

        main_layout.addLayout(right_panel, stretch=2)
        self._update_nav_buttons()

    # --- ZDARZENIA ---
    def _load_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Wybierz plik logów")
        if filepath:
            if self.model.load_logs(filepath):
                self._populate_list()
                self._setup_filter_dates()
            else:
                QMessageBox.critical(self, "Błąd", "Nie udało się wczytać pliku.")

    def _populate_list(self):
        self.list_widget.clear()
        for log in self.model.filtered_logs:
            # Ucinanie do 30 znaków zgodnie z zadaniem
            display = log.raw_line[:30] + "..." if len(log.raw_line) > 30 else log.raw_line
            self.list_widget.addItem(display)
            
        if self.model.filtered_logs:
            self.list_widget.setCurrentRow(0)

    def _setup_filter_dates(self):
        if self.model.all_logs:
            timestamps = [log.timestamp for log in self.model.all_logs]
            self.dt_start.setDateTime(self._py_datetime_to_qdt(min(timestamps)))
            # Dodajemy 1 sekundę do maksa, żeby zmieścił się w Twoim warunku '< end'
            max_dt = max(timestamps) + datetime.timedelta(seconds=1)
            self.dt_end.setDateTime(self._py_datetime_to_qdt(max_dt))

    def _apply_filter(self):
        start = self.dt_start.dateTime().toPyDateTime()
        end = self.dt_end.dateTime().toPyDateTime()
        self.model.filter_logs(start, end)
        self._populate_list()
        self._update_nav_buttons()

    def _on_log_selected(self, index: int):
        log = self.model.get_log(index)
        if log:
            self.val_time.setDateTime(self._py_datetime_to_qdt(log.timestamp))
            self.val_uid.setText(log.uid)
            self.val_client.setText(f"{log.orig_h} : {log.orig_p}")
            self.val_server.setText(f"{log.resp_h} : {log.resp_p}")
            self.val_method.setText(log.method)
            self.val_host.setText(log.host)
            self.val_uri.setText(log.uri)
            self.val_status.setValue(log.status_code)
        else:
            self.val_uid.clear()
            self.val_client.clear()
            self.val_server.clear()
            self.val_method.clear()
            self.val_host.clear()
            self.val_uri.clear()
            self.val_status.setValue(0)
            
        self._update_nav_buttons()

    def _go_prev(self):
        c = self.list_widget.currentRow()
        if c > 0: self.list_widget.setCurrentRow(c - 1)

    def _go_next(self):
        c = self.list_widget.currentRow()
        if c < self.list_widget.count() - 1: self.list_widget.setCurrentRow(c + 1)

    def _update_nav_buttons(self):
        c = self.list_widget.currentRow()
        t = self.list_widget.count()
        self.btn_prev.setEnabled(c > 0)
        self.btn_next.setEnabled(c < t - 1 and c != -1)

    @staticmethod
    def _py_datetime_to_qdt(dt: datetime.datetime) -> QDateTime:
        return QDateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(LogModel())
    window.show()
    sys.exit(app.exec_())