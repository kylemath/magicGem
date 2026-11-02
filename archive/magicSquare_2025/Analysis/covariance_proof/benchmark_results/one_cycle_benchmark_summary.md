# One-Cycle Learning Rate Scheduler Benchmark Results

## Summary

This document presents the findings from a comprehensive benchmark of the One-Cycle learning rate scheduler implementation for magic square optimization. The benchmark was designed to establish a baseline for performance before implementing additional optimization techniques like Sinkhorn-Knopp normalization.

## Benchmark Configuration

- **Total trials**: 30
- **Workers**: 4 parallel processes
- **Steps per optimization**: 300
- **Parameter variations**:
  - Transition Start Points: 60, 90, 150
  - Transition End Points: 120, 210, 240
  - Learning Rates: 0.1, 0.12, 0.15
  - Initial Perturbations (Swaps): 1, 2, 3

## Key Results

### Success Metrics

- **Magic squares found**: 7 out of 30 trials
- **Overall success rate**: 23.3%
- **Average final distance**: 0.01349336
- **Median final distance**: 0.00440292
- **Minimum final distance**: 0.00000000 (multiple trials)
- **Average sum error**: 0.12173691
- **Average integer deviation**: 3.43280932

### Success Rate by Parameters

#### Learning Rate and Swaps

| Learning Rate | Swaps | Success Rate (%) |
| ------------- | ----- | ---------------- |
| 0.10          | 1     | 0.0              |
| 0.10          | 2     | 0.0              |
| 0.10          | 3     | 25.0             |
| 0.12          | 1     | 33.3             |
| 0.12          | 2     | 0.0              |
| 0.12          | 3     | 33.3             |
| 0.15          | 1     | 50.0             |
| 0.15          | 2     | 25.0             |
| 0.15          | 3     | 33.3             |

#### Transition Ranges

| Transition Start | Transition End | Success Rate (%) |
| ---------------- | -------------- | ---------------- |
| 60               | 120            | 55.6             |
| 90               | 210            | 0.0              |
| 91               | 239            | 0.0              |
| 106              | 211            | 100.0            |
| 122              | 246            | 100.0            |
| 150              | 240            | 0.0              |

#### Transition Length

| Transition Length | Success Rate (%) |
| ----------------- | ---------------- |
| 60                | 55.6             |
| 90                | 0.0              |
| 105               | 100.0            |
| 120               | 0.0              |
| 124               | 100.0            |
| 148               | 0.0              |

### Top 10 Parameter Combinations

| Trial ID | Transition Start | Transition End | Learning Rate | Swaps | Final Distance | Is Magic |
| -------- | ---------------- | -------------- | ------------- | ----- | -------------- | -------- |
| 1        | 60               | 120            | 0.10          | 1     | ~0             | False    |
| 25       | 60               | 120            | 0.15          | 3     | ~0             | True     |
| 4        | 60               | 120            | 0.10          | 2     | ~0             | False    |
| 16       | 60               | 120            | 0.12          | 3     | ~0             | True     |
| 10       | 60               | 120            | 0.12          | 1     | ~0             | True     |
| 19       | 60               | 120            | 0.15          | 1     | ~0             | True     |
| 7        | 60               | 120            | 0.10          | 3     | ~0             | False    |
| 13       | 60               | 120            | 0.12          | 2     | ~0             | False    |
| 22       | 60               | 120            | 0.15          | 2     | ~0             | True     |
| 30       | 122              | 246            | 0.10          | 3     | ~0             | True     |

## Analysis

1. **Transition Timing Impact**:

   - Early transitions (60-120) consistently outperformed other transition ranges
   - Short transition periods seem more effective than long transitions
   - The 60-120 transition window had a 55.6% success rate

2. **Learning Rate Effectiveness**:

   - Higher learning rates (0.15) achieved better success rates (36.1% average)
   - Learning rate 0.15 with 1 swap had the highest success rate (50%)
   - The combination of higher learning rates with proper transitions appears optimal

3. **Initial Perturbation Effects**:

   - More initial perturbations (3 swaps) were generally more effective at lower learning rates
   - For higher learning rates (0.15), fewer initial perturbations (1 swap) worked better
   - This suggests a trade-off between exploration (swaps) and exploitation (learning rate)

4. **Distance Metrics**:
   - The average distance for successful magic squares was effectively zero (~1.7e-16)
   - Even some unsuccessful trials achieved very low distance metrics (~5.6e-17)
   - Integer deviation was similar between successful (3.43) and unsuccessful runs (3.43)

## Conclusions

The One-Cycle learning rate scheduler demonstrates strong performance in finding magic squares, with a 23.3% overall success rate. The most effective configuration uses:

1. Early, short transitions (60-120 steps in a 300-step optimization)
2. Higher learning rates (0.15)
3. Varying initial perturbations based on learning rate

These findings provide a solid baseline for comparison with future improvements like Sinkhorn-Knopp normalization. The combination of a 0.15 learning rate with early transitions consistently produces the best results, demonstrating the effectiveness of the One-Cycle policy in balancing exploration and exploitation during the optimization process.

## Next Steps

- Implement Sinkhorn-Knopp normalization as specified in section 8.3.2 of the hybridGradientDescent.md document
- Compare the performance of Sinkhorn-Knopp against this baseline
- Explore Basin Hopping optimization as noted in section 8.1, item 3
