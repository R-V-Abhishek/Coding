import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
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

def hyperparameter_search_with_adam(X, y):
    """
    Use Adam to quickly find good hyperparameters
    """
    print("=" * 60)
    print("PHASE 1: Hyperparameter Search with Adam")
    print("=" * 60)
    
    # Test different learning rates with Adam
    learning_rates = [0.01, 0.005, 0.001, 0.0005]
    batch_sizes = [16, 32, 64]
    
    best_loss = float('inf')
    best_lr = None
    best_batch_size = None
    
    results = []
    
    for lr in learning_rates:
        for batch_size in batch_sizes:
            print(f"\nTesting Adam: lr={lr}, batch_size={batch_size}")
            
            # Create fresh model
            model = create_model()
            optimizer = optimizers.Adam(learning_rate=lr)
            model.compile(optimizer=optimizer, loss='mse')
            
            # Quick training (fewer epochs for search)
            history = model.fit(X, y, 
                              batch_size=batch_size, 
                              epochs=30, 
                              verbose=0,
                              validation_split=0.2)
            
            final_loss = history.history['val_loss'][-1]
            print(f"Final validation loss: {final_loss:.4f}")
            
            results.append({
                'lr': lr,
                'batch_size': batch_size,
                'final_loss': final_loss,
                'history': history.history
            })
            
            if final_loss < best_loss:
                best_loss = final_loss
                best_lr = lr
                best_batch_size = batch_size
    
    print(f"\n🎯 Best hyperparameters found with Adam:")
    print(f"   Learning Rate: {best_lr}")
    print(f"   Batch Size: {best_batch_size}")
    print(f"   Best Validation Loss: {best_loss:.4f}")
    
    return best_lr, best_batch_size, results

def train_with_optimized_hyperparameters(X, y, best_lr, best_batch_size):
    """
    Now use the found hyperparameters with both Adam and SGD
    """
    print("\n" + "=" * 60)
    print("PHASE 2: Training with Optimized Hyperparameters")
    print("=" * 60)
    
    epochs = 100  # More epochs for final training
    
    # Model 1: Adam with found hyperparameters
    print(f"\n🔍 Training Adam with lr={best_lr}, batch_size={best_batch_size}")
    model_adam = create_model()
    optimizer_adam = optimizers.Adam(learning_rate=best_lr)
    model_adam.compile(optimizer=optimizer_adam, loss='mse')
    
    history_adam = model_adam.fit(X, y, 
                                 batch_size=best_batch_size, 
                                 epochs=epochs, 
                                 verbose=0,
                                 validation_split=0.2)
    
    # Model 2: SGD with ADAPTED hyperparameters
    # Key insight: SGD typically needs higher learning rate than Adam
    sgd_lr = best_lr * 10  # Common practice: SGD lr = Adam lr * 5-20
    
    print(f"\n🔍 Training SGD with ADAPTED lr={sgd_lr}, batch_size={best_batch_size}")
    model_sgd = create_model()
    optimizer_sgd = optimizers.SGD(learning_rate=sgd_lr, momentum=0.9)
    model_sgd.compile(optimizer=optimizer_sgd, loss='mse')
    
    history_sgd = model_sgd.fit(X, y, 
                               batch_size=best_batch_size, 
                               epochs=epochs, 
                               verbose=0,
                               validation_split=0.2)
    
    # Model 3: SGD with learning rate scheduling
    print(f"\n🔍 Training SGD with LR Scheduling")
    model_sgd_scheduled = create_model()
    optimizer_sgd_scheduled = optimizers.SGD(learning_rate=sgd_lr, momentum=0.9)
    model_sgd_scheduled.compile(optimizer=optimizer_sgd_scheduled, loss='mse')
    
    # Add learning rate decay
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=1e-6)
    
    history_sgd_scheduled = model_sgd_scheduled.fit(X, y,
                                                   batch_size=best_batch_size,
                                                   epochs=epochs,
                                                   verbose=0,
                                                   validation_split=0.2,
                                                   callbacks=[lr_scheduler])
    
    return history_adam, history_sgd, history_sgd_scheduled

def plot_comparison(history_adam, history_sgd, history_sgd_scheduled):
    """
    Plot the comparison of all three approaches
    """
    plt.figure(figsize=(15, 5))
    
    # Training Loss
    plt.subplot(1, 3, 1)
    plt.plot(history_adam.history['loss'], label='Adam (Optimized)', color='blue')
    plt.plot(history_sgd.history['loss'], label='SGD (Adapted)', color='red')
    plt.plot(history_sgd_scheduled.history['loss'], label='SGD + Scheduling', color='green')
    plt.xlabel('Epochs')
    plt.ylabel('Training Loss')
    plt.title('Training Loss Comparison')
    plt.legend()
    plt.grid(True)
    
    # Validation Loss
    plt.subplot(1, 3, 2)
    plt.plot(history_adam.history['val_loss'], label='Adam (Optimized)', color='blue')
    plt.plot(history_sgd.history['val_loss'], label='SGD (Adapted)', color='red')
    plt.plot(history_sgd_scheduled.history['val_loss'], label='SGD + Scheduling', color='green')
    plt.xlabel('Epochs')
    plt.ylabel('Validation Loss')
    plt.title('Validation Loss Comparison')
    plt.legend()
    plt.grid(True)
    
    # Final comparison
    plt.subplot(1, 3, 3)
    final_losses = [
        history_adam.history['val_loss'][-1],
        history_sgd.history['val_loss'][-1],
        history_sgd_scheduled.history['val_loss'][-1]
    ]
    methods = ['Adam\n(Optimized)', 'SGD\n(Adapted)', 'SGD +\nScheduling']
    colors = ['blue', 'red', 'green']
    
    bars = plt.bar(methods, final_losses, color=colors, alpha=0.7)
    plt.ylabel('Final Validation Loss')
    plt.title('Final Performance')
    plt.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, loss in zip(bars, final_losses):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{loss:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.show()

def print_final_results(history_adam, history_sgd, history_sgd_scheduled):
    """
    Print detailed comparison of results
    """
    print("\n" + "=" * 60)
    print("FINAL RESULTS COMPARISON")
    print("=" * 60)
    
    adam_final = history_adam.history['val_loss'][-1]
    sgd_final = history_sgd.history['val_loss'][-1]
    sgd_scheduled_final = history_sgd_scheduled.history['val_loss'][-1]
    
    print(f"Adam (Optimized):           {adam_final:.4f}")
    print(f"SGD (Adapted):              {sgd_final:.4f}")
    print(f"SGD + LR Scheduling:        {sgd_scheduled_final:.4f}")
    
    # Find the best
    best_loss = min(adam_final, sgd_final, sgd_scheduled_final)
    if best_loss == adam_final:
        winner = "Adam (Optimized)"
    elif best_loss == sgd_final:
        winner = "SGD (Adapted)"
    else:
        winner = "SGD + LR Scheduling"
    
    print(f"\n🏆 Best performer: {winner} with loss {best_loss:.4f}")
    
    # Performance improvements
    adam_vs_sgd = ((sgd_final - adam_final) / adam_final) * 100
    adam_vs_scheduled = ((sgd_scheduled_final - adam_final) / adam_final) * 100
    
    print(f"\n📊 Performance Analysis:")
    print(f"   SGD vs Adam: {adam_vs_sgd:+.1f}% ({'worse' if adam_vs_sgd > 0 else 'better'})")
    print(f"   SGD+Scheduling vs Adam: {adam_vs_scheduled:+.1f}% ({'worse' if adam_vs_scheduled > 0 else 'better'})")

# Main execution
if __name__ == "__main__":
    # Load data
    X, y = create_data()
    
    # Phase 1: Use Adam to find good hyperparameters
    best_lr, best_batch_size, search_results = hyperparameter_search_with_adam(X, y)
    
    # Phase 2: Use found hyperparameters with different optimizers
    history_adam, history_sgd, history_sgd_scheduled = train_with_optimized_hyperparameters(
        X, y, best_lr, best_batch_size
    )
    
    # Analysis and visualization
    plot_comparison(history_adam, history_sgd, history_sgd_scheduled)
    print_final_results(history_adam, history_sgd, history_sgd_scheduled)
    
    print("\n" + "=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)
    print("✅ Adam is excellent for hyperparameter search (fast convergence)")
    print("✅ SGD needs learning rate adaptation (typically 5-20x higher than Adam)")
    print("✅ SGD + scheduling can match or beat Adam's final performance")
    print("✅ Best strategy: Adam for search → SGD for production")
    print("✅ Always validate on separate test set for final evaluation!")
