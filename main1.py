"""

Resizer app from 'Acheive Goal' Team
 This is a image resizer app made with kivymd
 
 D1 : crop the icon background
 D5 : change icon in buildozer

"""
# from sys import path
import PIL
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.utils import platform
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from PIL import Image
import os
import random


class Resizer(MDApp):
    # new chooser
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            # preview=True
        )

    def file_manager_open(self, *args):
        path = '.'
        self.file.text = str(path)
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            app_folder = os.path.dirname(os.path.abspath(__file__))
            path = "/storage/emulated/0/"  # app_folder
            self.file.text = str(path)

        self.file_manager.show(path)  # output manager to the screen
        toast(path)
        self.manager_open = True

    def select_path(self, path):
        """It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        """

        self.exit_manager()
        self.input1.text = path
        toast(path)

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        """Called when buttons are pressed on the mobile device."""

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    # OPEN FILE BUTTON
    def open_file(self, *args):
        """ called when open file clicked"""
        location = self.file.text
        self.file_manager.show(location)  # output manager to the screen
        self.manager_open = True

    # RESIZE FUNCTION
    def Resize(self, *args):  # RESIZING THE IMAGE
        try:

            width = int(self.input3.text)
            height = int(self.input4.text)

            img_size_input = self.input2.text == 'Eg: 40' or ''
            if not img_size_input:
                img_size = int(self.input2.text) * 1024
            in_image = self.input1.text
            img = Image.open(in_image)  # image extension *.png,*.jpg
            compare = False

            while not compare:
                new_width = width
                new_height = height
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
                rand = random.randint(10, 1000)
                out_image = str(rand) + 'resizedimage.png'
                img.save(out_image)  # format may what you want *.png, *jpg, *.gif
                resize_img = os.stat(out_image).st_size
                save_location = os.path.abspath(out_image)
                if platform == "android":
                    os.replace(str(save_location), self.file.text + '/Pictures' + '/' + out_image)
                else:
                    os.replace(str(save_location), self.file.text + "\\" + out_image)
                toast(save_location)

                if not img_size_input:
                    compare = img_size >= resize_img
                    if compare:
                        self.msg.text = "IMAGE RESIZED SUCCESSFULLY"
                        break
                    else:
                        os.remove(out_image)
                        width = int(width * 0.9)
                        height = int(height * 0.9)
                        compare = False
                        if width <= 0:
                            break
                else:
                    self.msg.text = "IMAGE RESIZED SUCCESSFULLY"
                    break

        # manage error
        except ValueError:
            self.msg.text = "Please Adjust Your Width"
        except FileNotFoundError:
            self.msg.text = "Select Image File"
        except PIL.UnidentifiedImageError:
            self.msg.text = "Select Image File"
        except PermissionError:
            self.msg.text = "Select Image File"
            # RESIZE FUNCTION

    # reset function
    def reset(self, *args):
        self.input1.text = "File Path"
        self.input2.text = "Eg: 40"
        self.input3.text = "* Width"
        self.input4.text = "* Height"
        self.msg.text = ''

    def build(self):
        # INITIALIZE SCREEN
        screen = MDScreen()
        self.icon = 'LOGO.png'
        self.theme_cls.theme_style = "Dark"
        self.toolbar = MDTopAppBar(title="IMAGE RESIZER")
        self.theme_cls.primary_palette = "LightGreen"
        self.theme_cls.primary_hue = "A700"

        # TOP TOOLBAR
        # left_action_items: [['menu', lambda x: None]]
        self.toolbar.left_action_items = [['menu', lambda x: None]]
        self.toolbar.pos_hint = {"top": 1}
        screen.add_widget(self.toolbar)

        # STUDY TIME
        self.label = MDLabel(
            text="UPLOAD FILE",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            theme_text_color="Secondary"
        )
        screen.add_widget(self.label)

        # FILENAME FIELD
        self.input1 = MDTextField(
            text="File Path",
            halign="center",
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            font_size=18
        )
        screen.add_widget(self.input1)

        # SIZE TEXT
        self.label = MDLabel(
            text="SIZE",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            theme_text_color="Secondary"
        )

        # KB TEXT
        self.label1 = MDLabel(
            text="Kb",
            halign="center",
            pos_hint={"center_x": 0.6, "center_y": 0.4},
            theme_text_color="Secondary"
        )
        # width TEXT
        self.label2 = MDLabel(
            text="px",
            halign="center",
            pos_hint={"center_x": 0.45, "center_y": 0.5},
            theme_text_color="Secondary"
        )
        # height TEXT
        self.label3 = MDLabel(
            text="px",
            halign="center",
            pos_hint={"center_x": 0.75, "center_y": 0.5},
            theme_text_color="Secondary"
        )
        # SIZE FIELD
        self.input2 = MDTextField(
            text="Eg: 40",
            halign="center",
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            font_size=18
        )

        # WIDTH FIELD
        self.input3 = MDTextField(
            text="* Width",
            halign="center",
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.35, "center_y": 0.5},
            font_size=18
        )

        # HEIGHT FIELD
        self.input4 = MDTextField(
            text="* Height",
            halign="center",
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.65, "center_y": 0.5},
            font_size=18
        )

        # open file invisible field
        self.file = MDTextField(
            text=".",
            halign="center",
            size_hint=(0.3, 1),
            pos_hint={"center_x": 0.2, "center_y": 0.4},
            font_size=18
        )

        screen.add_widget(self.label)
        screen.add_widget(self.label1)
        screen.add_widget(self.label2)
        screen.add_widget(self.label3)
        screen.add_widget(self.input2)
        screen.add_widget(self.input3)
        screen.add_widget(self.input4)

        # file choose button
        screen.add_widget(MDFillRoundFlatButton(
            text="UPLOAD",
            font_size=17,
            pos_hint={"center_x": 0.7, "center_y": 0.7},
            on_press=self.file_manager_open

        ))

        # RESIZE BUTTON
        screen.add_widget(MDFillRoundFlatButton(
            text="RESIZE",
            font_size=17,
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            on_press=self.Resize

        ))

        # OPEN FILE BUTTON
        screen.add_widget(MDFillRoundFlatButton(
            text="Open File",
            font_size=17,
            pos_hint={"center_x": 0.3, "center_y": 0.3},
            on_press=self.open_file

        ))

        # RESET BUTTON
        screen.add_widget(MDFillRoundFlatButton(
            text="RESET",
            font_size=17,
            pos_hint={"center_x": 0.7, "center_y": 0.3},
            on_press=self.reset
        ))

        # MESSAGETEXT
        self.msg = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            theme_text_color="Secondary",
            font_style="H5"

        )

        screen.add_widget(self.msg)

        # note text
        self.note = MDLabel(
            text="--Note: size in kb is optional--",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            theme_text_color="Secondary",
            # font_style="H6"
            font_size=20

        )

        # Achieve goal text
        self.name1 = MDLabel(
            text="Achieve Goal",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.05},
            theme_text_color="Secondary",
            font_style="H5"
        )
        screen.add_widget(self.name1)
        screen.add_widget(self.note)

        return screen


if __name__ == '__main__':
    Resizer().run()
