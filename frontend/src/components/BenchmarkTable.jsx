function BenchmarkTable({ data }) {
  return (
    <div style={{ marginTop: "50px" }}>
      <h2>Benchmark History</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>ID</th>
            <th>Device</th>
            <th>Batch</th>
            <th>Throughput</th>
            <th>Time</th>
            <th>Cost</th>
          </tr>
        </thead>
        <tbody>
          {data.map((exp, index) => (
            <tr key={index}>
              <td>{exp.experiment_id}</td>
              <td>{exp.device}</td>
              <td>{exp.batch_size}</td>
              <td>{exp.throughput_samples_per_sec}</td>
              <td>{exp.total_time_seconds}</td>
              <td>${exp.estimated_cost}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BenchmarkTable;
