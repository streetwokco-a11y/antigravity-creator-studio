"use client";

import { useEffect, useState } from "react";

interface Lead {
  id: number;
  name: string;
  company: string;
  email: string;
  budget: number;
  score: number;
  status: string;
  createdAt: string;
}

export default function DashboardPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [triaging, setTriaging] = useState<boolean>(false);
  const [name, setName] = useState("");
  const [company, setCompany] = useState("");
  const [email, setEmail] = useState("");
  const [budget, setBudget] = useState(3500);

  const fetchLeads = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/leads");
      if (res.ok) {
        const data = await res.json();
        setLeads(data);
      }
    } catch (err) {
      console.error("Failed to load leads from FastAPI backend:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  const handleCreateLead = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, company, email, budget: Number(budget) }),
      });
      if (res.ok) {
        setName("");
        setCompany("");
        setEmail("");
        fetchLeads();
      }
    } catch (err) {
      console.error("Error creating lead:", err);
    }
  };

  const handleRunTriage = async () => {
    setTriaging(true);
    try {
      const res = await fetch("http://localhost:8000/api/triage/execute", {
        method: "POST",
      });
      if (res.ok) {
        await fetchLeads();
      }
    } catch (err) {
      console.error("Error executing triage:", err);
    } finally {
      setTriaging(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        <header className="flex justify-between items-center border-b border-slate-800 pb-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white">
              Autonomous Lead Triage Engine
            </h1>
            <p className="text-slate-400 mt-1">
              Next.js 15 Client &bull; FastAPI Backend &bull; SQLite Database
            </p>
          </div>
          <button
            onClick={handleRunTriage}
            disabled={triaging}
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-semibold rounded-lg shadow-lg shadow-emerald-950 transition-all cursor-pointer"
          >
            {triaging ? "Processing Triage..." : "Run AI Triage Engine"}
          </button>
        </header>

        {/* Ingestion Form */}
        <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <h2 className="text-lg font-semibold text-slate-200 mb-4">
            Ingest Direct Lead
          </h2>
          <form onSubmit={handleCreateLead} className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <input
              type="text"
              placeholder="Full Name"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-500"
            />
            <input
              type="text"
              placeholder="Company"
              required
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-500"
            />
            <input
              type="email"
              placeholder="Work Email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-500"
            />
            <div className="flex gap-2">
              <input
                type="number"
                placeholder="Budget ($)"
                required
                value={budget}
                onChange={(e) => setBudget(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-500"
              />
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 font-semibold rounded-lg text-white"
              >
                Add
              </button>
            </div>
          </form>
        </section>

        {/* Live Data Grid */}
        <section className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
          <div className="px-6 py-4 border-b border-slate-800 flex justify-between items-center">
            <h2 className="text-lg font-semibold text-slate-200">
              Ingested Leads Database ({leads.length})
            </h2>
            <button
              onClick={fetchLeads}
              className="text-xs text-slate-400 hover:text-white underline cursor-pointer"
            >
              Refresh Table
            </button>
          </div>

          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 font-medium">
              <tr>
                <th className="px-6 py-3">ID</th>
                <th className="px-6 py-3">Lead</th>
                <th className="px-6 py-3">Company</th>
                <th className="px-6 py-3">Budget</th>
                <th className="px-6 py-3">Score</th>
                <th className="px-6 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {leads.map((lead) => (
                <tr key={lead.id} className="hover:bg-slate-800/40 transition">
                  <td className="px-6 py-4 font-mono text-slate-500">#{lead.id}</td>
                  <td className="px-6 py-4 font-medium text-white">{lead.name}</td>
                  <td className="px-6 py-4">{lead.company}</td>
                  <td className="px-6 py-4 font-mono">${lead.budget.toLocaleString()}</td>
                  <td className="px-6 py-4 font-bold">
                    <span
                      className={
                        lead.score >= 80
                          ? "text-emerald-400"
                          : lead.score >= 50
                          ? "text-amber-400"
                          : "text-slate-500"
                      }
                    >
                      {lead.score}/100
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        lead.status === "QUALIFIED"
                          ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                          : lead.status === "DISQUALIFIED"
                          ? "bg-rose-950 text-rose-400 border border-rose-800"
                          : "bg-slate-800 text-slate-300"
                      }`}
                    >
                      {lead.status}
                    </span>
                  </td>
                </tr>
              ))}
              {leads.length === 0 && !loading && (
                <tr>
                  <td colSpan={6} className="text-center py-8 text-slate-500">
                    No leads in database. Use the ingestion form above to add one.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </section>
      </div>
    </main>
  );
}
