from PythonClientAPI.libs.Game import PointUtils
from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.Entities import *
from PythonClientAPI.libs.Game.World import *


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

        """WORLD object passed has the following
        :type tiles: list of (list of TileType)
        :type width: int (map size)
        :type height: int  (map size)
        :type controlPointCores: list of ControlPoint
        :type pickupCores: list of Pickup
        :type enemies: list of EnemyUnit
        """

        """Tiles can be WALL(0) FLOOR(1) or AMBER/BLUE_SPAWN(2)"""

        #each sub array in the gameboard corresponds to a column of the board
        gameboard = world._tiles;
        #for row in gameboard:
        #    print(row);

        #all we need to do is set the next action for friendly units and then pass


        #FRIENDLY Units
        """
             :type position: (int,int)
             :type team: Team
             :type call_sign: CallSign
             :type weaponType: WeaponType
             :type health: int
             :type lastMoveResult: MoveResult
             :type lastShotResult: ShotResult
             :type lastPickupResult: PickupResult
             :type lastShieldActivationResult: ActivateShieldResult
             :type lastShooters: list of EnemyUnit
             :type damageTakenLastTurn: int
             :type world: World
             :type enemies: list of EnemyUnit
             :type friendlies: list of FriendlyUnit
             :type shieldedTurnsRemaining: int
             :type numShields: int
             """

        for friend in friendly_units:
            print (friend.call_sign);
            print (friend.team);
            print(friend.position);

        #perfect information game
        for enenmy in enemy_units:
            print(enemy.call_sign);
            print(enemy.team);
            print(enemy.position);

            #should check enemy loadout
            #if shotgun & can't move, shield -> if going to die even if move,
            #figure out how we want this shit to behave now and look at the buildin methods for seeing if shot in line, etc.


        #self.control_points = controlPointCores
        #self.pickups = [pickup for pickup in pickupCores if not pickup.pickedUp]


        print(enemy_units);
        print(friendly_units);
        pass
