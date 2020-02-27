# UBC MOCCA Migration Project (Still in Progress)

This project is meant to migrate core components and datasets of the C++ based UBC MOCCA software, which is called (TerrainRLSim)[https://github.com/UBCMOCCA/TerrainRLSim], into Gym. Thus this useful tool would be much easier to use, and potentially attract even more researchers join it.

## Roadmap

### Done

* Converted MOCCA character (JSON format) into (mujoco)[http://www.mujoco.org] **MJCF** format.

### TODO by now

* Solve the skybox issue for [0 -9.81 0] world.
* Adjust the camera in a better way.
* Handle joint limits/range.
* Add terrain data.
* Load and play motion data.

### In progress

* Converting MOCCA terrain (JSON format) into mujoco format.
* Parsing MOCCA motion files with python.
* Play motion data with mujoco based environment.
* Being able to access motion state, e.g. position, quaternion, velocity etc., of every body part and end effector easily.
* Creating learning tasks (or known as **env**) with Gym manner.
* Creating RL learning nets, or reusing open source implementations such as (OpenAI)[https://openai.github.io] and DeepMind.

## Python version&requirements

Python version 3.6+ is recommended.

Besides the requirements declared in **requirements.txt**, some external packages are required.

* (gym)[https://github.com/openai/gym]
* (mujoco-py)[https://github.com/openai/mujoco-py]
* (baselines)[https://github.com/openai/baselines]