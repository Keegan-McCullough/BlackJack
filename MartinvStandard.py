import pandas as pd
import matplotlib.pyplot as plt
from BlackJack_Engine import Game

# --- Simulation Constants ---
NUM_SIMULATIONS = 10000  # Number of times to run a full session
ROUNDS_PER_SESSION = 200 # Number of hands to play in one session
STARTING_BANKROLL = 800

# --- Betting Strategies ---

def flat_bet_strategy(initial_bet, **kwargs):
    """Always bets the same initial amount."""
    return initial_bet

def martingale_strategy(initial_bet, current_bet, last_outcome, **kwargs):
    """Doubles the bet on a loss, resets to initial on a win."""
    if last_outcome == 'win':
        return initial_bet
    else: # loss or push
        return current_bet * 2

# --- Simulation Runner ---

def run_session(bet_strategy_fn, initial_bet, stop_loss, profit_target):
    """Simulates one full session of playing blackjack."""
    bankroll = STARTING_BANKROLL
    current_bet = initial_bet
    last_outcome = 'win' # Start fresh
    game = Game()
    
    for _ in range(ROUNDS_PER_SESSION):
        if bankroll <= stop_loss or bankroll >= profit_target:
            break
        
        bet_amount = bet_strategy_fn(
            initial_bet=initial_bet, 
            current_bet=current_bet, 
            last_outcome=last_outcome, 
            bankroll=bankroll
        )
        
        # Ensure player can cover the bet
        if bet_amount > bankroll:
            bet_amount = bankroll

        if bankroll <= 0:
            break
            
        winnings = game.play_round(bet_amount)
        
        bankroll += winnings
        
        if winnings > 0:
            last_outcome = 'win'
        else:
            last_outcome = 'loss'
        
        current_bet = bet_amount
            
    return bankroll


# --- Main Execution ---

if __name__ == "__main__":
    print("Running Blackjack Betting Strategy Simulations...")

    # Define the parameters to test
    bet_strategies = {
        "Flat Betting": flat_bet_strategy,
        "Martingale": martingale_strategy
    }
    initial_bets_to_test = [10, 25, 50]
    
    results = []

    for strategy_name, strategy_fn in bet_strategies.items():
        for bet in initial_bets_to_test:
            final_bankrolls = []
            print(f"  Testing Strategy: {strategy_name} with Initial Bet: ${bet}")
            for i in range(NUM_SIMULATIONS):
                stop_loss = 0
                profit_target = STARTING_BANKROLL * 2 # e.g., double your money
                final_bankroll = run_session(strategy_fn, bet, stop_loss, profit_target)
                final_bankrolls.append(final_bankroll)
            
            # Record results for this configuration
            avg_final_bankroll = sum(final_bankrolls) / len(final_bankrolls)
            bust_rate = (sum(1 for b in final_bankrolls if b <= stop_loss) / NUM_SIMULATIONS) * 100
            
            results.append({
                "Strategy": strategy_name,
                "Initial Bet": bet,
                "Average Final Bankroll": avg_final_bankroll,
                "Bust Rate (%)": bust_rate
            })

    # --- Analysis with Pandas ---
    df = pd.DataFrame(results)
    
    print("\n--- Simulation Results ---")
    print(df.to_string())

    # --- Visualization with Matplotlib ---
    df.pivot(index="Initial Bet", columns="Strategy", values="Average Final Bankroll").plot(
        kind='bar', 
        figsize=(10, 6),
        title=f'Average Final Bankroll After {ROUNDS_PER_SESSION} Rounds (or limits hit)'
    )
    plt.ylabel("Average Final Bankroll ($)")
    plt.axhline(y=STARTING_BANKROLL, color='r', linestyle='--', label='Starting Bankroll')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
