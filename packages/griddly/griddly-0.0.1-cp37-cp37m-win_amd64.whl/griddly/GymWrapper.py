import gym
import numpy as np
from gym.envs.registration import register

from griddly import griddly_loader, gd


class GymWrapper(gym.Env):

    def __init__(self, yaml_file, level=0, global_observer_type=gd.ObserverType.SPRITE_2D,
                 player_observer_type=gd.ObserverType.SPRITE_2D, resources_path=None):
        """
        Currently only supporting a single player (player 1 as defined in the environment yaml
        :param yaml_file:
        :param level:
        :param global_observer_type: the render mode for the global renderer
        :param player_observer_type: the render mode for the players
        """

        # Set up multiple render windows so we can see what the AIs see and what the game environment looks like
        self._renderWindow = {}
        if resources_path == None:
            loader = griddly_loader()
        else:
            loader = griddly_loader(resources_path=resources_path)

        game_description = loader.load_game_description(yaml_file)

        self._grid = game_description.load_level(level)

        self._num_actions = self._grid.get_num_actions()
        self._action_mode = self._grid.get_action_mode()

        self._players = []

        self.game = self._grid.create_game(global_observer_type)
        self._players.append(self.game.add_player(f'Player 1', player_observer_type))

        self._num_players = self.game.get_num_players()
        self.game.init()

    def step(self, action):

        if isinstance(action, int):
            action = [action]
        reward, done = self._players[0].step('move', action)
        self._last_observation = np.array(self._players[0].observe(), copy=False)
        return self._last_observation, reward, done, None

    def reset(self):
        self.game.reset()
        self._last_observation = np.array(self._players[0].observe(), copy=False)

        self._grid_width = self._grid.get_width()
        self._grid_height = self._grid.get_height()

        self._observation_shape = self._last_observation.shape
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=self._observation_shape, dtype=np.uint8)

        if self._action_mode == gd.ActionMode.SELECTION:
            self.action_space = gym.spaces.MultiDiscrete([self._grid_width, self._grid_height, self._num_actions])
        elif self._action_mode == gd.ActionMode.DIRECT:
            self.action_space = gym.spaces.MultiDiscrete([self._num_actions])

        return self._last_observation

    def render(self, mode='human', observer='player'):
        observation = self._last_observation
        if observer == 'global':
            observation = np.array(self.game.observe(), copy=False)

        if mode == 'human':
            if self._renderWindow.get(observer) is None:
                from griddly.RenderTools import RenderWindow
                self._renderWindow[observer] = RenderWindow(observation.shape[1], observation.shape[2])
            self._renderWindow[observer].render(observation)
        elif mode == 'rgb_array':
            return np.array(observation, copy=False).swapaxes(0, 2)


    def get_keys_to_action(self):
        keymap = {
            (ord('a'),): 1,
            (ord('w'),): 2,
            (ord('d'),): 3,
            (ord('s'),): 4,
            (ord('e'),): 5
        }

        return keymap


class GymWrapperFactory():

    def build_gym_from_yaml(self, environment_name, yaml_file, global_observer_type=gd.ObserverType.SPRITE_2D,
                            player_observer_type=gd.ObserverType.SPRITE_2D, level=None):
        register(
            id=f'GDY-{environment_name}-v0',
            entry_point='griddly:GymWrapper',
            kwargs={
                'yaml_file': yaml_file,
                'level': level,
                'global_observer_type': global_observer_type,
                'player_observer_type': player_observer_type
            }
        )
