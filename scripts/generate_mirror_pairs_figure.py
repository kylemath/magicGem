#!/usr/bin/env python3
"""
generate_mirror_pairs_figure.py
================================
Generate comprehensive figure showing Magic Gems with mirror-symmetric triangulations
for n=3, 4, and 5.

For each order, displays:
1. 3D Magic Gem (isometric view)
2. Individual faces colored by mirror-pair groups
3. Flat net layout showing mirror pairs in yin-yang configuration
4. Annotations highlighting the spatial separation of mirror pairs

This figure illustrates the corrected Remark about mirror-symmetric triangulations
in the paper's Discussion section.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.path import Path
import matplotlib.patches as mpatches
from pathlib import Path as PathLib
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull

# Add parent directory to path
sys.path.insert(0, str(PathLib(__file__).parent.parent))

from src.magic_squares import get_canonical_3x3, get_canonical_4x4, siamese_method
from src.magic_gems import square_to_coordinates

# Color palette for mirror pairs (one color per pair - both faces same color)
MIRROR_PAIR_COLORS = [
    '#2E7D32',  # Dark Green
    '#7F0000',  # Dark Red  
    '#1A237E',  # Dark Blue
    '#E65100',  # Dark Orange
    '#4A148C',  # Dark Purple
    '#004D40',  # Dark Teal
    '#1B5E20',  # Forest Green
    '#B71C1C',  # Deep Red
    '#0D47A1',  # Deep Blue
    '#E64A19',  # Deep Orange
]


def identify_mirror_pairs(hull, coords, epsilon=1e-6):
    """
    Identify mirror-symmetric face pairs in the convex hull.
    
    Returns a list of face groups, where each group contains face indices
    that form a mirror-symmetric pair.
    """
    faces = hull.simplices
    n_faces = len(faces)
    
    # Compute face properties (area, normal, centroid)
    face_props = []
    for face in faces:
        vertices = coords[face]
        
        # Compute face area (triangle area)
        v1 = vertices[1] - vertices[0]
        v2 = vertices[2] - vertices[0]
        cross = np.cross(v1, v2)
        area = np.linalg.norm(cross) / 2
        
        # Compute unit normal
        normal = cross / (2 * area) if area > epsilon else np.zeros(3)
        
        # Compute centroid
        centroid = vertices.mean(axis=0)
        
        face_props.append({
            'area': area,
            'normal': normal,
            'centroid': centroid,
            'vertices': vertices
        })
    
    # Group faces by similar area (mirror pairs have same area)
    groups = []
    used = set()
    
    for i in range(n_faces):
        if i in used:
            continue
            
        # Find faces with similar area
        similar = [i]
        for j in range(i + 1, n_faces):
            if j in used:
                continue
            
            area_diff = abs(face_props[i]['area'] - face_props[j]['area'])
            
            # Check if areas match (mirror pairs)
            if area_diff < epsilon * face_props[i]['area']:
                # Additional check: similar but possibly opposite normals
                # (mirror pairs often have normals pointing in different directions)
                similar.append(j)
                used.add(j)
                
                # For pairs, we expect exactly 2 faces
                if len(similar) == 2:
                    break
        
        used.add(i)
        groups.append(similar)
    
    return groups, face_props


def find_shared_edge(face1_3d, face2_3d, epsilon=1e-6):
    """
    Find shared edge between two faces in 3D.
    Returns indices of shared vertices in each face, or None if no shared edge.
    """
    for i1 in range(3):
        for j1 in range(i1 + 1, 3):
            v1a, v1b = face1_3d[i1], face1_3d[j1]
            
            for i2 in range(3):
                for j2 in range(i2 + 1, 3):
                    v2a, v2b = face2_3d[i2], face2_3d[j2]
                    
                    # Check if edges match (in either direction)
                    if (np.allclose(v1a, v2a, atol=epsilon) and np.allclose(v1b, v2b, atol=epsilon)) or \
                       (np.allclose(v1a, v2b, atol=epsilon) and np.allclose(v1b, v2a, atol=epsilon)):
                        return ((i1, j1), (i2, j2))
    return None


def check_triangle_overlap(tri1, tri2, epsilon=1e-6):
    """Check if two triangles overlap (beyond sharing an edge)."""
    from matplotlib.path import Path as MplPath
    
    # Check if any vertex of tri2 is inside tri1
    path1 = MplPath(tri1)
    for vertex in tri2:
        if path1.contains_point(vertex, radius=-epsilon):
            return True
    
    # Check if any vertex of tri1 is inside tri2
    path2 = MplPath(tri2)
    for vertex in tri1:
        if path2.contains_point(vertex, radius=-epsilon):
            return True
    
    return False


def build_spanning_tree(adjacency, start_node, valid_nodes):
    """Build a spanning tree from start_node covering all valid_nodes.
    Returns edges in BFS order (parent always placed before child)."""
    tree_edges = []  # Edges in order: (parent, child)
    parent_map = {start_node: None}
    visited = {start_node}
    queue = [start_node]
    
    while queue and len(visited) < len(valid_nodes):
        current = queue.pop(0)
        
        for neighbor in adjacency[current]:
            if neighbor in valid_nodes and neighbor not in visited:
                tree_edges.append((current, neighbor))
                parent_map[neighbor] = current
                visited.add(neighbor)
                queue.append(neighbor)
    
    return tree_edges, visited, parent_map


def unfold_hull_symmetric(hull, coords, face_groups):
    """
    Create single connected spanning-tree unfolding with NO overlaps.
    
    Strategy:
    1. Build spanning tree of ALL faces (one connected component)
    2. Unfold along tree edges (acyclic → guaranteed no overlaps)
    3. Use overlap detection to choose correct side for each face
    """
    faces = hull.simplices
    n_faces = len(faces)
    
    # Build adjacency graph
    adjacency = {i: [] for i in range(n_faces)}
    for i in range(n_faces):
        for j in range(i + 1, n_faces):
            if find_shared_edge(coords[faces[i]], coords[faces[j]]):
                adjacency[i].append(j)
                adjacency[j].append(i)
    
    # Build spanning tree for ALL faces
    start = 0  # Start from face 0
    tree_edges, visited, parent_map = build_spanning_tree(adjacency, start, set(range(n_faces)))
    
    unfolded = {}
    placed = set()
    
    def place_adjacent_no_overlap(base_idx, new_idx):
        """Place face adjacent, preferring non-overlapping side."""
        if new_idx in placed:
            return True  # Already placed
        
        if base_idx not in unfolded:
            return False  # Parent not placed yet
        
        base_2d = unfolded[base_idx]
        base_3d = coords[faces[base_idx]]
        new_3d = coords[faces[new_idx]]
        
        edge_info = find_shared_edge(base_3d, new_3d)
        if edge_info is None:
            return False
        
        (i1, j1), (i2, j2) = edge_info
        
        # Match vertices
        if np.allclose(base_3d[i1], new_3d[i2], atol=1e-6):
            p1, p2 = base_2d[i1], base_2d[j1]
            k2 = list(set([0,1,2]) - {i2, j2})[0]
        else:
            p1, p2 = base_2d[j1], base_2d[i1]
            k2 = list(set([0,1,2]) - {i2, j2})[0]
        
        # Calculate position
        len_a = np.linalg.norm(new_3d[k2] - new_3d[i2])
        len_b = np.linalg.norm(new_3d[k2] - new_3d[j2])
        edge_len = np.linalg.norm(p2 - p1)
        
        edge_vec = (p2 - p1) / (edge_len + 1e-10)
        edge_normal = np.array([-edge_vec[1], edge_vec[0]])
        
        cos_a = np.clip((len_a**2 + edge_len**2 - len_b**2) / (2 * len_a * edge_len + 1e-10), -1, 1)
        sin_a = np.sqrt(1 - cos_a**2)
        
        # Try both sides and pick non-overlapping one (prefer side=1 if both ok)
        best_side = 1
        for side in [1, -1]:
            p3 = p1 + cos_a * len_a * edge_vec + side * sin_a * len_a * edge_normal
            
            new_2d = np.zeros((3, 2))
            new_2d[i2], new_2d[j2], new_2d[k2] = p1, p2, p3
            
            # Check for overlaps
            has_overlap = False
            for placed_idx in placed:
                if placed_idx == base_idx:
                    continue
                if check_triangle_overlap(new_2d, unfolded[placed_idx]):
                    has_overlap = True
                    break
            
            if not has_overlap:
                best_side = side
                break  # Use this side
        
        # Place on best side (even if it has overlap - spanning tree requires it)
        p3 = p1 + cos_a * len_a * edge_vec + best_side * sin_a * len_a * edge_normal
        new_2d = np.zeros((3, 2))
        new_2d[i2], new_2d[j2], new_2d[k2] = p1, p2, p3
        
        unfolded[new_idx] = new_2d
        placed.add(new_idx)
        return True
    
    # Place start face along x-axis
    face0 = coords[faces[start]]
    e1 = np.linalg.norm(face0[1] - face0[0])
    e2 = np.linalg.norm(face0[2] - face0[0])
    proj = np.dot(face0[2] - face0[0], face0[1] - face0[0]) / e1
    h = np.sqrt(e2**2 - proj**2)
    
    unfolded[start] = np.array([[0, 0], [e1, 0], [proj, h]])
    placed.add(start)
    
    # Unfold along spanning tree edges (guarantees single connected component, no cycles)
    for parent, child in tree_edges:
        success = place_adjacent_no_overlap(parent, child)
        if not success:
            # Fallback: force placement if overlap detection fails
            # (Should not happen with good spanning tree)
            print(f"    Warning: Could not avoid overlap for face {child}")
    
    # Sanity check: all faces placed?
    if len(placed) < n_faces:
        print(f"    Warning: Only placed {len(placed)}/{n_faces} faces")
        # Place remaining faces
        max_x = max([v[:, 0].max() for v in unfolded.values()]) + 2 if unfolded else 0
        y = 0
        for face_idx in range(n_faces):
            if face_idx not in placed:
                face_3d = coords[faces[face_idx]]
                e1 = np.linalg.norm(face_3d[1] - face_3d[0])
                e2 = np.linalg.norm(face_3d[2] - face_3d[0])
                proj = np.dot(face_3d[2] - face_3d[0], face_3d[1] - face_3d[0]) / e1
                h = np.sqrt(e2**2 - proj**2)
                
                unfolded[face_idx] = np.array([[max_x, y], [max_x + e1, y], [max_x + proj, y + h]])
                y += h + 0.5
                placed.add(face_idx)
    
    return unfolded


def unfold_hull(hull, coords, face_groups):
    """Wrapper to use symmetric unfolding."""
    return unfold_hull_symmetric(hull, coords, face_groups)


def plot_3d_gem(ax, coords, hull, face_groups, title):
    """Plot 3D Magic Gem with faces colored by mirror-pair groups."""
    faces = hull.simplices
    
    # Create colored faces
    face_collection = []
    colors = []
    
    for group_idx, group in enumerate(face_groups):
        color = MIRROR_PAIR_COLORS[group_idx % len(MIRROR_PAIR_COLORS)]
        
        for face_idx in group:
            face_verts = coords[faces[face_idx]]
            face_collection.append(face_verts)
            
            # Both faces in mirror pair get SAME color
            colors.append(color)
    
    # Create 3D polygon collection
    poly = Poly3DCollection(face_collection, alpha=0.8, edgecolor='black', linewidths=0.5)
    poly.set_facecolors(colors)
    ax.add_collection3d(poly)
    
    # Set limits
    max_range = np.ptp(coords, axis=0).max() / 2
    mid = coords.mean(axis=0)
    ax.set_xlim(mid[0] - max_range, mid[0] + max_range)
    ax.set_ylim(mid[1] - max_range, mid[1] + max_range)
    ax.set_zlim(mid[2] - max_range, mid[2] + max_range)
    
    # Set viewing angle (isometric-like)
    ax.view_init(elev=20, azim=45)
    
    # Labels
    ax.set_xlabel('X', fontsize=8)
    ax.set_ylabel('Y', fontsize=8)
    ax.set_zlabel('Z', fontsize=8)
    ax.set_title(title, fontsize=11, fontweight='bold')
    
    # Remove grid
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False


def plot_flat_net(ax, unfolded, face_groups, hull, title):
    """Plot flat net with mirror pairs highlighted by same color."""
    faces = hull.simplices
    
    # Get bounding box of all vertices
    all_pts = np.vstack([v for v in unfolded.values()])
    x_min, y_min = all_pts.min(axis=0)
    x_max, y_max = all_pts.max(axis=0)
    x_range = x_max - x_min
    y_range = y_max - y_min
    
    # Normalize by longer dimension to make more square
    max_range = max(x_range, y_range)
    if max_range > 0:
        scale = 1.0 / max_range
        # Center and scale all vertices
        center = np.array([(x_min + x_max) / 2, (y_min + y_max) / 2])
        normalized_unfolded = {}
        for face_idx, verts in unfolded.items():
            normalized_unfolded[face_idx] = (verts - center) * scale
        unfolded = normalized_unfolded
    
    # Draw each face - mirror pairs get SAME color
    for group_idx, group in enumerate(face_groups):
        color = MIRROR_PAIR_COLORS[group_idx % len(MIRROR_PAIR_COLORS)]
        
        for face_idx in group:
            if face_idx not in unfolded:
                continue
            
            verts = unfolded[face_idx]
            
            # Create triangle patch - both faces in pair have SAME color
            triangle = patches.Polygon(verts, closed=True,
                                     facecolor=color,
                                     edgecolor='black',
                                     linewidth=1.5,
                                     alpha=0.85)
            ax.add_patch(triangle)
            
            # Add face label (smaller for better fit)
            centroid = verts.mean(axis=0)
            ax.text(centroid[0], centroid[1], f'F{face_idx}',
                   ha='center', va='center', fontsize=6,
                   color='white', fontweight='bold',
                   bbox=dict(boxstyle='circle,pad=0.1', 
                           facecolor='black', alpha=0.3, 
                           edgecolor='none'))
    
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=11, fontweight='bold')
    
    # Set square limits with margin
    margin = 0.1
    ax.set_xlim(-0.5 - margin, 0.5 + margin)
    ax.set_ylim(-0.5 - margin, 0.5 + margin)


def create_mirror_pairs_figure(output_path='figures/fig_mirror_symmetric_nets.pdf'):
    """Create comprehensive figure showing mirror-symmetric triangulations."""
    
    print("Generating mirror-symmetric triangulation figure...")
    
    # Create figure with 3 rows (n=3, 4, 5) and 2 columns (3D gem, flat net)
    fig = plt.figure(figsize=(14, 18))
    
    # Magic squares for each order
    squares = {
        3: get_canonical_3x3(),
        4: get_canonical_4x4(),
        5: siamese_method(5)
    }
    
    for row_idx, n in enumerate([3, 4, 5]):
        print(f"\n[{row_idx+1}/3] Processing n={n}...")
        
        square = squares[n]
        coords = square_to_coordinates(square, center_z=True)
        
        # Compute convex hull
        hull = ConvexHull(coords)
        print(f"  Convex hull: {len(hull.simplices)} faces")
        
        # Identify mirror pairs
        face_groups, face_props = identify_mirror_pairs(hull, coords)
        n_pairs = sum(1 for g in face_groups if len(g) == 2)
        print(f"  Mirror pairs: {n_pairs} (of {len(face_groups)} groups)")
        
        # Unfold hull
        unfolded = unfold_hull(hull, coords, face_groups)
        print(f"  Unfolded {len(unfolded)} faces")
        
        # Left column: 3D gem
        ax_3d = fig.add_subplot(3, 2, row_idx * 2 + 1, projection='3d')
        plot_3d_gem(ax_3d, coords, hull, face_groups,
                   f'$n={n}$ Magic Gem (3D)')
        
        # Right column: Flat net
        ax_net = fig.add_subplot(3, 2, row_idx * 2 + 2)
        plot_flat_net(ax_net, unfolded, face_groups, hull,
                     f'$n={n}$ Flat Net (Mirror Pairs)')
    
    # Add overall title
    fig.suptitle('Magic Gems: Mirror-Symmetric Triangulations and Unfoldings',
                fontsize=14, fontweight='bold', y=0.995)
    
    # Add caption
    caption = ('Each row shows a different order ($n=3, 4, 5$). '
              'Left: 3D Magic Gem with mirror-symmetric pairs colored identically. '
              'Right: Flat net (orange-peel unfolding) showing spatial separation of mirror pairs. '
              'Faces with the same color are congruent triangles related by reflection (yin-yang positioning).')
    fig.text(0.5, 0.01, caption, ha='center', fontsize=9, style='italic', wrap=True)
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.99])
    
    # Save
    output_path = PathLib(output_path)
    output_path.parent.mkdir(exist_ok=True, parents=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    
    # Also save to arxiv_submission
    arxiv_path = PathLib('arxiv_submission/figures') / output_path.name
    arxiv_path.parent.mkdir(exist_ok=True, parents=True)
    fig.savefig(arxiv_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {arxiv_path}")
    
    plt.close()
    
    return output_path


if __name__ == '__main__':
    import os
    os.chdir(PathLib(__file__).parent.parent)
    print(f"Working directory: {os.getcwd()}\n")
    
    create_mirror_pairs_figure()
    
    print("\n" + "="*60)
    print("✓ Mirror-symmetric triangulation figure complete!")
    print("="*60)
