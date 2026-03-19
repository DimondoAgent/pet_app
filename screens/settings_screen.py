from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from firebase.user import save_user_profile, get_user_profile
from kivymd.uix.snackbar import Snackbar

class SettingsScreen(MDScreen):
    
    def on_enter(self, *args):
        print("DEBUG: Зашли на экран настроек, запускаю загрузку...")
        self.load_profile_firebase()

    def load_profile_firebase(self):
        app = MDApp.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        id_token = getattr(app, 'id_token', None)

        if not user_id:
            print("DEBUG: Юзер не залогинен. Загрузка отменена.")
            return

        try:
            from firebase.user import get_user_profile
            data = get_user_profile(user_id, id_token)

            print(f"DEBUG: Ответ от Firebase: {data}") # Если тут None, значит в БД пусто
            
            if data:
                self.ids.name_input.text = str(data.get('first_name', ''))
                self.ids.email_input.text = str(data.get('email', ''))
                self.ids.pet_name_input.text = str(data.get('pet_name', ''))
                print("DEBUG: Поля заполнены!")
            else:
                print("DEBUG: В базе пока нет данных для этого ID.")
        except Exception as e:
            print(f"ERROR загрузки: {e}")

    def save_profile_firebase(self):
        app = MDApp.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        id_token = getattr(app, 'id_token', None)

        if not user_id or not id_token:
            Snackbar(text="Ошибка: Нет авторизации").open()
            return

        data = {
            'first_name': self.ids.name_input.text.strip() if 'name_input' in self.ids else "",
            'email': self.ids.email_input.text.strip() if 'email_input' in self.ids else "",
            'pet_name': self.ids.pet_name_input.text.strip() if 'pet_name_input' in self.ids else ""
        }

        try:
            # ВАЖНО: передаем только 1 аргумент (без id_token)
            save_user_profile(user_id, data, id_token)
            Snackbar(text="Профиль успешно сохранен!").open()
        except Exception as e:
            print(f"ERROR при сохранении: {e}")
            Snackbar(text="Ошибка при сохранении профиля").open()