from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager


from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.main_screen import MainScreen

class PetApp(MDApp):
    current_user_id = None  # Сюда пишем ID
    id_token = None

    def build(self):
        self.title = "Pet App"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        # Загружаем файлы разметки (убедись, что все файлы есть в папке kv)
        Builder.load_file("kv/register_screen.kv")
        Builder.load_file("kv/login_screen.kv")
        Builder.load_file("kv/main_screen.kv")
        Builder.load_file("kv/settings_screen.kv")
        Builder.load_file("kv/map_screen.kv")
        Builder.load_file("kv/chat_screen.kv")

        # Инициализируем ScreenManager
        self.sm = ScreenManager()
        
        # Регистрируем все экраны
        self.sm.add_widget(LoginScreen(name="login_screen"))
        self.sm.add_widget(RegisterScreen(name="register_screen"))
        self.sm.add_widget(MainScreen(name="main_screen"))
       
        return self.sm

    def change_screen(self, screen_name, direction='left'):
        if self.sm:
            self.sm.transition.direction = direction
            self.sm.current = screen_name
        else:
            print("Error: ScreenManager not initialized.")

    def set_user(self, user_id, token):
        self.current_user_id = user_id
        self.id_token = token
        print(f"AUTH: Пользователь {user_id} успешно авторизован.")

if __name__ == '__main__':
    PetApp().run()