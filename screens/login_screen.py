from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from firebase.auth import login_user

class LoginScreen(MDScreen):

    def do_login(self):
        print("DEBUG: Попытка входа...")
        
        email = self.ids.email_field.text.strip()
        password = self.ids.password_field.text.strip()
        
        if not email or not password:
            Snackbar(text="Заполните почту и пароль!").open()
            return

        result = login_user(email, password)

        if isinstance(result, dict) and "idToken" in result:
            app = MDApp.get_running_app()
            
            # Безопасно сохраняем данные в главный класс приложения
            if hasattr(app, 'set_user'):
                app.set_user(result["localId"], result["idToken"])
            else:
                app.current_user_id = result["localId"]
                app.id_token = result["idToken"] 
            
            print(f"Успешный вход! ID: {result['localId']}")
            
            self.manager.current = "main_screen"
        else:
            error_msg = "Ошибка входа"
            if isinstance(result, dict):
                error_msg = result.get("error", {}).get("message", "Неверный логин или пароль")
            
            print(f"ERROR: {error_msg}")
            Snackbar(text=f"Ошибка: {error_msg}").open()

    def go_to_register(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "register_screen"