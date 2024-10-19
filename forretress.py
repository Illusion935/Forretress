import random
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class ForretressApp(App):
    def build(self):
        self.total_heads = 0
        self.total_damage = 0
        self.spin_count = 0
        self.flipping = False  # Flag to prevent multiple flips

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Set the background color to white
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # RGBA for white
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        # Update the rectangle size and position when the layout is resized
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Display the Forretress card image
        self.card_image = Image(source='forretress.jpg', size_hint=(1, 0.4))
        layout.add_widget(self.card_image)

        # Label to display the spin results
        self.result_label = Label(text='', font_size='20sp', size_hint=(1, 0.2), color=(0, 0, 0, 1))
        layout.add_widget(self.result_label)

        # Spin button
        self.spin_button = Button(text='Spin the Coin', size_hint=(1, 0.1))
        self.spin_button.bind(on_press=self.spin_coin)
        layout.add_widget(self.spin_button)

        # Reset button
        self.reset_button = Button(text='Reset', size_hint=(1, 0.1))
        self.reset_button.bind(on_press=self.reset_game)
        layout.add_widget(self.reset_button)

        # Load coin images
        self.coin_heads_image = 'coin_heads.jpg'
        self.coin_tails_image = 'coin_tails.jpg'
        self.coin_image = Image(source=self.coin_heads_image, size_hint=(1, 0.5))
        layout.add_widget(self.coin_image)

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def spin_coin(self, instance):
        # Prevent spinning if already flipping
        if self.flipping:
            return

        self.flipping = True  # Set the flag to indicate flipping
        self.spin_count += 1  # Increment spin count

        # Start the coin flip animation
        self.animate_coin_flip()

    def animate_coin_flip(self):
        # Define how many flips and the delay between each flip
        flips = 10
        delay = 0.1
        for i in range(flips):
            # Schedule each flip image change
            Clock.schedule_once(self.flip_coin, i * delay)

        # Schedule the final result display after all flips
        Clock.schedule_once(self.show_result, flips * delay)

    def flip_coin(self, dt):
        # Switch between heads and tails images
        if self.coin_image.source == self.coin_heads_image:
            self.coin_image.source = self.coin_tails_image
        else:
            self.coin_image.source = self.coin_heads_image

    def show_result(self, dt):
        # Randomly choose heads or tails
        result = random.choice(['heads', 'tails'])
        self.coin_image.source = self.coin_heads_image if result == 'heads' else self.coin_tails_image
        self.coin_image.reload()  # Reload image to update display
        
        # Show the spin result without updating totals
        self.result_label.text += f'Spin {self.spin_count}: {result.capitalize()}!\n'

        if result == 'heads':
            # Update totals only if the result is heads
            self.total_heads += 1
            self.total_damage += 50
        else:
            # Disable the spin button on tails
            self.spin_button.disabled = True
            
            # Display totals only if the result is tails
            self.result_label.text += f'Total Heads: {self.total_heads}\n'
            self.result_label.text += f'Total Damage: {self.total_damage} damage\n'

        # Reset flipping flag
        self.flipping = False

    def reset_game(self, instance):
        # Reset the game state
        self.total_heads = 0
        self.total_damage = 0
        self.spin_count = 0
        self.result_label.text = ''  # Clear the results
        self.coin_image.source = self.coin_heads_image  # Reset the coin image
        self.coin_image.reload()  # Reload the heads image
        self.flipping = False  # Reset flipping flag
        self.spin_button.disabled = False  # Re-enable the spin button

if __name__ == '__main__':
    ForretressApp().run()