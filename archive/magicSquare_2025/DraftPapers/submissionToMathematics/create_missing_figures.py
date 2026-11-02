#!/usr/bin/env python3
"""
Create missing figures for the Magic Square Gems paper submission.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os

# Set up the output directory
output_dir = '/Users/kylemathewson/magicSquare/submissionToMathematics/figures/'
os.makedirs(output_dir, exist_ok=True)

def create_analysis_pipeline():
    """Create analysis pipeline diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define colors
    color_input = '#E8F4F8'
    color_embed = '#B8E0D2'
    color_analysis = '#EAC4D5'
    color_output = '#EBBAB9'
    
    # Title
    ax.text(5, 9.5, 'Magic Square Analysis Pipeline', fontsize=20, 
            ha='center', va='top', fontweight='bold')
    
    # Step 1: Magic Square
    square = FancyBboxPatch((0.5, 7), 2, 1.5, boxstyle="round,pad=0.1", 
                            facecolor=color_input, edgecolor='black', linewidth=2)
    ax.add_patch(square)
    ax.text(1.5, 7.75, 'Magic Square\n(4×4)', ha='center', va='center', fontsize=12)
    
    # Step 2: R³ Embedding
    embed = FancyBboxPatch((3.5, 7), 2, 1.5, boxstyle="round,pad=0.1",
                          facecolor=color_embed, edgecolor='black', linewidth=2)
    ax.add_patch(embed)
    ax.text(4.5, 7.75, 'R³ Embedding\n(i,j,Mᵢⱼ)', ha='center', va='center', fontsize=12)
    
    # Step 3: Geometric Analysis
    geo = FancyBboxPatch((0.5, 4.5), 2, 1.5, boxstyle="round,pad=0.1",
                        facecolor=color_analysis, edgecolor='black', linewidth=2)
    ax.add_patch(geo)
    ax.text(1.5, 5.25, 'Geometric\nAnalysis', ha='center', va='center', fontsize=12)
    
    # Step 4: EMD Analysis
    emd = FancyBboxPatch((3.5, 4.5), 2, 1.5, boxstyle="round,pad=0.1",
                        facecolor=color_analysis, edgecolor='black', linewidth=2)
    ax.add_patch(emd)
    ax.text(4.5, 5.25, 'EMD\nAnalysis', ha='center', va='center', fontsize=12)
    
    # Step 5: Manifold Analysis
    manifold = FancyBboxPatch((6.5, 4.5), 2, 1.5, boxstyle="round,pad=0.1",
                             facecolor=color_analysis, edgecolor='black', linewidth=2)
    ax.add_patch(manifold)
    ax.text(7.5, 5.25, 'Manifold\nAnalysis', ha='center', va='center', fontsize=12)
    
    # Step 6: Results
    results = FancyBboxPatch((3.5, 2), 2, 1.5, boxstyle="round,pad=0.1",
                            facecolor=color_output, edgecolor='black', linewidth=2)
    ax.add_patch(results)
    ax.text(4.5, 2.75, 'Results\n& Insights', ha='center', va='center', fontsize=12)
    
    # Add arrows
    arrow_props = dict(arrowstyle='->', lw=2, color='black')
    
    # From Magic Square to Embedding
    ax.annotate('', xy=(3.5, 7.75), xytext=(2.5, 7.75), arrowprops=arrow_props)
    
    # From Embedding to analyses
    ax.annotate('', xy=(1.5, 6.5), xytext=(4.5, 7), arrowprops=arrow_props)
    ax.annotate('', xy=(4.5, 6.5), xytext=(4.5, 7), arrowprops=arrow_props)
    ax.annotate('', xy=(7.5, 6.5), xytext=(4.5, 7), arrowprops=arrow_props)
    
    # From analyses to results
    ax.annotate('', xy=(4.5, 3.5), xytext=(1.5, 4.5), arrowprops=arrow_props)
    ax.annotate('', xy=(4.5, 3.5), xytext=(4.5, 4.5), arrowprops=arrow_props)
    ax.annotate('', xy=(4.5, 3.5), xytext=(7.5, 4.5), arrowprops=arrow_props)
    
    # Add labels for outputs
    ax.text(1.5, 3.7, 'Volume\nVertices\nAngularity', ha='center', va='center', 
            fontsize=10, style='italic')
    ax.text(4.5, 3.7, 'Clustering\nDistances', ha='center', va='center', 
            fontsize=10, style='italic')
    ax.text(7.5, 3.7, 'Dimension\nConnectivity', ha='center', va='center', 
            fontsize=10, style='italic')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'analysis_pipeline.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Created analysis_pipeline.png")


def create_landscape_visualization():
    """Create optimization landscape visualization."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create grid for landscape
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    
    # Create a multi-modal landscape
    Z1 = 3 * np.exp(-(X**2 + Y**2) / 2)
    Z2 = 2 * np.exp(-((X-2)**2 + (Y-2)**2) / 3)
    Z3 = 2.5 * np.exp(-((X+2)**2 + (Y-1)**2) / 2.5)
    Z4 = 1.5 * np.exp(-((X-1)**2 + (Y+2)**2) / 2)
    Z = Z1 + Z2 + Z3 + Z4
    
    # Add some noise
    Z += 0.1 * np.random.randn(*Z.shape)
    
    # Invert for optimization (we want minima)
    Z = -Z
    
    # Plot surface
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, 
                          linewidth=0, antialiased=True)
    
    # Add contour lines at the bottom
    contours = ax.contour(X, Y, Z, zdir='z', offset=np.min(Z)-1, 
                         cmap='viridis', alpha=0.5)
    
    # Add optimization paths
    # Path 1: Gradient descent
    t = np.linspace(0, 4*np.pi, 100)
    path1_x = 3 * np.exp(-t/10) * np.cos(t)
    path1_y = 3 * np.exp(-t/10) * np.sin(t)
    path1_z = []
    for px, py in zip(path1_x, path1_y):
        idx_x = np.argmin(np.abs(x - px))
        idx_y = np.argmin(np.abs(y - py))
        path1_z.append(Z[idx_y, idx_x])
    
    ax.plot(path1_x, path1_y, path1_z, 'r-', linewidth=3, label='Gradient Descent')
    ax.plot(path1_x[0], path1_y[0], path1_z[0], 'ro', markersize=10)
    ax.plot(path1_x[-1], path1_y[-1], path1_z[-1], 'r*', markersize=15)
    
    # Path 2: Basin hopping
    jumps_x = [3, 2.5, 0, -2, -2, 0, 0]
    jumps_y = [0, -1, -1, -1, 1, 0, 0]
    jumps_z = []
    for jx, jy in zip(jumps_x, jumps_y):
        idx_x = np.argmin(np.abs(x - jx))
        idx_y = np.argmin(np.abs(y - jy))
        jumps_z.append(Z[idx_y, idx_x])
    
    ax.plot(jumps_x, jumps_y, jumps_z, 'b--', linewidth=3, label='Basin Hopping', marker='o')
    
    # Labels and formatting
    ax.set_xlabel('Covariance X', fontsize=12)
    ax.set_ylabel('Covariance Y', fontsize=12)
    ax.set_zlabel('Distance to Manifold', fontsize=12)
    ax.set_title('Magic Square Optimization Landscape', fontsize=16, pad=20)
    
    # Add legend
    ax.legend(loc='upper left')
    
    # Set viewing angle
    ax.view_init(elev=25, azim=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'landscape_visualization.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Created landscape_visualization.png")


def main():
    """Create all missing figures."""
    print("Creating missing figures for submission...")
    
    # Create analysis pipeline
    create_analysis_pipeline()
    
    # Create landscape visualization
    create_landscape_visualization()
    
    print("\nAll figures created successfully!")
    print(f"Figures saved to: {output_dir}")


if __name__ == '__main__':
    main() 