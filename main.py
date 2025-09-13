from gui.gui import ApplicationGUI

def main():
    app = ApplicationGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()
