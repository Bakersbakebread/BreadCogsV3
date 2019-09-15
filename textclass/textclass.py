import discord
from redbot.core import Config, commands

import numpy as np
import re
import nltk
from sklearn.datasets import load_files

nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords


class TextClass:
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(
            self, identifier=12343211, force_registration=True
        )
