'''
    File name: rlcard_custom/envs/__init__.py
    Author: Arnob Das
    Date created: 18/03/2025
'''
from rlcard.envs.registration import register
from rlcard_custom.envs.twenty_nine import TwentyNineEnv  # Adjust path to your custom env

register(
    env_id='twenty-nine',
    entry_point='rlcard_custom.envs.twenty_nine:TwentyNineEnv'  # Path to your env class
)