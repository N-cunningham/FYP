import json
from os import listdir
from Utilities import save_as_JSON
import numpy as np
from Utilities import get_sources
import numpy as np

sources = get_sources()

save_as_JSON(sources, "list_of_sources")
