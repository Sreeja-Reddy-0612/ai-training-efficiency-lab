# Decision Intelligence Engine – Explanation

The DecisionInsights component analyzes historical benchmark data.

## Steps Performed:

1. Sort experiments by throughput
2. Identify highest performing configuration
3. Separate CPU and GPU runs
4. Compute average throughput
5. Calculate GPU speedup vs CPU
6. Generate optimization suggestions

## Example

If:

CPU Avg Throughput = 1.8 samples/sec
GPU Avg Throughput = 124 samples/sec

Then:

Speedup = 124 / 1.8 = 68.8x

## Output

- Recommended experiment ID
- Device used
- Throughput
- Speedup factor
- Suggestions for improvement

This simulates real-world AI infra optimization systems.
