from PythonClientAPI.libs.Game import PointUtils
from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.Entities import *
from PythonClientAPI.libs.Game.World import *
import random

class PlayerAI:
    def __init__(self):
        pass

    def do_move(self, world, enemy_units, friendly_units):
        """
        This method will get called every turn; Your glorious AI code goes here.

        :param World world: The latest state of the world.
        :param list[EnemyUnit] enemy_units: An array of all 4 units on the enemy team. Their order won't change.
        :param list[FriendlyUnit] friendly_units: An array of all 4 units on your team. Their order won't change.
        """
        control_points = world.control_points
        pickups = world.pickups
        gameboard = world._tiles

        # Pick ups
        # control points
        # mainframes
        # enemies
        # blocked pathing
        # concave/flanking b/c multiple shots = more damage
        # friendly units block shots
        # kill lowest health
        # Weapon type preference depending on map

        for unit in friendly_units:
            print(unit.call_sign)
            # Order enemies by proximity to this unit
            enemies_by_prox = []
            for enemy in enemy_units:
                if enemy.health > 0:
                    enemies_by_prox.append((chebyshev_distance(unit.position, enemy.position), enemy))
            enemies_by_prox = sorted(enemies_by_prox, key=lambda x: x[0])

            # Order friendly units by proximity to this unit
            friendly_by_prox = []
            for friend in friendly_units:
                if friend.call_sign != unit.call_sign:
                    friendly_by_prox.append((chebyshev_distance(unit.position, friend.position), friend))

            # Find control points which are open for capture order by proximity to this unit & Mainframes
            mainframes_by_prox = []
            control_by_prox = []
            for point in control_points:
                if point.controlling_team != unit.team:
                    if point.is_mainframe:
                        mainframes_by_prox.append(point)
                    control_by_prox.append((chebyshev_distance(unit.position, point.position), point))
            control_by_prox = sorted(control_by_prox, key=lambda x: x[0])

            # Pickups by proximity
            pickups_by_prox = []
            repair_kits_by_prox = []
            weapons_by_prox = []
            shields_by_prox = []
            for pickup in pickups:
                if not pickup.pickedUp:
                    pickups_by_prox.append((chebyshev_distance(unit.position,pickup.position), pickup))

            if len(pickups_by_prox):
                pickups_by_prox = sorted(pickups_by_prox, key=lambda x: x[0])
                closest_pickup = pickups_by_prox[0][1];

                for pickup in pickups_by_prox:
                    if pickup[1].pickup_type == PickupType.REPAIR_KIT:
                        repair_kits_by_prox.append(pickup)
                    elif pickup[1].pickup_type == PickupType.SHIELD:
                        shields_by_prox.append(pickup)
                    else:
                        weapons_by_prox.append(pickup)

                if len(repair_kits_by_prox):
                    repair_kits_by_prox = sorted(repair_kits_by_prox, key=lambda x: x[0])
                    closest_repair = repair_kits_by_prox[0][1]

                if len(weapons_by_prox):
                    weapons_by_prox = sorted(weapons_by_prox, key=lambda x: x[0])
                    closest_weapon = weapons_by_prox[0][1]

                if len(shields_by_prox):
                    shields_by_prox = sorted(shields_by_prox, key=lambda x: x[0])
                    closest_shield = shields_by_prox[0][1]

            print(unit.last_action_succeeded)

            # If on a pickup, always pick it up
            if unit.check_pickup_result() == PickupResult.PICK_UP_VALID:
                print("Picking up {} at {}".format(closest_pickup.pickup_type, closest_pickup.position))
                if closest_pickup.pickup_type == PickupType.REPAIR_KIT:
                    if unit.health < 30:
                        unit.pickup_item_at_position()
                        break
                elif closest_pickup.pickup_type != PickupType.REPAIR_KIT:
                    unit.pickup_item_at_position()
                    break

            # Try to grab a weapon upgrade immediately
            if (unit.current_weapon_type == WeaponType.MINI_BLASTER) and len(weapons_by_prox):
                if unit.last_move_result == MoveResult.BLOCKED_BY_ENEMY or \
                                unit.last_move_result == MoveResult.BLOCKED_BY_FRIENDLY:
                    print("Moving in a random direction")
                    valid_directions = []
                    for direction in list(Direction):
                        if unit.check_move_in_direction(direction) == MoveResult.MOVE_VALID:
                            valid_directions.append(direction)
                    unit.move(random.choice(valid_directions))
                print("Moving to pickup at {} w/ type {}".format(closest_weapon.position, closest_weapon.pickup_type))
                unit.move_to_destination(closest_weapon.position)
                continue

            # Activate shield if unit might take damage and is low on health if the unit has one
            if (unit.damage_taken_last_turn > 0) and (unit.health <= 10) and (unit.num_shields > 0):
                unit.activate_shield()
                continue

            # If able to shoot an enemy, do so
            action = False
            for enemy in enemies_by_prox:
                enemy = enemy[1]
                if unit.check_shot_against_enemy(enemy) == ShotResult.CAN_HIT_ENEMY:
                    print("Shooting {} enemy {}".format(enemy.team, enemy.call_sign))
                    unit.shoot_at(enemy)
                    action=True
                    break
            if action:
                continue

            # Move towards a repair kit if health is below a threshold
            if (unit.health <= 20) and len(repair_kits_by_prox):
                if unit.last_move_result == MoveResult.BLOCKED_BY_ENEMY or \
                                unit.last_move_result == MoveResult.BLOCKED_BY_FRIENDLY:
                    print("Moving in a random direction")
                    valid_directions = []
                    for direction in list(Direction):
                        if unit.check_move_in_direction(direction) == MoveResult.MOVE_VALID:
                            valid_directions.append(direction)
                    unit.move(random.choice(valid_directions))
                print("Moving to pickup {} w/ type {}".format(closest_repair.position, closest_repair.pickup_type))
                unit.move_to_destination(closest_repair.position)
                continue

            # Move towards a shield if unit doesn't have one
            if (unit.num_shields < 1) and len(shields_by_prox):
                if unit.last_move_result == MoveResult.BLOCKED_BY_ENEMY or \
                                unit.last_move_result == MoveResult.BLOCKED_BY_FRIENDLY:
                    print("Moving in a random direction")
                    valid_directions = []
                    for direction in list(Direction):
                        if unit.check_move_in_direction(direction) == MoveResult.MOVE_VALID:
                            valid_directions.append(direction)
                    unit.move(random.choice(valid_directions))
                print("Moving to pickup {} w/ type {}".format(closest_shield.position, closest_shield.pickup_type))
                unit.move_to_destination(closest_shield.position)
                continue

            # Advance towards enemy units if no other objectives
            for enemy in enemies_by_prox:
                enemy = enemy[1]
                if unit.last_move_result == MoveResult.BLOCKED_BY_ENEMY or \
                                unit.last_move_result == MoveResult.BLOCKED_BY_FRIENDLY:
                    print("Moving in a random direction")
                    valid_directions = []
                    for direction in list(Direction):
                        if unit.check_move_in_direction(direction) == MoveResult.MOVE_VALID:
                            valid_directions.append(direction)
                    unit.move(random.choice(valid_directions))
                else:
                    print("Moving to enemy position at {}".format(enemy.position))
                    unit.move_to_destination(enemy.position)
                    break
        pass
