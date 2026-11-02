#!/usr/bin/env python3
"""
Validate statistics consistency across all submission documents.
"""

import os
import re
from pathlib import Path

# Define the correct statistics
CORRECT_STATS = {
    'volume': {
        'mean': 84.053,
        'std': 7.141,
        'min': 58.0,
        'max': 97.333,
        'patterns': [
            r'84\.(?:053|1|05)',  # Allow slight variations
            r'7\.(?:141|1|14)',
            r'58\.0',
            r'97\.(?:333|3)'
        ]
    },
    'vertices': {
        'mean': 12.227,
        'std': 1.438,
        'min': 8.0,
        'max': 16.0,
        'patterns': [
            r'12\.(?:227|2|23)',
            r'1\.(?:438|4|44)',
            r'8\.0',
            r'16\.0'
        ]
    },
    'angular_uniformity': {
        'mean': 0.569,
        'std': 0.000,
        'patterns': [
            r'0\.569',
            r'0\.000'
        ]
    }
}

# Files to check
FILES_TO_CHECK = [
    'sections/abstract.tex',
    'sections/results.tex',
    'sections/discussion.tex',
    'sections/conclusion.tex',
    'sections/geometric_stats.tex',
    'cover_letter.md',
    'highlights.txt',
    'graphical_abstract.tex'
]


def check_file_statistics(filepath):
    """Check a file for statistical values."""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check for old incorrect values
    old_values = [
        (r'75\.888', 'old volume mean'),
        (r'7\.745', 'old volume std'),
        (r'46\.667', 'old volume min'),
        (r'94\.167', 'old volume max'),
        (r'12\.019', 'old vertices mean'),
        (r'1\.250', 'old vertices std'),
        (r'0\.535', 'old angular uniformity')
    ]
    
    for pattern, desc in old_values:
        if re.search(pattern, content):
            issues.append(f"Found incorrect {desc}: {pattern}")
    
    # Check for presence of correct values
    found_stats = {
        'volume': False,
        'vertices': False,
        'angular_uniformity': False
    }
    
    for stat_type, stat_info in CORRECT_STATS.items():
        for pattern in stat_info.get('patterns', []):
            if re.search(pattern, content):
                found_stats[stat_type] = True
                break
    
    # Report findings
    if issues:
        print(f"\n❌ {filepath}:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        missing = [k for k, v in found_stats.items() if not v and k in content.lower()]
        if missing:
            print(f"\n⚠️  {filepath}:")
            print(f"   - May be missing updated stats for: {', '.join(missing)}")
        else:
            print(f"✅ {filepath}: All statistics appear correct")
    
    return len(issues) == 0


def validate_all_files():
    """Validate all files in the submission."""
    print("=" * 70)
    print("VALIDATING STATISTICS IN SUBMISSION FILES")
    print("=" * 70)
    
    base_dir = Path(__file__).parent
    all_valid = True
    
    for file_path in FILES_TO_CHECK:
        full_path = base_dir / file_path
        if not check_file_statistics(full_path):
            all_valid = False
    
    print("\n" + "=" * 70)
    if all_valid:
        print("✅ ALL FILES HAVE CORRECT STATISTICS!")
    else:
        print("❌ SOME FILES NEED ATTENTION")
    print("=" * 70)
    
    # Summary of correct values
    print("\nCORRECT VALUES FOR REFERENCE:")
    print("-" * 30)
    print(f"Volume: {CORRECT_STATS['volume']['mean']} ± {CORRECT_STATS['volume']['std']}")
    print(f"        (range: {CORRECT_STATS['volume']['min']}-{CORRECT_STATS['volume']['max']})")
    print(f"Vertices: {CORRECT_STATS['vertices']['mean']} ± {CORRECT_STATS['vertices']['std']}")
    print(f"Angular uniformity: {CORRECT_STATS['angular_uniformity']['mean']} ± {CORRECT_STATS['angular_uniformity']['std']}")
    
    return all_valid


if __name__ == '__main__':
    validate_all_files() 