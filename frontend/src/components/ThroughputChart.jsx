import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

function ThroughputChart({ data }) {
  return (
    <div>
      <h3>Throughput Comparison</h3>
      <LineChart width={400} height={300} data={data}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="experiment_id" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="throughput_samples_per_sec" stroke="#8884d8" />
      </LineChart>
    </div>
  );
}

export default ThroughputChart;
