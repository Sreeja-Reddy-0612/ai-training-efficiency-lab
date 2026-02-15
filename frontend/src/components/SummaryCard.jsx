function SummaryCard({ data }) {
  return (
    <div style={{
      background: "#f4f4f4",
      padding: "20px",
      borderRadius: "10px",
      marginTop: "20px"
    }}>
      <h2>Best Experiment</h2>
      <p><b>Experiment ID:</b> {data.experiment_id}</p>
      <p><b>Throughput:</b> {data.throughput_samples_per_sec} samples/sec</p>
      <p><b>Total Time:</b> {data.total_time_seconds} sec</p>
      <p><b>Estimated Cost:</b> ${data.estimated_cost}</p>
      <p><b>Device:</b> {data.device}</p>
    </div>
  );
}

export default SummaryCard;
