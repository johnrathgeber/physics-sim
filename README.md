# Physics Sim

A two-player, physics-based game. This started as a curiosity project to explore physics simulation and evolved into a playable game with customizable mechanics.

## Overview

This project is a combination between a physics simulation and a game. I originally set out to build a physics engine from scratch and thought it would be more interesting to gameify it along the way. The result is a ball-based physics game where two players compete against each other and AI-controlled bludgers.

The goal is simple: knock your opponent out of bounds to score points. Use momentum, positioning, and the heavy mode strategically to outmaneuver your opponent while avoiding the bludgers and the edge yourself.

Players control colored balls with realistic physics including gravity, friction, momentum, and collision dynamics. The game features extensive customization options allowing you to tweak nearly every physical property as multipliers.

## Features

- **Two-player gameplay**: Blue player (WASD) vs Red player (Arrow keys)
- **AI opponents**: Configurable number of bludgers on each side
- **Physics simulation**: Custom-built physics engine with gravity, friction, and elastic collisions
- **Heavy mode**: Players can toggle a "heavy" state to increase mass and change collision behavior
- **Extensive customization**: Adjust multipliers for radius, gravity, jump force, weight, friction, bounce, and more

## Technology

Built entirely from scratch using Python and the pygame library. All game logic, physics calculations, and mechanics were hand-coded. Some UI components and display elements were created with AI assistance (vibecoded).

## Running the Game

```bash
python3 main.py
```

## Controls

**Blue Player:**
- WASD: Movement
- Left Shift: Toggle heavy mode

**Red Player:**
- Arrow keys: Movement
- Space: Toggle heavy mode

## Customization

The settings screen allows you to customize physics properties for each player and global settings. The real fun of this game comes from tinkering with the multipliers. Want zero gravity? 10x jump force? Massive bludgers with tiny players? The multipliers let you make the game as crazy as you want it to be.

## Project Status

This is more of a curiosity project than a finished product. It was built to explore physics simulation concepts and experiment with game mechanics rather than to create a polished, production-ready game.

## Inspiration

Takes inspiration from bonk.io, the browser-based multiplayer physics game.
