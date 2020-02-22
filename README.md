# UBC MOCCA Migration Project

This project is meant to migrate core components and datasets of the C++ based UBC MOCCA software, which is called (TerrainRLSim)[https://github.com/UBCMOCCA/TerrainRLSim], into Gym. Thus this useful tool would be much easier to use, and potentially attract even more researchers join it.

## Roadmap

### Done

N./A.

### In progress

* Converting MOCCA character (JSON format) into (mujoco)[http://www.mujoco.org] **MJCF** format.
* Converting MOCCA terrain (JSON format) into mujoco format.
* Parsing MOCCA motion files with python.
* Play motion data with mujoco based environment.
* Being able to access motion state, e.g. position, quaternion, velocity etc., of every body part and end effector easily.
* Creating learning tasks (or known as **env**) with Gym manner.
* Creating RL learning nets, or reusing open source implementations such as (OpenAI)[https://openai.github.io] and DeepMind.