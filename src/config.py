import src.defaults as df

MULTIPLIER_METADATA = {
    'r_radiusm': {
        'label': 'Radius',
        'description': 'Ball radius',
        'default': 1,
        'category': 'red_player'
    },
    'r_gravitym': {
        'label': 'Gravity',
        'description': 'Gravity strength - higher values pull the ball down faster',
        'default': 1,
        'category': 'red_player'
    },
    'r_jump_forcem': {
        'label': 'Jump Force',
        'description': 'Jump power when pressing UP key',
        'default': 1,
        'category': 'red_player'
    },
    'r_vertical_forcem': {
        'label': 'Vertical Force',
        'description': 'Vertical movement speed (up/down keys)',
        'default': 1,
        'category': 'red_player'
    },
    'r_lateral_forcem': {
        'label': 'Lateral Force',
        'description': 'Horizontal movement speed (left/right keys)',
        'default': 1,
        'category': 'red_player'
    },
    'r_lateral_frictionm': {
        'label': 'Lateral Friction',
        'description': 'Friction when moving sideways - higher = stops faster',
        'default': 1,
        'category': 'red_player'
    },
    'r_floor_bouncem': {
        'label': 'Floor Bounce',
        'description': 'Bounciness when hitting the floor',
        'default': 1,
        'category': 'red_player'
    },
    'r_player_weightm': {
        'label': 'Weight',
        'description': 'Ball mass - heavier balls push others more in collisions',
        'default': 1,
        'category': 'red_player'
    },
    'r_heavy_weightm': {
        'label': 'Heavy Weight',
        'description': 'Mass multiplier when in heavy mode',
        'default': 1,
        'category': 'red_player'
    },
    'r_heavy_force_multiplierm': {
        'label': 'Heavy Speed',
        'description': 'Speed reduction in heavy mode - lower = slower',
        'default': 1,
        'category': 'red_player'
    },
    'b_radiusm': {
        'label': 'Radius',
        'description': 'Ball radius',
        'default': 1,
        'category': 'blue_player'
    },
    'b_gravitym': {
        'label': 'Gravity',
        'description': 'Gravity strength - higher values pull the ball down faster',
        'default': 1,
        'category': 'blue_player'
    },
    'b_jump_forcem': {
        'label': 'Jump Force',
        'description': 'Jump power when pressing W key',
        'default': 1,
        'category': 'blue_player'
    },
    'b_vertical_forcem': {
        'label': 'Vertical Force',
        'description': 'Vertical movement speed (W/S keys)',
        'default': 1,
        'category': 'blue_player'
    },
    'b_lateral_forcem': {
        'label': 'Lateral Force',
        'description': 'Horizontal movement speed (A/D keys)',
        'default': 1,
        'category': 'blue_player'
    },
    'b_lateral_frictionm': {
        'label': 'Lateral Friction',
        'description': 'Friction when moving sideways - higher = stops faster',
        'default': 1,
        'category': 'blue_player'
    },
    'b_floor_bouncem': {
        'label': 'Floor Bounce',
        'description': 'Bounciness when hitting the floor',
        'default': 1,
        'category': 'blue_player'
    },
    'b_player_weightm': {
        'label': 'Weight',
        'description': 'Ball mass - heavier balls push others more in collisions',
        'default': 1,
        'category': 'blue_player'
    },
    'b_heavy_weightm': {
        'label': 'Heavy Weight',
        'description': 'Mass multiplier when in heavy mode',
        'default': 1,
        'category': 'blue_player'
    },
    'b_heavy_force_multiplierm': {
        'label': 'Heavy Speed',
        'description': 'Speed reduction in heavy mode - lower = slower',
        'default': 1,
        'category': 'blue_player'
    },
    'ball_bouncem': {
        'label': 'Bounciness',
        'description': 'Bounciness of ball-to-ball collisions',
        'default': 1,
        'category': 'global'
    },
    'npc_ball_radiusm': {
        'label': 'Bludger Radius',
        'description': 'Size of bludgers',
        'default': 1,
        'category': 'global'
    },
    'npc_accelerationm': {
        'label': 'Bludger Acceleration',
        'description': 'How fast bludgers accelerate towards players',
        'default': 1,
        'category': 'global'
    },
    'npc_max_speedm': {
        'label': 'Bludger Max Speed',
        'description': 'Maximum speed of bludgers',
        'default': 1,
        'category': 'global'
    },
    'npc_weightm': {
        'label': 'Bludger Weight',
        'description': 'Mass of bludgers',
        'default': 1,
        'category': 'global'
    },
    'num_npc_balls_per_side': {
        'label': 'Bludgers Per Side',
        'description': 'Number of bludgers on each side',
        'default': df.num_npc_balls_per_side,
        'category': 'global'
    }
}

class GameConfig:
    def __init__(self):
        self.multipliers = {}
        for key, metadata in MULTIPLIER_METADATA.items():
            self.multipliers[key] = metadata['default']

    def get_multiplier(self, key):
        return self.multipliers.get(key)

    def set_multiplier(self, key, value):
        if key not in MULTIPLIER_METADATA:
            raise ValueError(f"Unknown multiplier: {key}")

        metadata = MULTIPLIER_METADATA[key]

        if value < 0:
            raise ValueError(f"{key} must be greater than 0.")

        self.multipliers[key] = value

    def get_all_as_dict(self):
        return self.multipliers.copy()

    def validate_all(self):
        for key, value in self.multipliers.items():
            metadata = MULTIPLIER_METADATA[key]
            if value < 0:
                return False, f"{metadata['label']} out of range"
        return True, "All valid"

    def get_category_multipliers(self, category):
        result = {}
        for key, metadata in MULTIPLIER_METADATA.items():
            if metadata['category'] == category:
                result[key] = self.multipliers[key]
        return result
