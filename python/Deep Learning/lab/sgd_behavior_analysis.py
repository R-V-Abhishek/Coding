import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models, optimizers
import tensorflow as tf

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

def create_data():
    X = np.random.randn(1000, 10)
    y = np.random.randn(1000, 1)
    return X, y

def create_model():
    model = models.Sequential([
        layers.Dense(50, activation='relu', input_shape=(10,)),
        layers.Dense(20, activation='relu'),
        layers.Dense(1)
    ])
    return model

def detailed_sgd_analysis():
    """
    Analyze SGD behavior in detail to understand the 70-90 epoch anomaly
    """
    X, y = create_data()
    
    # Use the hyperparameters from our previous analysis
    adam_lr = 0.0005
    sgd_lr = adam_lr * 10  # 0.005
    batch_size = 32
    epochs = 100
    
    print("🔍 Detailed SGD Analysis: Understanding the 70-90 Epoch Behavior")
    print("=" * 70)
    
    # Create models
    model_adam = create_model()
    model_sgd = create_model()
    model_sgd_momentum = create_model()
    
    # Optimizers
    optimizer_adam = optimizers.Adam(learning_rate=adam_lr)
    optimizer_sgd = optimizers.SGD(learning_rate=sgd_lr)  # No momentum
    optimizer_sgd_momentum = optimizers.SGD(learning_rate=sgd_lr, momentum=0.9)
    
    # Compile models
    model_adam.compile(optimizer=optimizer_adam, loss='mse')
    model_sgd.compile(optimizer=optimizer_sgd, loss='mse')
    model_sgd_momentum.compile(optimizer=optimizer_sgd_momentum, loss='mse')
    
    # Train with detailed tracking
    print("Training models with detailed loss tracking...")
    
    # Store detailed metrics
    detailed_metrics = {
        'adam': {'train_loss': [], 'val_loss': [], 'lr': []},
        'sgd': {'train_loss': [], 'val_loss': [], 'lr': []},
        'sgd_momentum': {'train_loss': [], 'val_loss': [], 'lr': []}
    }
    
    # Train epoch by epoch to capture detailed metrics
    for epoch in range(epochs):
        # Adam training
        hist_adam = model_adam.fit(X, y, batch_size=batch_size, epochs=1, verbose=0, validation_split=0.2)
        detailed_metrics['adam']['train_loss'].append(hist_adam.history['loss'][0])
        detailed_metrics['adam']['val_loss'].append(hist_adam.history['val_loss'][0])
        detailed_metrics['adam']['lr'].append(adam_lr)
        
        # SGD training (no momentum)
        hist_sgd = model_sgd.fit(X, y, batch_size=batch_size, epochs=1, verbose=0, validation_split=0.2)
        detailed_metrics['sgd']['train_loss'].append(hist_sgd.history['loss'][0])
        detailed_metrics['sgd']['val_loss'].append(hist_sgd.history['val_loss'][0])
        detailed_metrics['sgd']['lr'].append(sgd_lr)
        
        # SGD with momentum training
        hist_sgd_mom = model_sgd_momentum.fit(X, y, batch_size=batch_size, epochs=1, verbose=0, validation_split=0.2)
        detailed_metrics['sgd_momentum']['train_loss'].append(hist_sgd_mom.history['loss'][0])
        detailed_metrics['sgd_momentum']['val_loss'].append(hist_sgd_mom.history['val_loss'][0])
        detailed_metrics['sgd_momentum']['lr'].append(sgd_lr)
        
        # Print progress every 10 epochs
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1:3d} | Adam: {detailed_metrics['adam']['val_loss'][-1]:.4f} | "
                  f"SGD: {detailed_metrics['sgd']['val_loss'][-1]:.4f} | "
                  f"SGD+Mom: {detailed_metrics['sgd_momentum']['val_loss'][-1]:.4f}")
    
    return detailed_metrics

def analyze_loss_patterns(detailed_metrics):
    """
    Analyze specific patterns in loss curves
    """
    print("\n" + "=" * 70)
    print("📊 LOSS PATTERN ANALYSIS")
    print("=" * 70)
    
    # Focus on the 70-90 epoch region
    start_epoch, end_epoch = 70, 90
    
    sgd_losses = detailed_metrics['sgd']['val_loss'][start_epoch:end_epoch]
    adam_losses = detailed_metrics['adam']['val_loss'][start_epoch:end_epoch]
    
    # Calculate statistics for this region
    sgd_volatility = np.std(sgd_losses)
    adam_volatility = np.std(adam_losses)
    
    sgd_trend = np.polyfit(range(len(sgd_losses)), sgd_losses, 1)[0]  # Linear trend
    adam_trend = np.polyfit(range(len(adam_losses)), adam_losses, 1)[0]
    
    print(f"📈 Epochs {start_epoch}-{end_epoch} Analysis:")
    print(f"   SGD Volatility (std):     {sgd_volatility:.4f}")
    print(f"   Adam Volatility (std):    {adam_volatility:.4f}")
    print(f"   SGD Trend (slope):        {sgd_trend:.6f}")
    print(f"   Adam Trend (slope):       {adam_trend:.6f}")
    
    # Identify specific issues
    print(f"\n🔍 Specific Issues Identified:")
    
    # Check for oscillations
    sgd_oscillations = count_oscillations(sgd_losses)
    adam_oscillations = count_oscillations(adam_losses)
    print(f"   SGD Oscillations:         {sgd_oscillations}")
    print(f"   Adam Oscillations:        {adam_oscillations}")
    
    # Check for sudden jumps
    sgd_jumps = find_sudden_jumps(sgd_losses, threshold=0.1)
    adam_jumps = find_sudden_jumps(adam_losses, threshold=0.1)
    print(f"   SGD Sudden Jumps:         {len(sgd_jumps)}")
    print(f"   Adam Sudden Jumps:        {len(adam_jumps)}")
    
    return {
        'sgd_volatility': sgd_volatility,
        'adam_volatility': adam_volatility,
        'sgd_oscillations': sgd_oscillations,
        'adam_oscillations': adam_oscillations,
        'sgd_jumps': sgd_jumps,
        'adam_jumps': adam_jumps
    }

def count_oscillations(losses, min_change=0.01):
    """Count the number of oscillations (direction changes) in loss"""
    if len(losses) < 3:
        return 0
    
    oscillations = 0
    prev_direction = None
    
    for i in range(1, len(losses)):
        change = losses[i] - losses[i-1]
        if abs(change) > min_change:  # Only count significant changes
            current_direction = 'up' if change > 0 else 'down'
            if prev_direction and current_direction != prev_direction:
                oscillations += 1
            prev_direction = current_direction
    
    return oscillations

def find_sudden_jumps(losses, threshold=0.1):
    """Find epochs where loss suddenly jumps up"""
    jumps = []
    for i in range(1, len(losses)):
        change = losses[i] - losses[i-1]
        if change > threshold:
            jumps.append((i, change))
    return jumps

def plot_detailed_analysis(detailed_metrics):
    """
    Create detailed plots to visualize the SGD behavior
    """
    epochs = range(len(detailed_metrics['adam']['val_loss']))
    
    plt.figure(figsize=(20, 12))
    
    # Plot 1: Full training curves
    plt.subplot(3, 3, 1)
    plt.plot(epochs, detailed_metrics['adam']['val_loss'], label='Adam', color='blue', alpha=0.8)
    plt.plot(epochs, detailed_metrics['sgd']['val_loss'], label='SGD (No Momentum)', color='red', alpha=0.8)
    plt.plot(epochs, detailed_metrics['sgd_momentum']['val_loss'], label='SGD + Momentum', color='green', alpha=0.8)
    plt.xlabel('Epochs')
    plt.ylabel('Validation Loss')
    plt.title('Full Training Curves')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Zoomed view of epochs 60-100
    plt.subplot(3, 3, 2)
    zoom_start, zoom_end = 60, 100
    zoom_epochs = range(zoom_start, min(zoom_end, len(epochs)))
    plt.plot(zoom_epochs, detailed_metrics['adam']['val_loss'][zoom_start:zoom_end], 
             label='Adam', color='blue', linewidth=2)
    plt.plot(zoom_epochs, detailed_metrics['sgd']['val_loss'][zoom_start:zoom_end], 
             label='SGD (No Momentum)', color='red', linewidth=2)
    plt.plot(zoom_epochs, detailed_metrics['sgd_momentum']['val_loss'][zoom_start:zoom_end], 
             label='SGD + Momentum', color='green', linewidth=2)
    plt.xlabel('Epochs')
    plt.ylabel('Validation Loss')
    plt.title('Zoomed: Epochs 60-100 (Problem Region)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Loss differences from Adam baseline
    plt.subplot(3, 3, 3)
    adam_baseline = detailed_metrics['adam']['val_loss']
    sgd_diff = [sgd - adam for sgd, adam in zip(detailed_metrics['sgd']['val_loss'], adam_baseline)]
    sgd_mom_diff = [sgd - adam for sgd, adam in zip(detailed_metrics['sgd_momentum']['val_loss'], adam_baseline)]
    
    plt.plot(epochs, sgd_diff, label='SGD - Adam', color='red', alpha=0.7)
    plt.plot(epochs, sgd_mom_diff, label='SGD+Mom - Adam', color='green', alpha=0.7)
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    plt.xlabel('Epochs')
    plt.ylabel('Loss Difference from Adam')
    plt.title('Performance Gap vs Adam')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 4: Moving average (smoothed curves)
    plt.subplot(3, 3, 4)
    window = 5
    adam_smooth = moving_average(detailed_metrics['adam']['val_loss'], window)
    sgd_smooth = moving_average(detailed_metrics['sgd']['val_loss'], window)
    sgd_mom_smooth = moving_average(detailed_metrics['sgd_momentum']['val_loss'], window)
    
    plt.plot(epochs[:len(adam_smooth)], adam_smooth, label='Adam (Smoothed)', color='blue')
    plt.plot(epochs[:len(sgd_smooth)], sgd_smooth, label='SGD (Smoothed)', color='red')
    plt.plot(epochs[:len(sgd_mom_smooth)], sgd_mom_smooth, label='SGD+Mom (Smoothed)', color='green')
    plt.xlabel('Epochs')
    plt.ylabel('Validation Loss (Moving Avg)')
    plt.title('Smoothed Curves (5-epoch window)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 5: Epoch-to-epoch changes
    plt.subplot(3, 3, 5)
    adam_changes = np.diff(detailed_metrics['adam']['val_loss'])
    sgd_changes = np.diff(detailed_metrics['sgd']['val_loss'])
    sgd_mom_changes = np.diff(detailed_metrics['sgd_momentum']['val_loss'])
    
    plt.plot(epochs[1:], adam_changes, label='Adam Changes', color='blue', alpha=0.6)
    plt.plot(epochs[1:], sgd_changes, label='SGD Changes', color='red', alpha=0.6)
    plt.plot(epochs[1:], sgd_mom_changes, label='SGD+Mom Changes', color='green', alpha=0.6)
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    plt.xlabel('Epochs')
    plt.ylabel('Loss Change (Δ)')
    plt.title('Epoch-to-Epoch Loss Changes')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 6: Volatility over time (rolling standard deviation)
    plt.subplot(3, 3, 6)
    window = 10
    adam_volatility = rolling_std(detailed_metrics['adam']['val_loss'], window)
    sgd_volatility = rolling_std(detailed_metrics['sgd']['val_loss'], window)
    sgd_mom_volatility = rolling_std(detailed_metrics['sgd_momentum']['val_loss'], window)
    
    plt.plot(epochs[:len(adam_volatility)], adam_volatility, label='Adam Volatility', color='blue')
    plt.plot(epochs[:len(sgd_volatility)], sgd_volatility, label='SGD Volatility', color='red')
    plt.plot(epochs[:len(sgd_mom_volatility)], sgd_mom_volatility, label='SGD+Mom Volatility', color='green')
    plt.xlabel('Epochs')
    plt.ylabel('Rolling Std Dev (10 epochs)')
    plt.title('Training Stability Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 7: Histogram of loss values in problem region
    plt.subplot(3, 3, 7)
    problem_start, problem_end = 70, 90
    adam_problem = detailed_metrics['adam']['val_loss'][problem_start:problem_end]
    sgd_problem = detailed_metrics['sgd']['val_loss'][problem_start:problem_end]
    
    plt.hist(adam_problem, bins=10, alpha=0.6, label='Adam (70-90)', color='blue')
    plt.hist(sgd_problem, bins=10, alpha=0.6, label='SGD (70-90)', color='red')
    plt.xlabel('Loss Value')
    plt.ylabel('Frequency')
    plt.title('Loss Distribution: Epochs 70-90')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 8: Training vs Validation Loss for SGD
    plt.subplot(3, 3, 8)
    plt.plot(epochs, detailed_metrics['sgd']['train_loss'], label='SGD Training', color='orange', alpha=0.7)
    plt.plot(epochs, detailed_metrics['sgd']['val_loss'], label='SGD Validation', color='red', alpha=0.7)
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('SGD: Training vs Validation Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 9: Convergence rate comparison
    plt.subplot(3, 3, 9)
    # Calculate distance from final loss
    adam_final = detailed_metrics['adam']['val_loss'][-1]
    sgd_final = detailed_metrics['sgd']['val_loss'][-1]
    
    adam_convergence = [abs(loss - adam_final) for loss in detailed_metrics['adam']['val_loss']]
    sgd_convergence = [abs(loss - sgd_final) for loss in detailed_metrics['sgd']['val_loss']]
    
    plt.semilogy(epochs, adam_convergence, label='Adam Convergence', color='blue')
    plt.semilogy(epochs, sgd_convergence, label='SGD Convergence', color='red')
    plt.xlabel('Epochs')
    plt.ylabel('Distance from Final Loss (log scale)')
    plt.title('Convergence Rate Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def moving_average(data, window):
    """Calculate moving average"""
    return np.convolve(data, np.ones(window)/window, mode='valid')

def rolling_std(data, window):
    """Calculate rolling standard deviation"""
    result = []
    for i in range(window-1, len(data)):
        window_data = data[i-window+1:i+1]
        result.append(np.std(window_data))
    return result

def explain_sgd_behavior():
    """
    Provide detailed explanation of SGD behavior
    """
    print("\n" + "=" * 70)
    print("🧠 EXPLANATION: Why SGD Shows Abnormal Behavior in Epochs 70-90")
    print("=" * 70)
    
    explanations = [
        ("🎯 1. Learning Rate Too High", 
         "SGD lr=0.005 might be too aggressive, causing overshooting around local minima"),
        
        ("⚡ 2. No Momentum", 
         "Pure SGD lacks momentum to smooth out oscillations and maintain direction"),
        
        ("🌊 3. Loss Landscape Navigation", 
         "SGD is bouncing around in a complex loss landscape without adaptive scaling"),
        
        ("📊 4. Batch Variance", 
         "Mini-batch gradient estimates are noisier than Adam's smoothed gradients"),
        
        ("🔄 5. Local Minima Escaping", 
         "SGD's noise helps escape shallow local minima but causes instability"),
        
        ("⚖️ 6. No Adaptive Scaling", 
         "Unlike Adam, SGD doesn't adjust per-parameter learning rates automatically"),
        
        ("🎰 7. Stochastic Nature", 
         "The 'S' in SGD - inherent randomness from mini-batch sampling"),
        
        ("🏔️ 8. Plateau Navigation", 
         "SGD struggles on flat regions of loss surface without adaptive mechanisms")
    ]
    
    for title, explanation in explanations:
        print(f"\n{title}")
        print(f"   {explanation}")
    
    print(f"\n💡 SOLUTIONS:")
    solutions = [
        "✅ Add momentum (0.9) to smooth gradient updates",
        "✅ Use learning rate scheduling (reduce lr when stuck)",
        "✅ Lower the learning rate (try 0.001-0.002 instead of 0.005)",
        "✅ Use larger batch sizes to reduce gradient noise",
        "✅ Add weight decay for regularization",
        "✅ Consider AdamW as a compromise solution"
    ]
    
    for solution in solutions:
        print(f"   {solution}")

# Main execution
if __name__ == "__main__":
    # Run detailed analysis
    detailed_metrics = detailed_sgd_analysis()
    
    # Analyze loss patterns
    pattern_analysis = analyze_loss_patterns(detailed_metrics)
    
    # Create detailed plots
    plot_detailed_analysis(detailed_metrics)
    
    # Explain the behavior
    explain_sgd_behavior()
