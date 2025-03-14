"""
docustring
"""
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from pathlib import Path
from Profile import Profile, Post
from ds_messenger import DirectMessenger

SERVER = '127.0.0.1'
PORT = 3001
NAME = 'Kiara'
PASSWORD = '56789'
PATH = 'myjournal.dsu'


class LocalService():
    """
    This class call direct messagenger and sync to local
    """
    def __init__(self, server=None, username=None, password=None):
        self.server = server
        self.username = username
        self.password = password
        self.local = None
        self.airmessage = None
        self.newmessage = None

    def connect(self):
        """
        This function connects to the server
        and synchronizes the current data
        If connection is successful,
        local will download all the server content
        If connection fails, program will use
        the local content
        precondition:
            local must have a file called myjournal.dsu
            This file must have the content
        """
        try:
            p = Path(PATH)
            if not p.exists():
                p.touch()
            my_messenger = DirectMessenger(self.server,
                                           self.username,
                                           self.password)
            self.airmessage = my_messenger.retrieve_all()
            # print(all_messages)
            if self.airmessage is not None:
                self.synch_server(self.airmessage)
        except ConnectionRefusedError as ce:
            print('Server is not running!', str(ce))
        finally:
            local_message = Profile(SERVER, NAME, PASSWORD)
            local_message.load_profile(PATH)
            print('local file loaded!')
            self.local = local_message

    def refresh(self, recipient, msg):
        """
        docustring
        """
        try:
            my_messenger = DirectMessenger(self.server,
                                           self.username,
                                           self.password)
            my_messenger.send(msg, recipient)
            self.newmessage = my_messenger.retrieve_new()
            return self.newmessage
        except ConnectionRefusedError as ce:
            print('Server is not running!',  str(ce))

    def synch_server(self, all_messages):
        """
        docustring
        """
        my_profile = Profile(SERVER, NAME, PASSWORD)
        # temp_post = Post('My Post')
        # my_profile.add_post(temp_post)
        # print(my_profile.get_posts())
        for message in all_messages:
            # if 'from::' in message.recipient:
            #     recipient = message.recipient.split("::")[1]
            #     new_post = Post(entry = message.message,
            #                     friend = recipient,
            #                     type = 'from')
            # else:
            new_post = Post(entry=message.message,
                            friend=message.recipient)
            my_profile.add_post(new_post)
        print('posts', my_profile.get_posts())
        my_profile.save_profile(PATH)

    def create_friend_account(self, friend_name):
        """
        docustring
        """
        DirectMessenger(SERVER, friend_name, PASSWORD)
        # sid_account = DirectMessenger(SERVER, 'sid', '45678')
        # my_messenger.send('Hello Sid!', 'sid')
        # my_messenger.send('Bye Sid!', 'sid')
        # sid_account.send('Hi Kiara', 'Kiara')

    # # create_main_account()
    # connect()


class Body(tk.Frame):
    """
    class
    """
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        """
        docustring
        """
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """
        docustring
        """
        self._contacts.append(contact)
        id1 = len(self._contacts) - 1
        self._insert_contact_tree(id1, contact)

    def _insert_contact_tree(self, id2, contact: str):
        if len(contact) > 25:
            contact = contact[:24] + "..."
        id2 = self.posts_tree.insert('', id2, id2, text=contact)

    def insert_user_message(self, message: str):
        """
        docustring
        """
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        """
        docustring
        """
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def delete_message(self):
        """
        docustring
        """
        self.entry_editor.delete(1.0, tk.END)

    def get_text_entry(self) -> str:
        """
        docustring
        """
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """
        docustring
        """
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    docustring
    """
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """
        docustring
        """
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.bind('<ButtonPress>', lambda event: self.send_click())
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """
    docustring
    """
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols
        # self.password
        self.password = tk.Label(frame, width=30, text='Password')
        self.password.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.server)
        self.password_entry['show'] = '*'
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """
    docustring
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        # self.direct_messenger = continue!
        # After all initialization is complete
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        # self.body.insert_contact("studentexw23")
        # adding one example student.
        # self.body.insert_contact('Sid')
        # self.body.insert_contact('sid')
        self.direct_message = None
        self.local_message = None
        self.service = None

    def send_message(self):
        """
        docustring
        """
        # You must implement this!
        msg = self.body.get_text_entry()
        self.publish(msg)

    def add_contact(self):
        """
        docustring
        """
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        user = simpledialog.askstring('Add contact', 'Please add a contact')
        if user:
            self.body.insert_contact(user)
            # if self.service:
            #     self.service.create_friend_account(user)

    def recipient_selected(self, recipient):
        """
        docustring
        """
        self.recipient = recipient
        self.check_new()

    def configure_server(self):
        """
        docustring
        """
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.
        self.service = LocalService(self.server, self.username, self.password)
        self.service.connect()
        print(type((self.service)))
        print(self.service.airmessage)
        if self.service.airmessage is not None:
            self.direct_message = self.service.airmessage
        else:
            self.local_message = self.service.local

    def publish(self, message: str):
        """
        docustring
        """
        # You must implement this!
        print('in publish', message)
        print(self.server, self.username, self.password)
        # temp = DirectMessenger(self.server, self.username, self.password)
        # temp.send(message, self.recipient)
        # temp.retrieve_new()
        temp = LocalService(self.server, self.username, self.password)
        temp.refresh(self.recipient, message)
        self.check_new()

    def check_new(self):
        """
        docustring
        """
        # You must implement this!
        self.service = LocalService(self.server, self.username, self.password)
        self.service.connect()
        if self.service.airmessage is not None:
            self.direct_message = self.service.airmessage
        else:
            self.local_message = self.service.local
        self.body.delete_message()
        if self.direct_message is not None:
            print('Using server message')
            for item in reversed(self.direct_message):
                if ('from::' in item.recipient
                        and item.recipient[6:] == self.recipient):
                    self.body.insert_contact_message(item.message)
                elif item.recipient == self.recipient:
                    self.body.insert_user_message(item.message)
        elif self.local_message is not None:
            print('Using local message')
            print(self.local_message.get_posts())
            for item in reversed(self.local_message.get_posts()):
                if ('from::' in item['friend']
                        and item['friend'][6:] == self.recipient):
                    self.body.insert_contact_message(item['entry'])
                elif item['friend'] == self.recipient:
                    self.body.insert_user_message(item['entry'])
        else:
            print('ERROR')

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id_ = main.after(2000, app.check_new)
    print(id_)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
