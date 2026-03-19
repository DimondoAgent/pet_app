from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from firebase.user import get_user_profile  # Исправлено с get_profile

class PetProfileScreen(MDScreen):
    def on_enter(self):
        app = MDApp.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        
        if not user_id:
            print("DEBUG: Пользователь не залогинен, профиль питомца не загружен.")
            return
            
        try:
            data = get_user_profile(user_id)
            if data and 'name_label' in self.ids:
                owner_name = data.get('first_name', 'Хозяин')
                pet_name = data.get('pet_name', 'Без имени')
                self.ids.name_label.text = f"Питомец {owner_name}: {pet_name}"
        except Exception as e:
            print(f"ERROR: Ошибка при загрузке профиля питомца: {e}")