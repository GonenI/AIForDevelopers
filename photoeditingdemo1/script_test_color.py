from photoedit.ui.main_window import MainWindow
w = MainWindow()
# simulate color set
w._set_color('#112233')
print('brush_color:', w._brush_color)
print('paint panel color var:', getattr(w._paint_panel, '_color').get())
# cleanup
w.destroy()
