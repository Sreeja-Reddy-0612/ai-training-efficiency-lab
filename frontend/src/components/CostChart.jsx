import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

function CostChart({ data }) {
  return (
    <div>
      <h3>Cost Comparison</h3>
      <BarChart width={400} height={300} data={data}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="experiment_id" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="estimated_cost" fill="#82ca9d" />
      </BarChart>
    </div>
  );
}

export default CostChart;
