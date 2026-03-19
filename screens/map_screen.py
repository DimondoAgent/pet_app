from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapMarker
from kivy.clock import Clock

class MapScreen(Screen):
    def on_enter(self, *args):
        print("DEBUG: Открыта карта")
        # Здесь в будущем будет запуск слушателя Firebase для получения координат
        
    def update_walker_location(self, lat, lon):
        
        if 'walker_marker' in self.ids:
            self.ids.walker_marker.lat = lat
            self.ids.walker_marker.lon = lon