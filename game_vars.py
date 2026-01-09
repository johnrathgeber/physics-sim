import defaults as df


def calculate_game_vars(config):
    multipliers = config.get_all_as_dict()

    return {
        'r_radius': df.radius * multipliers['r_radiusm'],
        'r_gravity': df.gravity * multipliers['r_gravitym'],
        'r_jump_force': df.jump_force * multipliers['r_jump_forcem'],
        'r_vertical_force': df.vertical_force * multipliers['r_vertical_forcem'],
        'r_lateral_force': df.lateral_force * multipliers['r_lateral_forcem'],
        'r_lateral_friction': df.lateral_friction * multipliers['r_lateral_frictionm'],
        'r_floor_bounce': df.floor_bounce * multipliers['r_floor_bouncem'],
        'r_weight': df.player_weight * multipliers['r_player_weightm'],
        'r_heavy_weight': df.heavy_weight * multipliers['r_heavy_weightm'],
        'r_heavy_force_multiplier': df.heavy_force_multiplier * multipliers['r_heavy_force_multiplierm'],

        'b_radius': df.radius * multipliers['b_radiusm'],
        'b_gravity': df.gravity * multipliers['b_gravitym'],
        'b_jump_force': df.jump_force * multipliers['b_jump_forcem'],
        'b_vertical_force': df.vertical_force * multipliers['b_vertical_forcem'],
        'b_lateral_force': df.lateral_force * multipliers['b_lateral_forcem'],
        'b_lateral_friction': df.lateral_friction * multipliers['b_lateral_frictionm'],
        'b_floor_bounce': df.floor_bounce * multipliers['b_floor_bouncem'],
        'b_weight': df.player_weight * multipliers['b_player_weightm'],
        'b_heavy_weight': df.heavy_weight * multipliers['b_heavy_weightm'],
        'b_heavy_force_multiplier': df.heavy_force_multiplier * multipliers['b_heavy_force_multiplierm'],

        'ball_bounce': df.ball_bounce * multipliers['ball_bouncem'],
        'npc_acceleration': df.npc_acceleration * multipliers['npc_accelerationm'],
        'npc_max_speed': df.npc_max_speed * multipliers['npc_max_speedm'],
        'npc_ball_radius': df.npc_ball_radius * multipliers['npc_ball_radiusm'],
        'npc_weight': df.npc_weight * multipliers['npc_weightm'],
        'num_npc_balls_per_side': int(multipliers['num_npc_balls_per_side'])
    }
