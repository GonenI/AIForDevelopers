import sys
sys.path.insert(0, r'C:\Gonen\Teaching\ai\aipython2024\photoeditingdemo1')
import photoedit.ui.main_window as mw
import photoedit.ui.ocr_ui as ou
print('Imported OK', hasattr(mw, 'MainWindow'), hasattr(ou, 'is_ocr_available'))
