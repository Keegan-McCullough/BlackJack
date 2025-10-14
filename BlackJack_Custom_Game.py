import pandas as pd
import matplotlib.pyplot as plt
from BlackJack_Engine import Game

# --- Simulation Runner (copied from simulation_main.py) ---

def run_session(bet_strategy_fn, initial_bet, starting_bankroll, rounds_per_session):
    """Simulates one full session of playing blackjack."""
    bankroll = starting_bankroll
    current_bet = initial_bet
    last_outcome = 'win'  # Start fresh
    win_streak = 0
    loss_streak = 0
    game = Game()
    
    for _ in range(rounds_per_session):
        # Stop if bankroll is zero or less
        if bankroll <= 0:
            break
            
        bet_amount = bet_strategy_fn(
            initial_bet=initial_bet,
            current_bet=current_bet,
            last_outcome=last_outcome,
            bankroll=bankroll,
            win_streak=win_streak,
            loss_streak=loss_streak
        )
        
        # Ensure player can cover the bet and bet is at least 1
        bet_amount = max(1, bet_amount)
        if bet_amount > bankroll:
            bet_amount = bankroll
            
        winnings = game.play_round(bet_amount)
        bankroll += winnings
        
        if winnings > 0:
            last_outcome = 'win'
            win_streak += 1
            loss_streak = 0
        else:
            last_outcome = 'loss' # Treat push as a loss for betting purposes
            loss_streak += 1
            win_streak = 0
        
        current_bet = bet_amount
            
    return bankroll

# --- Interactive Custom Strategy Definition ---

def get_custom_strategy_from_user():
    """
    Prompts the user to input their strategy logic and dynamically
    creates a Python function from it.
    """
    print("\n--- Define Your Custom Betting Strategy ---")
    print("You can use the following variables in your logic:")
    print("  - initial_bet: The starting bet amount you choose.")
    print("  - current_bet: The amount of the last bet placed.")
    print("  - last_outcome: A string, either 'win' or 'loss'.")
    print("  - bankroll: Your current total money.")
    print("  - win_streak: How many hands you've won in a row.")
    print("  - loss_streak: How many hands you've lost in a row.")
    print("\nYour code must return the new bet amount.")
    print("Example (Martingale): if last_outcome == 'loss': return current_bet * 2\nelse: return initial_bet")
    print("Example (D'Alembert): if last_outcome == 'loss': return current_bet + 5\nelse: return max(initial_bet, current_bet - 5)")
    print("\nEnter your strategy logic (press Enter twice to finish):")

    lines = []
    while True:
        line = input("> ")
        if not line:
            break
        lines.append("    " + line) # Add indentation
    
    user_code = "\n".join(lines)
    
    # Define a function using the user's code
    strategy_code = f"""
def custom_strategy(initial_bet, current_bet, last_outcome, bankroll, win_streak, loss_streak):
    # Default to initial bet if no logic is provided
    new_bet = initial_bet 
{user_code}
    return new_bet
"""
    
    try:
        # Execute the code to define the function in the local scope
        scope = {}
        exec(strategy_code, globals(), scope)
        print("\nStrategy compiled successfully!")
        return scope['custom_strategy']
    except Exception as e:
        print(f"\nError in your strategy code: {e}")
        return None

# --- Main Execution ---

if __name__ == "__main__":
    print("--- Blackjack Custom Strategy Simulator ---")
    
    # Get simulation parameters from user
    try:
        start_bankroll = int(input("Enter your starting bankroll (e.g., 1000): "))
        initial_bet_size = int(input("Enter your initial bet size (e.g., 25): "))
        num_sims = int(input("Enter the number of simulations to run (e.g., 500): "))
        num_rounds = int(input("Enter the number of hands per simulation (e.g., 200): "))
    except ValueError:
        print("Invalid input. Please enter whole numbers.")
        exit()

    # Get the custom strategy
    custom_strategy_fn = get_custom_strategy_from_user()

    if custom_strategy_fn:
        final_bankrolls = []
        print(f"\nRunning {num_sims} simulations...")
        for i in range(num_sims):
            final_bankroll = run_session(custom_strategy_fn, initial_bet_size, start_bankroll, num_rounds)
            final_bankrolls.append(final_bankroll)
        
        # --- Analysis ---
        avg_final_bankroll = sum(final_bankrolls) / len(final_bankrolls)
        net_profit = avg_final_bankroll - start_bankroll
        bust_count = sum(1 for b in final_bankrolls if b <= 0)
        bust_rate = (bust_count / num_sims) * 100
        profit_count = sum(1 for b in final_bankrolls if b > start_bankroll)
        profit_rate = (profit_count / num_sims) * 100

        print("\n--- Simulation Complete: Results ---")
        print(f"Average Final Bankroll: ${avg_final_bankroll:,.2f}")
        print(f"Average Net Profit/Loss: ${net_profit:,.2f}")
        print(f"Chance of Profit: {profit_rate:.2f}%")
        print(f"Chance of Busting (losing all money): {bust_rate:.2f}%")

        # --- Visualization ---
        plt.figure(figsize=(10, 6))
        plt.hist(final_bankrolls, bins=50, edgecolor='black')
        plt.title(f'Distribution of Final Bankrolls over {num_sims} Simulations')
        plt.xlabel("Final Bankroll ($)")
        plt.ylabel("Number of Simulations")
        plt.axvline(x=start_bankroll, color='r', linestyle='--', label=f'Starting Bankroll (${start_bankroll})')
        plt.axvline(x=avg_final_bankroll, color='g', linestyle='--', label=f'Average Result (${avg_final_bankroll:,.2f})')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()