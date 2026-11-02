import numpy as np
import matplotlib.pyplot as plt
from core import reduce_to_unique
import json

# Load all magic squares
squares = np.load('magic_squares/data/magic_squares_20241031_133039.npy')
print(f"\nLoaded {len(squares)} magic squares")

# Reduce to unique squares
unique_squares = reduce_to_unique(squares)
print(f"\nReduced to {len(unique_squares)} unique squares")

# Export squares as JSON for web visualization
squares_list = [square.tolist() for square in unique_squares]
with open('magic_squares/web/unique_squares.json', 'w') as f:
    json.dump(squares_list, f)

# Plot a subset of the unique squares
n_squares_to_plot = 25  # We'll plot a 5x5 grid
fig, axes = plt.subplots(5, 5, figsize=(15, 15))
fig.suptitle('Sample of Unique 4x4 Magic Squares', fontsize=16)

for i in range(5):
    for j in range(5):
        idx = i * 5 + j
        square = unique_squares[idx]
        
        # Create heatmap
        ax = axes[i, j]
        im = ax.imshow(square, cmap='viridis')
        
        # Add text annotations
        for x in range(4):
            for y in range(4):
                ax.text(y, x, str(square[x, y]), 
                       ha='center', va='center', 
                       color='white' if square[x, y] < 12 else 'black')
        
        ax.set_title(f'Square {idx + 1}')
        ax.axis('off')

plt.tight_layout()
plt.savefig('magic_squares/web/unique_squares_sample.png')
plt.close()

print("\nPlot saved as 'unique_squares_sample.png'")
print("Squares exported as 'unique_squares.json'") 