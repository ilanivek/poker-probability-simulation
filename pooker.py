import pied_poker as pp
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

np.random.seed(420)


class PokerSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Simulator")
        
        self.num_players = tk.IntVar(value=2)
        self.your_cards = tk.StringVar()
        self.community_cards = []
        self.players = []  
        self.simulation_result = None  

        self.create_widgets()

    def create_widgets(self):
        # Number of players dropdown
        tk.Label(self.root, text="Number of Players:").grid(row=0, column=0, padx=10, pady=10)
        self.player_count_combo = ttk.Combobox(self.root, textvariable=self.num_players, values=list(range(2, 10)), state='readonly')
        self.player_count_combo.grid(row=0, column=1, padx=10, pady=10)
        self.player_count_combo.current(0)  # Set default value to 2

        # Your cards input
        tk.Label(self.root, text="Your Cards (e.g., 'as, qs'):").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.your_cards).grid(row=1, column=1, padx=10, pady=10)

        # Community cards input
        self.community_cards_var = tk.StringVar()
        tk.Label(self.root, text="Community Cards (e.g., '4s, 4h, 10s'):").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.community_cards_var).grid(row=2, column=1, padx=10, pady=10)

        # Add Community Card Button
        self.add_card_button = tk.Button(self.root, text="Add Community Card", command=self.add_community_card)
        self.add_card_button.grid(row=3, columnspan=2, padx=10, pady=10)

        # Run Simulation Button
        self.simulate_button = tk.Button(self.root, text="Compute Winning Probabilities", command=self.run_simulation)
        self.simulate_button.grid(row=4, columnspan=2, padx=10, pady=10)

        # Player selection dropdown for hand distribution
        tk.Label(self.root, text="Select Player for Hand Distribution:").grid(row=5, column=0, padx=10, pady=10)
        self.player_distribution_combo = ttk.Combobox(self.root, state='readonly')
        self.player_distribution_combo.grid(row=5, column=1, padx=10, pady=10)

        # Visualize Player Hand Distribution Button
        self.visualize_distribution_button = tk.Button(self.root, text="Visualize Hand Distribution", command=self.visualize_hand_distribution)
        self.visualize_distribution_button.grid(row=6, columnspan=2, padx=10, pady=10)

    def add_community_card(self):
        if len(self.community_cards) < 5:
            new_card = self.community_cards_var.get().strip()
            if new_card:
                self.community_cards.append(new_card)
                self.community_cards_var.set('') 
                messagebox.showinfo("Success", f"Community card '{new_card}' added.")
            else:
                messagebox.showwarning("Input Error", "Please enter a community card.")
        else:
            messagebox.showwarning("Limit Reached", "Maximum of 5 community cards reached.")

    def run_simulation(self):
        try:
            num_players = self.num_players.get()
            if num_players < 2 or num_players > 9:
                raise ValueError("Number of players must be between 2 and 9.")

            your_hand = self.your_cards.get().strip().split(',')
            community_cards = self.community_cards

            self.players = [pp.Player(f'Player {i+1}') for i in range(num_players)]
            your_player = pp.Player('You', pp.Card.of(*[card.strip() for card in your_hand]))
            self.players[0] = your_player 

            cc = pp.Card.of(*[card.strip() for card in community_cards])

            simulator = pp.PokerRound.PokerRoundSimulator(
                community_cards=cc,
                players=self.players,
                total_players=num_players
            )
            self.simulation_result = simulator.simulate(n=10000, n_jobs=1)
            self.simulation_result.visualize_winner_distribution()

            self.community_cards.clear() 
            self.community_cards_var.set('') 

            self.update_player_distribution_dropdown()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def update_player_distribution_dropdown(self):
        player_names = [player.name for player in self.players]
        self.player_distribution_combo['values'] = player_names
        if player_names:
            self.player_distribution_combo.current(0) 

    def visualize_hand_distribution(self):
        selected_player_name = self.player_distribution_combo.get()
        if selected_player_name:
            selected_player = next((player for player in self.players if player.name == selected_player_name), None)
            if selected_player:
                if self.simulation_result:  
                    self.simulation_result.visualize_player_hand_distribution(selected_player)
                else:
                    messagebox.showwarning("Simulation Error", "Please run the simulation first.")
            else:
                messagebox.showwarning("Player Not Found", "Selected player does not exist.")
        else:
            messagebox.showwarning("Selection Error", "Please select a player.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PokerSimulatorApp(root)
    root.mainloop()
