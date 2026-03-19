from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.metrics import dp

class ChatScreen(Screen):
    def send_message(self):
        msg_text = self.ids.msg_input.text.strip()
        if not msg_text:
            return

        print(f"DEBUG: Отправка сообщения: {msg_text}")
        
        # 1. Добавляем сообщение на экран
        new_msg = Label(
            text=f"Вы: {msg_text}",
            color=(0,0,0,1),
            size_hint_y=None,
            height=dp(40),
            text_size=(None, None),
            halign="right"
        )
        self.ids.chat_history.add_widget(new_msg)
        
        # 2. Очищаем поле ввода
        self.ids.msg_input.text = ""

        # 3. (В будущем) Отправляем msg_text в Firebase Firestore