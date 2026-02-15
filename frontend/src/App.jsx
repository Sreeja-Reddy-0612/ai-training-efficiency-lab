import { useEffect, useState } from "react";
import { fetchLatest, fetchHistory } from "./services/api";
import SummaryCard from "./components/SummaryCard";
import ThroughputChart from "./components/ThroughputChart";
import CostChart from "./components/CostChart";
import BenchmarkTable from "./components/BenchmarkTable";
import DecisionInsights from "./components/DecisionInsights";
import sampleData from "./data/sampleData.json";

function App() {
  const [latest, setLatest] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    async function loadData() {
      const latestData = await fetchLatest();
      const historyData = await fetchHistory();

      setLatest(latestData);
      setHistory(historyData);
    }

    loadData();
  }, []);

  if (!latest) return <h2>Loading Dashboard...</h2>;

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1 style={{ marginBottom: "30px" }}>
        AI Training Efficiency Dashboard 🚀
      </h1>

      {/* Summary */}
      <SummaryCard data={latest} />

      {/* Charts Side by Side */}
      <div
        style={{
          display: "flex",
          gap: "30px",
          marginTop: "40px",
          flexWrap: "wrap",
        }}
      >
        <div style={{ flex: 1, minWidth: "400px" }}>
          <ThroughputChart data={history} />
        </div>

        <div style={{ flex: 1, minWidth: "400px" }}>
          <CostChart data={history} />
        </div>
      </div>

      {/* Table + Intelligence Side by Side */}
      <div
        style={{
          display: "flex",
          gap: "30px",
          marginTop: "50px",
          alignItems: "flex-start",
          flexWrap: "wrap",
        }}
      >
        <div style={{ flex: 2, minWidth: "500px" }}>
          <BenchmarkTable data={history} />
        </div>

        <div style={{ flex: 1, minWidth: "500px" }}>
          <DecisionInsights history={sampleData.history} />
        </div>
      </div>
    </div>
  );
}

export default App;
