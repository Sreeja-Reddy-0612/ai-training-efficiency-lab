import { useEffect, useState } from "react";
import { fetchLatest, fetchHistory } from "./services/api";
import SummaryCard from "./components/SummaryCard";
import ThroughputChart from "./components/ThroughputChart";
import CostChart from "./components/CostChart";
import BenchmarkTable from "./components/BenchmarkTable";
import DecisionInsights from "./components/DecisionInsights";

function App() {
  const [latest, setLatest] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        const latestData = await fetchLatest();
        const historyData = await fetchHistory();

        setLatest(latestData);
        setHistory(historyData);
      } catch (error) {
        console.error("Error loading data:", error);
      }
    }

    loadData();
  }, []);

  if (!latest) return <h2>Loading Dashboard...</h2>;

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>AI Training Efficiency Dashboard 🚀</h1>

      <SummaryCard data={latest} />

      {/* Charts side by side */}
      <div style={{ display: "flex", gap: "40px" }}>
        <ThroughputChart data={history} />
        <CostChart data={history} />
      </div>

      {/* Table + Decision side by side */}
      <div style={{ display: "flex", gap: "40px", marginTop: "40px" }}>
        <BenchmarkTable data={history} />
        <DecisionInsights history={history} />
      </div>
    </div>
  );
}

export default App;
