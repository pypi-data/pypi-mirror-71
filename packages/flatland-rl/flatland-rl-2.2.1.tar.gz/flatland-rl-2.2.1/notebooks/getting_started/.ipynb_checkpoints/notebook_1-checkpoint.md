---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.3.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Part 1: Creating and rendering an environment



> In this notebook, you will learn how to **create**, **interact with** and **render** your first railway system. Let's get started!


Let's start by importing a few Flatland classes - we will detail their role as we go

```python
from flatland.core.grid.rail_env_grid import RailEnvTransitions
from flatland.envs.rail_env import RailEnv, RailEnvActions
from flatland.envs.rail_generators import rail_from_manual_specifications_generator
from flatland.utils.rendertools import RenderTool, AgentRenderVariant
```

Creating a rail network
---


There are multiple ways to generate a rail network. The simpler one is to describe it explicitely, as such:

```python
specs = [[(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
         [(0, 0), (0, 0), (0, 0), (0, 0), (7, 0), (0, 0)],
         [(7, 270), (1, 90), (1, 90), (1, 90), (2, 90), (7, 90)],
         [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]]
```

As you can see, `specs` is a 2-dimensional array of tuples

```python
import numpy as np

rail_shape = np.array(specs).shape
rail_shape
```

The `specs` array represent a 4 by 6 2D grid of tuples. In each tuple, the first element represent the **cell type**, and the second the **rotation** of the cell (0, 90, 180 or 270 degrees clockwise).

See `flatland.core.grid.rail_env_grid.RailEnvTransitions` for implementation details.

```python
env = RailEnv(width=rail_shape[1],
              height=rail_shape[0],
              rail_generator=rail_from_manual_specifications_generator(specs),
              number_of_agents=1
              )
```

After the `RailEnv` environment is created, initialize it by calling `reset()`:

```python
env.reset();
```

**That's it!** You have just created your first rail environment. Let's render it to see how it looks.


Rendering the environment
---

```python
import PIL

env_renderer = RenderTool(env, gl="TKPIL")
env_renderer.render_env()
```

```python
arrImage = env_renderer.get_image()
pilImage = PIL.Image.fromarray(arrImage)
display(pilImage)
```

Creating a random environment
---


Alternatively, a random environment can be generated (optionally specifying weights for each cell type to increase or decrease their proportion in the generated rail networks).



```python
# Step the env, with an action for the agent, which causes it to become "active"
# You can re-run this cell to take another step.
# In this example the agent terminates after just 2 or 3 steps.
env.step({0: RailEnvActions.MOVE_FORWARD});
```

Animated rendering
---


We will use [ipycanvas](https://github.com/martinRenou/ipycanvas) to cleanly display the environment in the notebook.
Note that Flatland comes with multiple rendering options.

```python
from ipycanvas import Canvas
```

```python
env_renderer = render_pil = RenderTool(env, gl="PILSVG",
                                       agent_render_variant=AgentRenderVariant.ONE_STEP_BEHIND,
                                       show_debug=False,
                                       screen_height=1000,  # Adjust these parameters to fit your resolution
                                       screen_width=1300)  # Adjust these parameters to fit your resolution

env_renderer.reset()
```

```python
render_pil.render_env(show=False, show_observations=False, show_predictions=False, show_agents=True)
img = render_pil.get_image()

canvas = Canvas(size=(img.shape[0], img.shape[1]))
canvas.put_image_data(img)
```

```python
canvas
```
