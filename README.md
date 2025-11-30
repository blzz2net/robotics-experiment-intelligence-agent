
# **Robotics Experiment Intelligence Agent**

A modular multi-agent system that automates the analysis of TurtleBot3 experiment logs.
Instead of manually parsing CSV telemetry, the system converts structured logs into actionable insights through conversational queries.

---

## **Motivation**

Robotics experiments continuously record rich telemetry: odometry estimates, ground-truth poses, velocity commands, CPU usage, and memory.
Data collection is automated, but interpretation remains manual. Researchers spend hours:

* recomputing RMSE for every configuration
* slicing CSVs
* comparing durations and mapping states
* copying results into spreadsheets

This project eliminates that bottleneck.
The agent processes experiment logs and answers research questions directly, such as:

* *“Which configuration has the lowest localization error?”*
* *“How does Gmapping influence 10-minute runs?”*

---

## **Dataset**

Synthetic TurtleBot3 experiment logs sampled at **5 Hz**.
Each run includes:

* `timestamp`
* `x`, `y`
* `x_gt`, `y_gt` (ground truth)
* `v_linear`, `v_angular`
* `cpu`, `memory`

Configurations:

| Algorithm | Mapping | Durations    |
| --------- | ------- | ------------ |
| A         | ON/OFF  | 2, 5, 10 min |
| B         | ON/OFF  | 2, 5, 10 min |

A total of **12 runs** represent a realistic small ablation study used in robotics.

---

## **Localization Metrics**

Pointwise error is computed as:

[
e(t)=\sqrt{(x(t)-x_{gt}(t))^{2} + (y(t)-y_{gt}(t))^{2}}
]

From this sequence, the system computes:

* **RMSE** (root mean square error)
* **MAE** (mean absolute error)
* **Maximum localization error**

Resource metrics are averaged across the run:

* **CPU mean (%)**
* **Memory mean (MB)**

All metric operations are deterministic and reproducible.

---

## **Architecture**

The system is intentionally modular:

```
User → OrchestratorAgent → DataAnalysisAgent → ExplanationAgent → User
                     ↪ MemoryStore (conversational context)
```

### Agents

* **OrchestratorAgent**
  Interprets user questions and routes them to the appropriate modules.

* **DataAnalysisAgent**
  Loads summary metrics, performs filtering, and computes run-level comparisons.

* **ExplanationAgent**
  Converts numeric results into concise research insights.

* **MemoryStore**
  Maintains interaction context across sequential queries.

This separation ensures **no hallucinated results** — only grounded numeric outputs.

---

## **Example Usage**

```python
from agents import OrchestratorAgent

agent = OrchestratorAgent(summary_df)

print(agent.answer("Which configuration has the minimum localization error?"))
print(agent.answer("How does Gmapping affect localization for 10-minute runs?"))
```

---

## **Folder Structure**

```
robotics-experiment-intelligence-agent/
│
├─ agents/
│   ├─ memory_store.py
│   ├─ data_analysis_agent.py
│   ├─ explanation_agent.py
│   ├─ orchestrator_agent.py
│   └─ __init__.py
│
├─ data/
│   ├─ algorithma_gmappingon_2min.csv
│   ├─ algorithmb_gmappingoff_10min.csv
│   └─ ...
│
└─ robotics_experiment_intelligence_agent.ipynb
```

---

## **Running the Notebook**

Install dependencies:

```
pip install pandas numpy
```

Open the notebook:

```
robotics_experiment_intelligence_agent.ipynb
```

Run all cells to generate the summary table and agent Q&A results.

---

## **Why This Matters**

The system transforms experimental logs into a fast, conversational workflow:

* No spreadsheets
* No manual CSV slicing
* No repeated metric recalculation
* No ambiguity in interpretation

Evaluation becomes scalable, repeatable, and research-driven.

---

## **License**

This repository is intended for academic and research use.
Please cite the Kaggle Agents Intensive Capstone competition if reused.

👉 a **GitHub badge section** (stars, issues, license)
👉 a **cleaner README with diagrams included**
