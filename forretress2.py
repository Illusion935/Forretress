import tkinter as tk
from PIL import Image, ImageTk
import random

# Create the main window (root)
root = tk.Tk()
root.title("Forretress - Continuous Spin Attack")
root.configure(bg="white")  # Set background to white

# Function for spinning the coin (manual spins with animation)
def spin_once():
    global heads_count, total_damage

    # Start the flip animation
    flip_animation(0)  # Start at the first flip

def flip_animation(step):
    # Display the flipping animation for a short time
    flip_sequence = [coin_heads_photo, coin_tails_photo]  # Alternating heads and tails for the animation
    flip_widths = [100, 80, 60, 40, 20, 40, 60, 80, 100]  # Simulating 3D effect with varying widths

    # 3D flip effect by resizing the image
    if step < len(flip_widths):
        current_width = flip_widths[step]
        resized_img = coin_heads_img.resize((current_width, 100))  # Change the width
        coin_resized = ImageTk.PhotoImage(resized_img)

        # Update the coin label with the resized image
        coin_label.config(image=coin_resized)
        coin_label.image = coin_resized  # Keep a reference to avoid garbage collection

        # Schedule the next frame of the animation
        root.after(50, flip_animation, step + 1)  # Increase the step

    else:
        # After the animation, show the result and update the game
        show_result()

def show_result():
    global heads_count, total_damage

    # Determine the result of the flip
    spin_result = random.choice([True, False])  # True for heads, False for tails

    if spin_result:
        heads_count += 1
        total_damage += 50
        result_str = f"Spin {heads_count}: Heads!"
        coin_label.config(image=coin_heads_photo)  # Display heads
    else:
        result_str = f"Spin {heads_count + 1}: Tails! Spin ended.\nTotal Heads: {heads_count}\nTotal Damage: {total_damage} damage"
        spin_button.config(state="disabled")  # Disable button when a tails is spun
        coin_label.config(image=coin_tails_photo)  # Display tails

    result_label.config(text=result_label.cget("text") + "\n" + result_str)

# Function to reset the game
def reset_game():
    global heads_count, total_damage
    heads_count = 0
    total_damage = 0
    result_label.config(text="")
    spin_button.config(state="normal")  # Re-enable button for new spins
    coin_label.config(image="")  # Clear coin image

# Load and resize the Forretress card image
image_path = "forretress.jpg"
img = Image.open(image_path)
img = img.resize((500, 700))  # Resize the card image
photo = ImageTk.PhotoImage(img)

# Load coin images (these should be loaded **after** the root window is created)
coin_heads_img = Image.open("coin_heads.jpg").resize((100, 100))  # Adjust coin size as needed
coin_tails_img = Image.open("coin_tails.jpg").resize((100, 100))

# Convert to Tkinter-compatible images
coin_heads_photo = ImageTk.PhotoImage(coin_heads_img)
coin_tails_photo = ImageTk.PhotoImage(coin_tails_img)

# Create and place a label for the card image
label = tk.Label(root, image=photo, bg="white")
label.pack(pady=10)

# Create a label for displaying the coin flip result
coin_label = tk.Label(root, image="", bg="white")
coin_label.pack(pady=10)

# Create a spin button
spin_button = tk.Button(root, text="Spin Coin", command=spin_once, bg="white")
spin_button.pack(pady=10)

# Create a label to display the spin results
result_label = tk.Label(root, text="", justify="left", font=("Helvetica", 12), bg="white")
result_label.pack(pady=10)

# Create a reset button
reset_button = tk.Button(root, text="Reset Game", command=reset_game, bg="white")
reset_button.pack(pady=10)

# Initialize variables to track heads and damage
heads_count = 0
total_damage = 0

# Start the GUI loop
root.mainloop()