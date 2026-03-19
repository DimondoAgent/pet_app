from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp

class SwipeableCard(MDCard):
    image_source = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_x = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.start_x = touch.x
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.x += touch.dx
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            diff_x = touch.x - self.start_x
            if diff_x > dp(100):
                self.swipe_right()
            elif diff_x < -dp(100):
                self.swipe_left()
            else:
                self.reset_card()
            return True
        return super().on_touch_up(touch)

    def swipe_right(self):
        anim = Animation(x=Window.width + dp(50), opacity=0, duration=0.3)
        anim.bind(on_complete=self._remove_card)
        anim.start(self)

    def swipe_left(self):
        anim = Animation(x=-self.width - dp(50), opacity=0, duration=0.3)
        anim.bind(on_complete=self._remove_card)
        anim.start(self)

    def reset_card(self):
        anim = Animation(center_x=self.parent.center_x, duration=0.2)
        anim.bind(on_complete=self._reset_opacity)
        anim.start(self)

    def _remove_card(self, *args):
        if self.parent:
            self.parent.remove_widget(self)

    def _reset_opacity(self, *args):
        self.opacity = 1

class MainScreen(MDScreen):
    pass