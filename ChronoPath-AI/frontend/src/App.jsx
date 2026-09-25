import { useState } from "react";

function App() {
  const [title, setTitle] = useState("");

  const [options, setOptions] = useState([
    "MCA",
    "GATE",
    "Software Job",
  ]);

  const [criteria, setCriteria] = useState([
    { name: "Career Growth", weight: 0.3 },
    { name: "Salary", weight: 0.25 },
    { name: "Job Security", weight: 0.2 },
    { name: "Cost", weight: 0.1 },
    { name: "Time", weight: 0.15 },
  ]);

  const [scores, setScores] = useState({});

  const [results, setResults] = useState([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  // --------------------------------
  // OPTIONS
  // --------------------------------

  const addOption = () => {
    setOptions([...options, ""]);
  };

  const updateOption = (index, value) => {
    const updated = [...options];

    updated[index] = value;

    setOptions(updated);
  };

  // --------------------------------
  // CRITERIA
  // --------------------------------

  const addCriterion = () => {
    setCriteria([
      ...criteria,
      {
        name: "",
        weight: 0,
      },
    ]);
  };

  const updateCriterionName = (index, value) => {
    const updated = [...criteria];

    updated[index].name = value;

    setCriteria(updated);
  };

  const updateCriterionWeight = (index, value) => {
    const updated = [...criteria];

    updated[index].weight = Number(value);

    setCriteria(updated);
  };

  // --------------------------------
  // SCORE MATRIX
  // --------------------------------

  const updateScore = (
    optionIndex,
    criterionIndex,
    value
  ) => {
    const key = `${optionIndex}-${criterionIndex}`;

    setScores({
      ...scores,
      [key]: Number(value),
    });
  };

  // --------------------------------
  // ANALYZE
  // --------------------------------

  const analyzeDecision = async () => {
    setError("");

    setResults([]);

    const validOptions = options.filter(
      (option) => option.trim() !== ""
    );

    const validCriteria = criteria.filter(
      (criterion) => criterion.name.trim() !== ""
    );

    if (!title.trim()) {
      setError("Please enter a decision.");

      return;
    }

    if (validOptions.length < 2) {
      setError(
        "Please enter at least two options."
      );

      return;
    }

    if (validCriteria.length < 1) {
      setError(
        "Please enter at least one criterion."
      );

      return;
    }

    // -----------------------------
    // CHECK WEIGHTS
    // -----------------------------

    const totalWeight =
      validCriteria.reduce(
        (sum, criterion) =>
          sum + criterion.weight,
        0
      );

    if (
      Math.abs(totalWeight - 1) >
      0.001
    ) {
      setError(
        `Criterion weights must total 100%. Current total: ${(
          totalWeight * 100
        ).toFixed(1)}%`
      );

      return;
    }

    // -----------------------------
    // CREATE SCORE MATRIX
    // -----------------------------

    const optionScores =
      validOptions.map(
        (option, optionIndex) => ({
          option,

          scores:
            validCriteria.map(
              (_, criterionIndex) => {
                const key = `${optionIndex}-${criterionIndex}`;

                return (
                  scores[key] ?? 5
                );
              }
            ),
        })
      );

    setLoading(true);

    try {
      const response =
        await fetch(
          "http://127.0.0.1:8000/api/decision/analyze",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              title,

              options:
                validOptions,

              criteria:
                validCriteria,

              option_scores:
                optionScores,
            }),
          }
        );

      if (!response.ok) {
        const errorData =
          await response.json();

        throw new Error(
          errorData.detail ||
            "Failed to analyze decision."
        );
      }

      const data =
        await response.json();

      setResults(
        data.results
      );
    } catch (error) {
      setError(
        error.message
      );
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------
  // UI
  // --------------------------------

  return (
    <div
      style={{
        minHeight: "100vh",

        background:
          "#f5f7fb",

        padding: "40px",

        fontFamily:
          "Arial, sans-serif",
      }}
    >
      <div
        style={{
          maxWidth:
            "1100px",

          margin:
            "0 auto",
        }}
      >
        <h1>
          ChronoPath AI
        </h1>

        <p>
          AI-Assisted Future
          Decision Simulator
        </p>

        <hr />

        {/* ---------------------- */}
        {/* DECISION */}
        {/* ---------------------- */}

        <h2>
          1. Your Decision
        </h2>

        <input
          type="text"
          placeholder="Example: Should I pursue MCA or take a software job?"
          value={title}
          onChange={(e) =>
            setTitle(
              e.target.value
            )
          }
          style={{
            width: "100%",

            padding: "12px",

            fontSize: "16px",

            marginBottom:
              "20px",
          }}
        />

        {/* ---------------------- */}
        {/* OPTIONS */}
        {/* ---------------------- */}

        <h2>
          2. Options
        </h2>

        {options.map(
          (
            option,
            index
          ) => (
            <input
              key={index}
              type="text"
              placeholder={`Option ${
                index + 1
              }`}
              value={option}
              onChange={(e) =>
                updateOption(
                  index,
                  e.target.value
                )
              }
              style={{
                width:
                  "100%",

                padding:
                  "10px",

                marginBottom:
                  "10px",
              }}
            />
          )
        )}

        <button
          onClick={
            addOption
          }
        >
          + Add Option
        </button>

        {/* ---------------------- */}
        {/* CRITERIA */}
        {/* ---------------------- */}

        <h2>
          3. Criteria &
          Weights
        </h2>

        {criteria.map(
          (
            criterion,
            index
          ) => (
            <div
              key={index}
              style={{
                display:
                  "flex",

                gap:
                  "10px",

                marginBottom:
                  "10px",
              }}
            >
              <input
                type="text"
                placeholder="Criterion"
                value={
                  criterion.name
                }
                onChange={(e) =>
                  updateCriterionName(
                    index,
                    e.target.value
                  )
                }
                style={{
                  flex: 1,

                  padding:
                    "10px",
                }}
              />

              <input
                type="number"
                min="0"
                max="1"
                step="0.05"
                value={
                  criterion.weight
                }
                onChange={(e) =>
                  updateCriterionWeight(
                    index,
                    e.target.value
                  )
                }
                style={{
                  width:
                    "120px",

                  padding:
                    "10px",
                }}
              />
            </div>
          )
        )}

        <button
          onClick={
            addCriterion
          }
        >
          + Add Criterion
        </button>

        {/* ---------------------- */}
        {/* SCORE MATRIX */}
        {/* ---------------------- */}

        <h2
          style={{
            marginTop:
              "40px",
          }}
        >
          4. Score Each
          Option
        </h2>

        <p>
          Rate each option
          from 0 to 10.
        </p>

        <div
          style={{
            overflowX:
              "auto",
          }}
        >
          <table
            style={{
              width:
                "100%",

              borderCollapse:
                "collapse",

              background:
                "white",
            }}
          >
            <thead>
              <tr>
                <th
                  style={{
                    padding:
                      "12px",

                    border:
                      "1px solid #ddd",
                  }}
                >
                  Option
                </th>

                {criteria.map(
                  (
                    criterion,
                    index
                  ) => (
                    <th
                      key={
                        index
                      }
                      style={{
                        padding:
                          "12px",

                        border:
                          "1px solid #ddd",
                      }}
                    >
                      {
                        criterion.name
                      }
                    </th>
                  )
                )}
              </tr>
            </thead>

            <tbody>
              {options.map(
                (
                  option,
                  optionIndex
                ) => (
                  <tr
                    key={
                      optionIndex
                    }
                  >
                    <td
                      style={{
                        padding:
                          "12px",

                        border:
                          "1px solid #ddd",

                        fontWeight:
                          "bold",
                      }}
                    >
                      {option ||
                        `Option ${
                          optionIndex +
                          1
                        }`}
                    </td>

                    {criteria.map(
                      (
                        _,
                        criterionIndex
                      ) => {
                        const key =
                          `${optionIndex}-${criterionIndex}`;

                        return (
                          <td
                            key={
                              criterionIndex
                            }
                            style={{
                              padding:
                                "8px",

                              border:
                                "1px solid #ddd",
                            }}
                          >
                            <input
                              type="number"
                              min="0"
                              max="10"
                              value={
                                scores[
                                  key
                                ] ??
                                ""
                              }
                              onChange={(
                                e
                              ) =>
                                updateScore(
                                  optionIndex,
                                  criterionIndex,
                                  e
                                    .target
                                    .value
                                )
                              }
                              style={{
                                width:
                                  "70px",

                                padding:
                                  "8px",
                              }}
                            />
                          </td>
                        );
                      }
                    )}
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>

        {/* ---------------------- */}
        {/* ANALYZE */}
        {/* ---------------------- */}

        <button
          onClick={
            analyzeDecision
          }
          disabled={
            loading
          }
          style={{
            marginTop:
              "30px",

            padding:
              "14px 30px",

            fontSize:
              "16px",

            cursor:
              "pointer",
          }}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Decision"}
        </button>

        {/* ---------------------- */}
        {/* ERROR */}
        {/* ---------------------- */}

        {error && (
          <div
            style={{
              marginTop:
                "20px",

              padding:
                "15px",

              background:
                "#ffe5e5",

              borderRadius:
                "8px",
            }}
          >
            {error}
          </div>
        )}

        {/* ---------------------- */}
        {/* RESULTS */}
        {/* ---------------------- */}

        {results.length >
          0 && (
          <div
            style={{
              marginTop:
                "40px",
            }}
          >
            <h2>
              Decision Results
            </h2>

            {results.map(
              (
                result
              ) => (
                <div
                  key={
                    result.option
                  }
                  style={{
                    padding:
                      "20px",

                    marginBottom:
                      "10px",

                    background:
                      "white",

                    borderRadius:
                      "8px",

                    border:
                      "1px solid #ddd",
                  }}
                >
                  <h3>
                    #
                    {
                      result.rank
                    }{" "}
                    —{" "}
                    {
                      result.option
                    }
                  </h3>

                  <p>
                    Weighted
                    Score:{" "}
                    {
                      result.score
                    }
                  </p>
                </div>
              )
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;