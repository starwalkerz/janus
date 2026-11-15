# Event gating: when enabled, IQM hardware is only used when KAIROS
# flags an anomaly or Causalitybot detects a horizon above threshold.
# Baseline ticks run on Aer/classical with zero credit burn.
gate_enabled = true
gate_on_kairos = true
gate_on_causality = true
gate_kairos_threshold = 0.05
gate_causality_threshold = 0.20