"""
Classical Classification of 4x4 Magic Squares
==============================================

This module classifies the 880 unique 4x4 magic squares according to
well-established categories in the magic square literature:

1. Associative (Self-Complementary): M[i,j] + M[3-i,3-j] = 17 for all cells
2. Pandiagonal: All broken diagonals also sum to 34
3. Semi-Pandiagonal: Some but not all broken diagonals sum to 34
4. D4 Symmetry: Squares with non-trivial self-symmetry

References:
- Dudeney, H.E. (1917). Amusements in Mathematics
- Ollerenshaw & Brée (1998). Most-Perfect Pandiagonal Magic Squares

Author: Kyle Elliott Mathewson
"""

import numpy as np
import json
import os
from typing import List, Tuple, Dict


def load_880_squares():
    """Load the 880 unique magic squares."""
    json_path = os.path.join(os.path.dirname(__file__), '..', 'web', 'assets', 'data', 'unique_squares.json')
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    squares = [np.array(s).reshape(4, 4) if len(np.array(s).shape) == 1 else np.array(s) 
               for s in data]
    return squares


def is_associative(square: np.ndarray) -> bool:
    """
    Check if a 4x4 magic square is associative (self-complementary).
    
    An associative square has the property that each pair of cells
    symmetrically opposite to the center sum to n² + 1 = 17.
    
    For a 4x4 square: M[i,j] + M[3-i,3-j] = 17 for all i,j
    """
    n = 4
    for i in range(n):
        for j in range(n):
            if square[i, j] + square[n-1-i, n-1-j] != 17:
                return False
    return True


def is_pandiagonal(square: np.ndarray) -> bool:
    """
    Check if a 4x4 magic square is pandiagonal.
    
    A pandiagonal square has all broken diagonals summing to 34.
    There are 4 broken diagonals in each direction (8 total).
    """
    n = 4
    target = 34
    
    # Check all broken diagonals (wrapping)
    for offset in range(n):
        # Main direction broken diagonals
        diag1 = sum(square[i, (i + offset) % n] for i in range(n))
        if diag1 != target:
            return False
        
        # Anti-diagonal direction broken diagonals
        diag2 = sum(square[i, (n - 1 - i + offset) % n] for i in range(n))
        if diag2 != target:
            return False
    
    return True


def count_valid_broken_diagonals(square: np.ndarray) -> int:
    """Count how many broken diagonals sum to 34."""
    n = 4
    target = 34
    count = 0
    
    for offset in range(n):
        diag1 = sum(square[i, (i + offset) % n] for i in range(n))
        if diag1 == target:
            count += 1
        
        diag2 = sum(square[i, (n - 1 - i + offset) % n] for i in range(n))
        if diag2 == target:
            count += 1
    
    return count


def get_d4_transformations(square: np.ndarray) -> List[np.ndarray]:
    """Get all 8 D4 transformations of a square."""
    transforms = [square.copy()]
    
    # Rotations
    for k in range(1, 4):
        transforms.append(np.rot90(square, k))
    
    # Reflections
    flipped = np.fliplr(square)
    transforms.append(flipped.copy())
    for k in range(1, 4):
        transforms.append(np.rot90(flipped, k))
    
    return transforms


def has_self_symmetry(square: np.ndarray) -> Tuple[bool, List[str]]:
    """
    Check if a square has non-trivial D4 self-symmetry.
    
    Returns (has_symmetry, list_of_symmetries)
    """
    symmetries = []
    
    # Check rotation symmetries
    for k in range(1, 4):
        if np.array_equal(square, np.rot90(square, k)):
            symmetries.append(f"R{k*90}")
    
    # Check reflection symmetries
    if np.array_equal(square, np.fliplr(square)):
        symmetries.append("H-flip")
    if np.array_equal(square, np.flipud(square)):
        symmetries.append("V-flip")
    if np.array_equal(square, square.T):
        symmetries.append("diag-flip")
    if np.array_equal(square, np.rot90(np.fliplr(square), 2)):
        symmetries.append("anti-diag-flip")
    
    return len(symmetries) > 0, symmetries


def check_2x2_subsquares(square: np.ndarray) -> bool:
    """
    Check if all 2x2 subsquares sum to 34.
    This is a property of "most-perfect" pandiagonal squares.
    """
    target = 34
    for i in range(4):
        for j in range(4):
            subsquare_sum = (square[i, j] + square[i, (j+1)%4] + 
                           square[(i+1)%4, j] + square[(i+1)%4, (j+1)%4])
            if subsquare_sum != target:
                return False
    return True


def classify_all_squares(squares: List[np.ndarray]) -> Dict:
    """
    Classify all 880 magic squares according to classical categories.
    """
    results = {
        'total': len(squares),
        'associative': [],
        'pandiagonal': [],
        'semi_pandiagonal': [],  # Some but not all broken diags work
        'has_self_symmetry': [],
        'most_perfect': [],  # Pandiagonal + all 2x2 subsquares sum to 34
        'simple': [],  # None of the above special properties
    }
    
    for idx, sq in enumerate(squares):
        is_assoc = is_associative(sq)
        is_pand = is_pandiagonal(sq)
        n_broken = count_valid_broken_diagonals(sq)
        has_sym, sym_list = has_self_symmetry(sq)
        is_most_perfect = is_pand and check_2x2_subsquares(sq)
        
        if is_assoc:
            results['associative'].append(idx)
        if is_pand:
            results['pandiagonal'].append(idx)
        if is_most_perfect:
            results['most_perfect'].append(idx)
        if has_sym:
            results['has_self_symmetry'].append((idx, sym_list))
        if 2 < n_broken < 8:  # Some but not all
            results['semi_pandiagonal'].append((idx, n_broken))
        
        # Simple = not associative and not pandiagonal
        if not is_assoc and not is_pand:
            results['simple'].append(idx)
    
    return results


def print_classification_report(results: Dict):
    """Print a formatted classification report."""
    print("=" * 60)
    print("CLASSICAL CLASSIFICATION OF 4×4 MAGIC SQUARES")
    print("=" * 60)
    print(f"\nTotal unique squares: {results['total']}")
    print("\n--- Category Breakdown ---\n")
    
    print(f"Associative (self-complementary): {len(results['associative'])}")
    print(f"  • Pairs symmetric about center sum to 17")
    
    print(f"\nPandiagonal (diabolic): {len(results['pandiagonal'])}")
    print(f"  • All broken diagonals also sum to 34")
    
    print(f"\nMost-Perfect: {len(results['most_perfect'])}")
    print(f"  • Pandiagonal + all 2×2 subsquares sum to 34")
    
    print(f"\nSemi-Pandiagonal: {len(results['semi_pandiagonal'])}")
    print(f"  • Some but not all broken diagonals sum to 34")
    
    print(f"\nWith D4 Self-Symmetry: {len(results['has_self_symmetry'])}")
    if results['has_self_symmetry']:
        sym_types = {}
        for idx, syms in results['has_self_symmetry']:
            for s in syms:
                sym_types[s] = sym_types.get(s, 0) + 1
        for s, count in sorted(sym_types.items()):
            print(f"    {s}: {count}")
    
    print(f"\nSimple (no special properties): {len(results['simple'])}")
    
    # Check overlaps
    print("\n--- Overlaps ---\n")
    assoc_set = set(results['associative'])
    pand_set = set(results['pandiagonal'])
    both = assoc_set & pand_set
    print(f"Both Associative AND Pandiagonal: {len(both)}")
    
    # Verify totals
    only_assoc = len(assoc_set - pand_set)
    only_pand = len(pand_set - assoc_set)
    neither = len(results['simple'])
    total_check = only_assoc + only_pand + len(both) + neither
    print(f"\nVerification: {only_assoc} + {only_pand} + {len(both)} + {neither} = {total_check}")


def get_hull_configuration(square: np.ndarray) -> str:
    """Get the convex hull configuration (v, f, i) for a magic square."""
    from scipy.spatial import ConvexHull
    
    # Embed in R3
    points = []
    for i in range(4):
        for j in range(4):
            points.append([i, j, square[i, j]])
    points = np.array(points)
    
    # Compute hull
    hull = ConvexHull(points)
    n_vertices = len(hull.vertices)
    
    # Classify remaining points
    vertex_set = set(hull.vertices)
    n_face = 0
    n_interior = 0
    
    for idx, pt in enumerate(points):
        if idx in vertex_set:
            continue
        
        # Check if on any face
        on_face = False
        for eq in hull.equations:
            dist = abs(np.dot(eq[:-1], pt) + eq[-1])
            if dist < 1e-10:
                on_face = True
                break
        
        if on_face:
            n_face += 1
        else:
            n_interior += 1
    
    return f"{n_vertices}v_{n_face}f_{n_interior}i"


def cross_tabulate_with_hull(squares: List[np.ndarray], classical_results: Dict) -> Dict:
    """Cross-tabulate classical classification with hull configurations."""
    print("\nComputing hull configurations for all squares...")
    
    hull_configs = [get_hull_configuration(sq) for sq in squares]
    
    # Count overall distribution
    config_counts = {}
    for cfg in hull_configs:
        config_counts[cfg] = config_counts.get(cfg, 0) + 1
    
    # Cross-tabulate with classical categories
    cross_tab = {
        'pandiagonal': {},
        'associative': {},
        'simple': {}
    }
    
    for idx in classical_results['pandiagonal']:
        cfg = hull_configs[idx]
        cross_tab['pandiagonal'][cfg] = cross_tab['pandiagonal'].get(cfg, 0) + 1
    
    for idx in classical_results['associative']:
        cfg = hull_configs[idx]
        cross_tab['associative'][cfg] = cross_tab['associative'].get(cfg, 0) + 1
    
    for idx in classical_results['simple']:
        cfg = hull_configs[idx]
        cross_tab['simple'][cfg] = cross_tab['simple'].get(cfg, 0) + 1
    
    return {
        'overall': config_counts,
        'cross_tab': cross_tab,
        'hull_configs': hull_configs
    }


def print_cross_tabulation(hull_results: Dict, classical_results: Dict):
    """Print cross-tabulation results."""
    print("\n" + "=" * 60)
    print("CROSS-TABULATION: Classical × Geometric Classification")
    print("=" * 60)
    
    # Overall configuration distribution
    print("\n--- All 880 Squares: Hull Configuration Distribution ---\n")
    sorted_configs = sorted(hull_results['overall'].items(), 
                           key=lambda x: -x[1])
    for cfg, count in sorted_configs:
        pct = 100 * count / 880
        print(f"  {cfg}: {count} ({pct:.1f}%)")
    
    print(f"\nTotal distinct configurations: {len(hull_results['overall'])}")
    
    # Pandiagonal squares
    print("\n--- 48 Pandiagonal Squares: Hull Configurations ---\n")
    pand_configs = hull_results['cross_tab']['pandiagonal']
    for cfg, count in sorted(pand_configs.items(), key=lambda x: -x[1]):
        print(f"  {cfg}: {count}")
    
    # Associative squares  
    print("\n--- 48 Associative Squares: Hull Configurations ---\n")
    assoc_configs = hull_results['cross_tab']['associative']
    for cfg, count in sorted(assoc_configs.items(), key=lambda x: -x[1]):
        print(f"  {cfg}: {count}")
    
    # Simple squares
    print("\n--- 784 Simple Squares: Hull Configurations ---\n")
    simple_configs = hull_results['cross_tab']['simple']
    sorted_simple = sorted(simple_configs.items(), key=lambda x: -x[1])[:10]
    for cfg, count in sorted_simple:
        print(f"  {cfg}: {count}")
    print(f"  ... and {len(simple_configs) - 10} more configurations")


if __name__ == '__main__':
    print("Loading 880 unique magic squares...")
    squares = load_880_squares()
    print(f"Loaded {len(squares)} squares")
    
    print("\nClassifying squares (classical)...")
    results = classify_all_squares(squares)
    
    print_classification_report(results)
    
    # Cross-tabulate with geometric classification
    hull_results = cross_tabulate_with_hull(squares, results)
    print_cross_tabulation(hull_results, results)
    
    # Print some example pandiagonal squares
    if results['pandiagonal']:
        print("\n--- Example Pandiagonal Square ---")
        idx = results['pandiagonal'][0]
        print(squares[idx])
    
    # Print example associative square
    if results['associative']:
        print("\n--- Example Associative Square ---")
        idx = results['associative'][0]
        sq = squares[idx]
        print(sq)
        print(f"\nVerifying pairs sum to 17:")
        for i in range(2):
            for j in range(4):
                print(f"  ({i},{j}) + ({3-i},{3-j}): {sq[i,j]} + {sq[3-i,3-j]} = {sq[i,j] + sq[3-i,3-j]}")

