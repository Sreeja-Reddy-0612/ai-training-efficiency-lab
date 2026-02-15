import React from "react";

function DecisionInsights({ history }) {
  if (!history || history.length === 0) {
    return <p>No data available</p>;
  }

  const sortedByThroughput = [...history].sort(
    (a, b) => b.throughput_samples_per_sec - a.throughput_samples_per_sec
  );

  const best = sortedByThroughput[0];

  const cpuRuns = history.filter(h => h.device.includes("cpu"));
  const gpuRuns = history.filter(h => h.device.includes("cuda"));

  const avgCPU =
    cpuRuns.reduce((acc, val) => acc + val.throughput_samples_per_sec, 0) /
    (cpuRuns.length || 1);

  const avgGPU =
    gpuRuns.reduce((acc, val) => acc + val.throughput_samples_per_sec, 0) /
    (gpuRuns.length || 1);

  const speedup = avgGPU / (avgCPU || 1);

  return (
    <div style={{ background: "#f5f5f5", padding: "20px", marginTop: "30px", borderRadius: "8px" }}>
      <h2>Decision Intelligence</h2>

      <p><strong>🏆 Recommended Setup:</strong></p>
      <ul>
        <li>Experiment: {best.experiment_id}</li>
        <li>Device: {best.device}</li>
        <li>Throughput: {best.throughput_samples_per_sec} samples/sec</li>
      </ul>

      <p><strong>⚡ GPU Speedup vs CPU:</strong> {speedup.toFixed(2)}x faster</p>

      <p><strong>💡 Optimization Insight:</strong></p>
      <ul>
        {best.mixed_precision && <li>Mixed precision improves performance significantly.</li>}
        {best.distributed && <li>Distributed training provides additional scaling benefits.</li>}
        {!best.mixed_precision && <li>Consider enabling mixed precision.</li>}
      </ul>
    </div>
  );
}

export default DecisionInsights;
