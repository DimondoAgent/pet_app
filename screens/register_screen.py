from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from firebase.auth import register_user
from firebase.user import save_user_profile

class RegisterScreen(MDScreen):
    def do_register(self):
        email = self.ids.email_field.text.strip()
        password = self.ids.password_field.text.strip()
        user_name = self.ids.name_field.text.strip()
        pet_name = self.ids.pet_name_field.text.strip()

        if not all([email, password, user_name]):
            Snackbar(text="Заполните хотя бы почту, пароль и имя!").open()
            return

        # 1. Регистрация в Firebase Auth
        result = register_user(email, password)

        if isinstance(result, dict) and "idToken" in result:
            user_id = result["localId"]
            id_token = result["idToken"]
            
            # 2. Подготавливаем данные для базы
            profile_data = {
                "first_name": user_name,
                "pet_name": pet_name,
                "email": email
            }

            try:
                # 3. Сохраняем в Realtime Database
                save_user_profile(user_id, profile_data)
                
                # 4. Авторизуем в приложении
                app = MDApp.get_running_app()
                if hasattr(app, 'set_user'):
                    app.set_user(user_id, id_token)
                else:
                    app.current_user_id = user_id
                    app.id_token = id_token
                
                Snackbar(text="Аккаунт создан и профиль заполнен!").open()
                self.manager.current = "main_screen"
            except Exception as e:
                print(f"ERROR при сохранении БД: {e}")
                Snackbar(text="Аккаунт создан, но данные профиля не сохранились.").open()
        else:
            if isinstance(result, dict):
                error_msg = result.get("error", {}).get("message", "Ошибка регистрации")
            else:
                error_msg = "Ошибка регистрации"
            Snackbar(text=f"Ошибка: {error_msg}").open()