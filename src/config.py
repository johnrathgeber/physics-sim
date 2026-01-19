import os
import json
import src.defaults as df

MULTIPLIER_METADATA = {
    'r_radiusm': {
        'label': 'Radius',
        'description': 'Ball radius',
        'default': 1.0,
        'category': 'red_player'
    },
    'r_gravitym': {
        'label': 'Gravity',
        'description': 'Gravity strength - higher values pull the ball down faster',
        'default': 1.0,
        'category': 'red_player'
    },
    'r_jump_forcem': {
        'label': 'Jump Force',
        'description': 'Jump power when pressing UP key',
        'default': 1.0,
        'category': 'red_player'
    },
    'r_vertical_forcem': {
        'label': 'Vertical Force',
        'description': 'Vertical movement speed (up/down keys)',
        'default': 1.0,
        'category': 'red_player'
    },
    'r_lateral_forcem': {
        'label': 'Lateral Force',
        'description': 'Horizontal movement speed (left/right keys)',
        'default': 1.0,
        'category': 'red_player'
    },
    'r_lateral_frictionm': {
        'label': 'Lateral Friction',
        'description': 'Friction when moving sideways - higher = stops faster',
        'default': 1.0,
        'category': 'red_player'
    },
    'r_floor_bouncem': {
        'label': 'Floor Bounce',
        'description': 'Bounciness when hitting the floor',
        'default': 1.0,
        'category': 'red_player'
    },
    'r_player_weightm': {
        'label': 'Weight',
        'description': 'Ball mass - heavier balls push others more in collisions',
        'default': 1.0,
        'category': 'red_player'
    },
    'r_heavy_weightm': {
        'label': 'Heavy Weight',
        'description': 'Mass multiplier when in heavy mode',
        'default': 1.0,
        'category': 'red_player'
    },
    'r_heavy_force_multiplierm': {
        'label': 'Heavy Speed',
        'description': 'Speed reduction in heavy mode - lower = slower',
        'default': 1.0,
        'category': 'red_player'
    },
    'b_radiusm': {
        'label': 'Radius',
        'description': 'Ball radius',
        'default': 1.0,
        'category': 'blue_player'
    },
    'b_gravitym': {
        'label': 'Gravity',
        'description': 'Gravity strength - higher values pull the ball down faster',
        'default': 1.0,
        'category': 'blue_player'
    },
    'b_jump_forcem': {
        'label': 'Jump Force',
        'description': 'Jump power when pressing W key',
        'default': 1.0,
        'category': 'blue_player'
    },
    'b_vertical_forcem': {
        'label': 'Vertical Force',
        'description': 'Vertical movement speed (W/S keys)',
        'default': 1.0,
        'category': 'blue_player'
    },
    'b_lateral_forcem': {
        'label': 'Lateral Force',
        'description': 'Horizontal movement speed (A/D keys)',
        'default': 1.0,
        'category': 'blue_player'
    },
    'b_lateral_frictionm': {
        'label': 'Lateral Friction',
        'description': 'Friction when moving sideways - higher = stops faster',
        'default': 1.0,
        'category': 'blue_player'
    },
    'b_floor_bouncem': {
        'label': 'Floor Bounce',
        'description': 'Bounciness when hitting the floor',
        'default': 1.0,
        'category': 'blue_player'
    },
    'b_player_weightm': {
        'label': 'Weight',
        'description': 'Ball mass - heavier balls push others more in collisions',
        'default': 1.0,
        'category': 'blue_player'
    },
    'b_heavy_weightm': {
        'label': 'Heavy Weight',
        'description': 'Mass multiplier when in heavy mode',
        'default': 1.0,
        'category': 'blue_player'
    },
    'b_heavy_force_multiplierm': {
        'label': 'Heavy Speed',
        'description': 'Speed reduction in heavy mode - lower = slower',
        'default': 1.0,
        'category': 'blue_player'
    },
    'ball_bouncem': {
        'label': 'Bounciness',
        'description': 'Bounciness of ball-to-ball collisions',
        'default': 1.0,
        'category': 'global'
    },
    'npc_ball_radiusm': {
        'label': 'Bludger Radius',
        'description': 'Size of bludgers',
        'default': 1.0,
        'category': 'global'
    },
    'npc_accelerationm': {
        'label': 'Bludger Acceleration',
        'description': 'How fast bludgers accelerate towards players',
        'default': 1.0,
        'category': 'global'
    },
    'npc_max_speedm': {
        'label': 'Bludger Max Speed',
        'description': 'Maximum speed of bludgers',
        'default': 1.0,
        'category': 'global'
    },
    'npc_weightm': {
        'label': 'Bludger Weight',
        'description': 'Mass of bludgers',
        'default': 1.0,
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
        self.multipliers[key] = value

    def get_all_as_dict(self):
        return self.multipliers.copy()

    def get_category_multipliers(self, category):
        result = {}
        for key, metadata in MULTIPLIER_METADATA.items():
            if metadata['category'] == category:
                result[key] = self.multipliers[key]
        return result

    def to_dict(self):
        return {
            "name": "",
            "description": "",
            "version": "1.0",
            "multipliers": self.multipliers.copy()
        }

    def from_dict(self, data):
        self.multipliers.update(data["multipliers"])

    def reset_to_defaults(self):
        for key, metadata in MULTIPLIER_METADATA.items():
            self.multipliers[key] = metadata['default']

    @staticmethod
    def get_presets_dir():
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        presets_dir = os.path.join(base_dir, "presets")
        return presets_dir

    @staticmethod
    def ensure_presets_dir():
        presets_dir = GameConfig.get_presets_dir()
        os.makedirs(presets_dir, exist_ok=True)

    def save_preset(self, name, description=""):
        GameConfig.ensure_presets_dir()
        presets_dir = GameConfig.get_presets_dir()
        filepath = os.path.join(presets_dir, f"{name}.json")

        preset_data = self.to_dict()
        preset_data["name"] = name
        preset_data["description"] = description
        with open(filepath, 'w') as f:
            json.dump(preset_data, f, indent=2)

    @staticmethod
    def load_preset(name):
        presets_dir = GameConfig.get_presets_dir()
        filepath = os.path.join(presets_dir, f"{name}.json")
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def delete_preset(name):
        presets_dir = GameConfig.get_presets_dir()
        filepath = os.path.join(presets_dir, f"{name}.json")
        os.remove(filepath)

    @staticmethod
    def list_presets():
        GameConfig.ensure_presets_dir()
        presets_dir = GameConfig.get_presets_dir()
        presets = []
        for filename in os.listdir(presets_dir):
            if filename.endswith('.json'):
                preset_name = filename[:-5]
                presets.append(preset_name)
        if "default" in presets:
            presets.remove("default")
        presets.insert(0, "default")
        return presets if presets else ["default"]

    @staticmethod
    def create_default_preset():
        GameConfig.ensure_presets_dir()
        presets_dir = GameConfig.get_presets_dir()
        default_path = os.path.join(presets_dir, "default.json")

        if not os.path.exists(default_path):
            default_config = GameConfig()
            preset_data = default_config.to_dict()
            preset_data["name"] = "default"
            preset_data["description"] = "Default balanced settings (1.0 multipliers)"
            with open(default_path, 'w') as f:
                json.dump(preset_data, f, indent=2)
