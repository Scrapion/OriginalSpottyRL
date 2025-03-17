# FDS-README

## 1. from spotmicro.util.gui import GUI

**Purpose:**

The GUI class provides a Graphical User Interface (GUI) based on PyBullet to interactively tune robot control parameters such as velocity, orientation, step length, etc.

This is especially useful for testing and debugging gait behaviors during simulation.

**Arguments:**

When you instantiate `GUI`, you must pass:
- `quadruped`: (**int**) — The PyBullet body unique ID of the robot, typically loaded from the URDF. This is used to visualize and control the robot in the GUI.

**Example:**

```python
gui = GUI(env.spot.quadruped)
```

Here, `env.spot` is the robot model, and `.quadruped` is the ID returned by PyBullet when loading the URDF. It is initialized in the parent class `spotGymEnv` and assigned inside the `reset()` method.

**Result:**

Provides a user interface for real-time control of gait parameters and robot states. Typically used during simulation/testing to manually tweak behavior. It relies on PyBullet to control the robot visually and interactively using sliders based on the robot's body ID.

---

## 2. from spotmicro.GymEnvs.spot_bezier_env import spotBezierEnv

**Purpose:**

A Gym environment compatible with OpenAI Gym, used for training reinforcement learning (RL) agents on a robot using Bezier-based gaits.

**Arguments:**

When you instantiate `spotBezierEnv()`, you can pass the following optional parameters:
- `render`: (**bool**) — If `True`, opens the PyBullet GUI for visualizing the robot.
- `on_rack`: (**bool**) — If `True`, the robot floats in the air without falling, useful for debugging.
- `height_field`: (**bool**) — Enables a procedurally generated terrain to test locomotion on uneven surfaces.
- `draw_foot_path`: (**bool**) — If `True`, visualizes the planned foot trajectory during gait.
- `contacts`: (**bool**) — If `True`, enables contact feedback from feet to be used as part of the observation.
- `env_randomizer`: (**SpotEnvRandomizer**) — Optional instance for randomizing physics/environment parameters to improve robustness.

```python
env = spotBezierEnv(render=True, on_rack=False)
```

**Result:**

Returns a custom OpenAI Gym-compatible environment for simulating the Spot Micro robot using Bezier gaits. Supports typical Gym interface:
- `env.step(action)` — Advances the simulation by one step.
- `env.reset()` — Resets the simulation to initial state.
- `env.render()` — Renders the current state (if GUI is enabled).
- `env.observation_space`, `env.action_space` — Standard Gym spaces for agent interaction.

The environment includes access to:
- `env.spot`: the robot model instance.
- `env.spot.quadruped`: the PyBullet ID of the robot loaded from URDF (used by GUI and controller logic).

---

## 3. from spotmicro.Kinematics.SpotKinematics import SpotModel

**Purpose:**

Encapsulates the robot kinematics model, particularly forward and inverse kinematics for each leg of the quadruped.

**Arguments:**

When you instantiate `SpotModel(...)`, you can customize the physical and geometric properties of the robot:

- `shoulder_length`: (**float**) — Default: 0.055 — Length of shoulder segment.
- `elbow_length`: (**float**) — Default: 0.10652 — Length of elbow segment.
- `wrist_length`: (**float**) — Default: 0.145 — Length of wrist segment (to foot).
- `hip_x`: (**float**) — Default: 0.23 — Distance between front and back legs (X-axis).
- `hip_y`: (**float**) — Default: 0.075 — Distance between left and right hips (Y-axis).
- `foot_x`: (**float**) — Default: 0.23 — Default X-position of feet.
- `foot_y`: (**float**) — Default: 0.185 — Default Y-position of feet.
- `height`: (**float**) — Default: 0.20 — Default height of the robot body.
- `com_offset`: (**float**) — Default: 0.016 — Center of mass offset.
- `shoulder_lim`: (**list of float**) — Joint angle limits for shoulder. Default: `[-0.548, 0.548]`
- `elbow_lim`: (**list of float**) — Joint angle limits for elbow. Default: `[-2.17, 0.97]`
- `wrist_lim`: (**list of float**) — Joint angle limits for wrist. Default: `[-0.1, 2.59]`

**Methods include:**

```python
joint_angles = spot_model.IK(orn, pos, T_bf)     # Returns 4x3 array of joint angles
hip_to_foot = spot_model.HipToFoot(orn, pos, T_bf)  # Returns vectors from hip to foot
```

Where:
- `orn` is a list of [roll, pitch, yaw]
- `pos` is a list of [x, y, z] body position
- `T_bf` is a dictionary of transformation matrices from body to foot

**Result:**

Provides inverse kinematics solutions for each of the four legs of the Spot Micro robot. Given the robot's body position and orientation, it returns joint angles for actuating the legs appropriately.

---

## 4. from spotmicro.GaitGenerator.Bezier import BezierGait

**Purpose:**

The `BezierGait` class generates smooth, cyclic leg trajectories for quadrupedal walking using Bezier curves for the swing phase and sine-based motion for the stance phase. It synchronizes leg phases using internal clocks and supports turning (yaw), lateral, and forward motions. It is designed for realistic and efficient walking gait generation.

**Arguments:**

```python
gait = BezierGait(dSref=[0.0, 0.0, 0.5, 0.5], dt=0.01, Tswing=0.2)
```

- `dSref`: (**list of float**) — Default: `[0.0, 0.0, 0.5, 0.5]`  
  Phase offset for each leg (FL, FR, BL, BR), used to coordinate leg timing.
- `dt`: (**float**) — Default: `0.01`  
  Time step of the simulation.
- `Tswing`: (**float**) — Default: `0.2`  
  Duration of the swing phase for each leg in seconds.

**Key Methods:**
- `GenerateTrajectory(L, LateralFraction, YawRate, vel, T_bf_, T_bf_curr, clearance_height, penetration_depth, contacts, dt=None)`  
  Generates updated foot target positions using Bezier or stance logic depending on phase. Returns updated foot transform matrices.

- `SwingStep(...)`  
  Computes the Bezier curve trajectory for a leg during the swing phase.

- `StanceStep(...)`  
  Computes smooth motion during the stance phase using a sine curve.

- `BezierSwing(...)`  
  Computes the X, Y, Z positions of a foot using a 12-control-point Bezier curve over time.

- `YawCircle(...)`  
  Applies rotation (yaw) to the swing trajectory for turning maneuvers.

- `GetPhase(leg_idx)`, `CheckTouchDown(...)`, `Get_ti(...)`, `Increment(...)`  
  Internal methods for handling phase timing and detecting transitions between swing and stance.

**Result:**

The class outputs updated body-to-foot transform matrices that define where each foot should be placed in the current time step. These trajectories can be fed to the inverse kinematics and motor controller to animate the robot's walking motion. It allows for flexible control over walking patterns, including turning and lateral movement. It supports both stance and swing phases for each leg independently and applies circular yaw transformations to foot trajectories for turning. The trajectories are returned as transformation matrices and can be used directly with inverse kinematics solvers like `SpotModel.IK()`.

---

## 5. from spotmicro.OpenLoopSM.SpotOL import BezierStepper

**Purpose:**

`BezierStepper` is an open-loop step parameter generator used to produce high-level walking behavior inputs for gait generation. It modulates parameters such as step length, lateral shift, turning rate (yaw), and foot velocities. It cycles through a state machine to simulate different walking patterns, such as forward motion, lateral steps, rotation, and combined movement — useful for robust policy training in reinforcement learning (RL).

**Arguments:**

When creating `BezierStepper`:

```python
stepper = BezierStepper(
    pos=np.array([0.0, 0.0, 0.0]),
    orn=np.array([0.0, 0.0, 0.0]),
    StepLength=0.04,
    LateralFraction=0.0,
    YawRate=0.0,
    StepVelocity=0.001,
    ClearanceHeight=0.045,
    PenetrationDepth=0.003,
    episode_length=5000,
    dt=0.01,
    num_shuffles=2,
    mode=0  # FWD or ALL
)
```

- `pos`, `orn`: Initial position and orientation vectors.
- `StepLength`, `LateralFraction`, `YawRate`, `StepVelocity`: Movement parameters (forward, lateral, rotational, and velocity).
- `ClearanceHeight`, `PenetrationDepth`: Foot trajectory height/depth parameters.
- `episode_length`: Steps before resetting the state sequence.
- `dt`: Simulation time step.
- `num_shuffles`: Number of times to shuffle gait modes.
- `mode`: FWD = only forward; ALL = use all movement states.

**Key Methods:**
- `StateMachine()`: Updates internal state and generates next movement parameters based on the current gait type (FB, LAT, ROT, COMBI).
- `return_bezier_params()`: Returns a tuple of updated parameters:
  ```python
  pos, orn, StepLength, LateralFraction, YawRate,
  StepVelocity, ClearanceHeight, PenetrationDepth
  ```
  These parameters are fed into `BezierGait.GenerateTrajectory(...)` to produce the actual foot movement patterns.
- `reset()`: Resets the internal step counter and state machine to start a new episode.

**Result:**

Produces time-evolving, randomized movement parameters for the gait generator. It is used in conjunction with `BezierGait` to produce diverse, naturalistic leg trajectories. Designed to support generalization in RL training through behavioral diversity.

---

## 6. from spotmicro.spot_env_randomizer import SpotEnvRandomizer

**Purpose:**

`SpotEnvRandomizer` adds domain randomization to the SpotMini simulation. It modifies physical properties like mass, voltage, friction, and damping at each environment reset. This makes the robot's behavior more robust to real-world uncertainties and improves generalization in reinforcement learning (RL) training.

**Arguments:**

```python
randomizer = SpotEnvRandomizer(
    spot_base_mass_err_range=(-0.2, 0.2),
    spot_leg_mass_err_range=(-0.2, 0.2),
    battery_voltage_range=(7.0, 8.4),
    motor_viscous_damping_range=(0.0, 0.01)
)
```

- `spot_base_mass_err_range`: (**tuple of float**) — Relative noise to apply to robot base mass (±20% default).
- `spot_leg_mass_err_range`: (**tuple of float**) — Relative noise for individual leg masses.
- `battery_voltage_range`: (**tuple of float**) — Voltage range to simulate battery fluctuation.
- `motor_viscous_damping_range`: (**tuple of float**) — Torque damping applied per motor to simulate real-world losses.

**Key Method:**

```python
randomizer.randomize_env(env)
```

- This method is called after environment reset and applies random physical variations to the robot via `env.spot`.

**Internal Adjustments:**

- Randomizes base mass via `spot.SetBaseMass(...)`
- Randomizes leg masses individually using `spot.SetLegMasses(...)`
- Samples battery voltage using `spot.SetBatteryVoltage(...)`
- Applies motor damping using `spot.SetMotorViscousDamping(...)`
- Randomizes foot-ground friction using `spot.SetFootFriction(...)` with sampled values from constants.

**Result:**

The randomizer applies noise to the simulation so the robot sees slightly different physical conditions each episode. This improves robustness of the control policy and helps bridge the sim-to-real gap in deployment.

---

## 7. from ars_lib.ars import ARSAgent, Normalizer, Policy, ParallelWorker

**Purpose:**

These are the core components of the Augmented Random Search (ARS) algorithm, a policy search method used to train the Spot robot using reinforcement learning. ARS is a scalable, derivative-free optimization method that works well with linear policies and parallel rollout execution.

---

**Components:**

### `ARSAgent`

- **Purpose**: Central class coordinating the training loop, policy updates, and evaluation of the robot in the simulation environment.
- **Arguments**:
  - `normalizer`: Instance of `Normalizer` for scaling state inputs.
  - `policy`: Instance of `Policy`, a linear state-action mapper.
  - `env`: The Gym environment (`spotBezierEnv`) used for interaction.
  - `smach`: Optional `BezierStepper` for gait modulation.
  - `TGP`: Optional `BezierGait` for trajectory generation.
  - `spot`: Optional robot kinematic model.
  - `gui`: If `True`, activates interactive GUI.
- **Methods**:
  - `deploy()`: Runs a rollout using the current policy and returns total reward.
  - `train_parallel()`: Runs multiple parallel workers with perturbed policies and updates weights based on best performing rollouts.

---

### `Normalizer`

- **Purpose**: Tracks running statistics (mean, variance) of observed states and normalizes them.
- **Methods**:
  - `observe(x)`: Updates statistics based on new state input.
  - `normalize(state)`: Standardizes input to zero-mean, unit-variance.

---

### `Policy`

- **Purpose**: A linear policy class that computes actions using:
  ```python
  action = theta.dot(state)
  ```
- **Arguments**:
  - `state_dim`, `action_dim`, `learning_rate`, `num_deltas`, `num_best_deltas`, `expl_noise`, `episode_steps`
- **Methods**:
  - `evaluate(state, delta=None, direction=None)`: Returns action for a given state (with optional perturbation).
  - `update(rollouts, std_dev_rewards)`: Adjusts weights using reward-weighted gradient estimation.
  - `sample_deltas()`: Samples random perturbations.

---

### `ParallelWorker`

- **Purpose**: Executes rollouts in parallel processes. Each worker receives a perturbed policy, runs a simulation episode, and returns the reward.
- **Workflow**:
  - Listens for commands over a multiprocessing pipe (`_EXPLORE`, `_RESET`, `_CLOSE`)
  - Executes environment rollouts
  - Sends results (reward) back to master process

---

**Result:**

Together, these components train the robot's gait policy using ARS by running many policy variations in parallel, evaluating them, and updating the policy parameters toward higher reward regions.
