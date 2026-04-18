import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { setInteractions, setSearchResults } from "./interactionSlice";

function App() {
  const dispatch = useDispatch();

  const { data = [], searchResults = [] } = useSelector(
    (state) => state.interaction
  );

  const [searchText, setSearchText] = useState("");
  const [activePage, setActivePage] = useState("dashboard");
  const [chatInput, setChatInput] = useState("");
  const [aiResponse, setAiResponse] = useState(null);

  const loadHistory = useCallback(async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/interaction/history"
      );
      dispatch(setInteractions(res.data.history || []));
    } catch (error) {
      console.error("History load failed:", error);
    }
  }, [dispatch]);

  const submitToAgent = async () => {
    try {
      if (!chatInput.trim()) {
        alert("Please enter interaction notes");
        return;
      }

      const response = await axios.post(
        "http://127.0.0.1:8000/interaction/ai-log",
        {
          text: chatInput,
        }
      );

      setAiResponse(response.data);

      await loadHistory();

      setChatInput("");
      setActivePage("interactions");
    } catch (error) {
      console.error(error);
      alert("AI logging failed");
    }
  };

  const searchInteraction = async () => {
    try {
      const keyword = searchText.trim();

      if (!keyword) {
        alert("Please enter search text");
        return;
      }

      const response = await fetch(
        `http://127.0.0.1:8000/interaction/search?keyword=${encodeURIComponent(
          keyword
        )}`
      );

      if (!response.ok) {
        throw new Error("Search API failed");
      }

      const result = await response.json();

      dispatch(setSearchResults(result.results || []));
      setActivePage("search");
    } catch (error) {
      console.error(error);
      alert("Search failed");
    }
  };

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const renderPage = () => {
    if (activePage === "dashboard") {
      return (
        <>
          <h1 style={pageTitle}>Medical CRM Dashboard</h1>

          <div style={cardsWrapper}>
            <div style={premiumCard}>
              <p>Total Interactions</p>
              <h2>{data.length}</h2>
            </div>

            <div style={premiumCard}>
              <p>Doctors Connected</p>
              <h2>{data.length}</h2>
            </div>

            <div style={premiumCard}>
              <p>AI Logs Processed</p>
              <h2>{data.length}</h2>
            </div>
          </div>

          <div style={chartCard}>
            <h3>Interaction Trend</h3>
            <div style={barWrapper}>
              <div style={{ ...barStyle, height: "70px" }} />
              <div style={{ ...barStyle, height: "120px" }} />
              <div style={{ ...barStyle, height: "90px" }} />
              <div style={{ ...barStyle, height: "140px" }} />
              <div style={{ ...barStyle, height: "110px" }} />
            </div>
          </div>
        </>
      );
    }

    if (activePage === "interactions") {
      return (
        <>
          <h1 style={pageTitle}>Recent Interactions</h1>

          {data.map((item) => (
            <div key={item.id} style={historyCard}>
              <p><b>ID:</b> {item.id}</p>
              <p><b>Notes:</b> {item.notes}</p>
              <p><b>Summary:</b> {item.summary}</p>
            </div>
          ))}
        </>
      );
    }

    if (activePage === "search") {
      return (
        <>
          <h1 style={pageTitle}>Search Results</h1>

          {searchResults.length === 0 ? (
            <p>No matching interactions found</p>
          ) : (
            searchResults.map((item) => (
              <div key={item.id} style={historyCard}>
                <p><b>ID:</b> {item.id}</p>
                <p><b>Notes:</b> {item.notes}</p>
                <p><b>Summary:</b> {item.summary}</p>
              </div>
            ))
          )}
        </>
      );
    }

    if (activePage === "analytics") {
      return (
        <div style={chartCard}>
          <h1 style={pageTitle}>Analytics</h1>
          <p>Total Logs Processed: {data.length}</p>
        </div>
      );
    }

    if (activePage === "doctors") {
      return (
        <>
          <h1 style={pageTitle}>Doctors List</h1>

          {data.map((item) => (
            <div key={item.id} style={historyCard}>
              <p>{item.notes}</p>
            </div>
          ))}
        </>
      );
    }

    if (activePage === "chat") {
      return (
        <>
          <h1 style={pageTitle}>AI Chat Logger</h1>

          <textarea
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            rows="6"
            style={textareaStyle}
            placeholder="Enter doctor interaction notes..."
          />

          <button style={buttonStyle} onClick={submitToAgent}>
            Submit to AI Agent
          </button>

          {aiResponse && (
            <div style={historyCard}>
              <h3>AI Response</h3>
              <pre>{JSON.stringify(aiResponse, null, 2)}</pre>
            </div>
          )}
        </>
      );
    }
  };

  return (
    <div style={layoutStyle}>
      <div style={sidebarStyle}>
        <h2 style={{ color: "white" }}>MedConnect AI</h2>

        <p style={menuStyle} onClick={() => setActivePage("dashboard")}>
          Dashboard
        </p>

        <p style={menuStyle} onClick={() => setActivePage("interactions")}>
          Interactions
        </p>

        <p style={menuStyle} onClick={() => setActivePage("analytics")}>
          Analytics
        </p>

        <p style={menuStyle} onClick={() => setActivePage("doctors")}>
          Doctors
        </p>

        <p style={menuStyle} onClick={() => setActivePage("chat")}>
          AI Chat Logger
        </p>
      </div>

      <div style={mainContentStyle}>
        <div style={searchBoxStyle}>
          <input
            type="text"
            placeholder="Search doctor / notes..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            style={inputStyle}
          />

          <button style={buttonStyle} onClick={searchInteraction}>
            Search
          </button>
        </div>

        {renderPage()}
      </div>
    </div>
  );
}

const layoutStyle = {
  display: "flex",
  minHeight: "100vh",
  fontFamily: "Inter, sans-serif",
  background: "#f3f7fb",
};

const sidebarStyle = {
  width: "250px",
  background: "#0a4fa3",
  padding: "30px",
  color: "white",
};

const menuStyle = {
  marginTop: "24px",
  cursor: "pointer",
  fontSize: "16px",
};

const mainContentStyle = {
  flex: 1,
  padding: "30px",
};

const pageTitle = {
  marginBottom: "20px",
};

const cardsWrapper = {
  display: "flex",
  gap: "20px",
  marginBottom: "30px",
};

const premiumCard = {
  flex: 1,
  background: "white",
  padding: "24px",
  borderRadius: "16px",
  boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
};

const chartCard = {
  background: "white",
  padding: "24px",
  borderRadius: "16px",
  marginTop: "20px",
};

const barWrapper = {
  display: "flex",
  gap: "16px",
  alignItems: "flex-end",
  height: "180px",
};

const barStyle = {
  width: "40px",
  background: "#0a4fa3",
  borderRadius: "8px",
};

const searchBoxStyle = {
  display: "flex",
  gap: "10px",
  marginBottom: "30px",
};

const inputStyle = {
  width: "350px",
  padding: "14px",
  borderRadius: "10px",
  border: "1px solid #ddd",
};

const buttonStyle = {
  background: "#0a4fa3",
  color: "white",
  border: "none",
  padding: "14px 24px",
  borderRadius: "10px",
  cursor: "pointer",
  marginTop: "10px",
};

const textareaStyle = {
  width: "100%",
  padding: "16px",
  borderRadius: "12px",
  minHeight: "150px",
};

const historyCard = {
  background: "white",
  padding: "18px",
  borderRadius: "14px",
  marginTop: "20px",
  boxShadow: "0 4px 10px rgba(0,0,0,0.06)",
};

export default App;