"""
LEAF-Link control simulation: one temperature channel of a plant growth chamber under PID control.

Independent research by Arjun, Null Set Labs, April 2026. Model and gains are unchanged from the
original script; October 2026 changes are limited to writing the results to JSON.

Scenario: the setpoint steps from a night value of 20 C to a day value of 25 C at t = 30 min,
as plant habitats do on a day/night schedule. Three gain sets are compared.

Chamber model: first-order, dT/dt = ((T0 + K_HEAT * u) - T) / TAU, with the heater command u
limited to +/- 80 W and integrator anti-windup at the limit. There is no sensor lag or dead time.

The "stress score" is an illustrative placeholder, not a biological model:
  score = 1 - exp(-(0.35 * overshoot_C + 0.08 * minutes_above_26C + 0.022 * settling_minutes))

Usage: python chamber_pid_sim.py   (writes results/pid_results.json next to this script)
"""
import json
from pathlib import Path

import numpy as np

TAU = 180.0        # s, chamber thermal time constant
T_START = 20.0     # C
K_HEAT = 0.12      # C of steady-state rise per W
HEATER_MAX = 80.0  # W
DT = 1.0           # s
T_END = 150 * 60   # s
STEP_AT = 1800     # s
TUNINGS = [(3.0, 0.005, 2.0, "Under-tuned"),
           (80.0, 1.00, 2.0, "Aggressive"),
           (25.0, 0.08, 20.0, "Balanced")]


class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0.0
        self.prev_err = 0.0

    def step(self, sp, meas, dt):
        err = sp - meas
        self.integral += err * dt
        deriv = (err - self.prev_err) / dt
        u = self.kp * err + self.ki * self.integral + self.kd * deriv
        u_sat = max(-HEATER_MAX, min(HEATER_MAX, u))
        if u_sat != u:
            self.integral -= err * dt  # anti-windup
        self.prev_err = err
        return u_sat


def run(kp, ki, kd, label):
    t = np.arange(0, T_END, DT)
    T = np.zeros_like(t)
    u = np.zeros_like(t)
    T[0] = T_START
    sp = np.where(t < STEP_AT, 20.0, 25.0)
    pid = PID(kp, ki, kd)
    for i in range(1, len(t)):
        u[i] = pid.step(sp[i], T[i - 1], DT)
        T[i] = T[i - 1] + ((T_START + K_HEAT * u[i]) - T[i - 1]) / TAU * DT
    after = T[STEP_AT:]
    peak = float(after.max())
    overshoot = max(0.0, peak - 25.0)
    above26 = float((after > 26.0).sum()) * DT / 60.0
    unsettled = np.where(np.abs(after - 25.0) >= 0.3)[0]
    settle = 0.0 if len(unsettled) == 0 else (unsettled.max() + 1) * DT / 60.0
    reach = np.where(after >= 24.5)[0]
    score = float(np.clip(1.0 - np.exp(-(0.35 * overshoot + 0.08 * above26 + 0.022 * settle)), 0.0, 1.0))
    every = slice(None, None, 30)
    return {"label": label, "kp": kp, "ki": ki, "kd": kd,
            "peak_C": round(peak, 3), "overshoot_C": round(overshoot, 3), "minutes_above_26C": round(above26, 2),
            "minutes_to_24_5C": round(float(reach[0]) * DT / 60.0, 2) if len(reach) else None,
            "settling_minutes": round(float(settle), 2), "final_C": round(float(T[-1]), 3),
            "stress_score": round(score, 3),
            "t_min": [round(float(v), 2) for v in (t / 60.0)[every]],
            "T": [round(float(v), 3) for v in T[every]],
            "heater_W": [round(float(v), 2) for v in u[every]]}


def main():
    runs = [run(*x) for x in TUNINGS]
    out = {"model": {"tau_s": TAU, "t_start_C": T_START, "k_heat_C_per_W": K_HEAT, "heater_limit_W": HEATER_MAX,
                     "setpoint": "20 C until 30 min, then 25 C"}, "runs": runs}
    dest = Path(__file__).parent / "results" / "pid_results.json"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out))
    print("%-12s %8s %9s %8s %9s %8s" % ("Tuning", "Peak C", "To 24.5", "Settle", "Above 26", "Score"))
    for r in runs:
        print("%-12s %8.3f %9.2f %8.2f %9.2f %8.3f" % (r["label"], r["peak_C"], r["minutes_to_24_5C"],
                                                      r["settling_minutes"], r["minutes_above_26C"], r["stress_score"]))


if __name__ == "__main__":
    main()
