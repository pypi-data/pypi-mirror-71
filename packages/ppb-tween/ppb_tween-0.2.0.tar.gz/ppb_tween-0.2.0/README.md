# ppb_tween

ppb_tween is a [tweening](https://en.wikipedia.org/wiki/Inbetweening) system
for [PursuedPyBear](https://ppb.dev/).

The tweening capabilities can be used directly or through Tweener objects. A
Tweener object can manage multiple transitions at different times across
different objects.

## Simple use case

```python
from ppb_tween import tween

# Move the player to (4, 0) over 3.5 seconds
tween(player_sprite, 'position', V(4, 0), 3.5)
```

## Property types supported

Tweening can transition object properties of `int`, `float`, or `ppb.Vector`
types, as well as tuples of any of these. This means RGB color tuples can also
be transitioned.

It is important to transition to `float` values for non-whole number properties,
even if the target value is a whole number. Otherwise, `ppb_tween` will think it
is an integer and transition in steps.

## Tweener objects

A `Tweener` object is a non-rendered scene object that manages the transitions
for one or more other objects in a scene. Using a `Tweener` over the simple
`tween` function has a few advantages:

- You can register a callback when transitions for a specific set of objects
  are done.
- You can check the `Tweener.is_tweening` property to find if any of the set
  of objects is still completing a transition.
- By sharing a single `Tweener` with multiple objects, you can control
  sequences of grouped movements.

See the example script for how to use a `Tweener` object:

```python
def on_scene_started(self, ev: SceneStarted, signal):
    self.position = ppb.Vector(-4, 0)
    self.tweener = ppb_tween.Tweener()
    ev.scene.add(self.tweener)

    self.tweener.tween(self, 'position', ppb.Vector(4, 0), 1, easing='bounce_out')
```
