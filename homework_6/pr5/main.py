"""🐧 LIT demo for tabular data using penguin classification.

To run:
  python -m lit_nlp.examples.penguin.demo --port=5432

Then navigate to localhost:5432 to access the demo UI.
"""

from collections.abc import Sequence
import sys
from typing import Optional

from absl import app
from absl import flags
from absl import logging
from lit_nlp import dev_server
from lit_nlp import server_flags
from lit_nlp.api import layout
from lit_nlp.components import minimal_targeted_counterfactuals
from model import CustomModel
from data import CustomDataset
MODEL_PATH = 'https://storage.googleapis.com/what-if-tool-resources/lit-models/penguin.h5'  

FLAGS = flags.FLAGS
FLAGS.set_default('default_layout', 'penguins')
_MODEL_PATH = flags.DEFINE_string('model_path', MODEL_PATH,
                                  'Path to load trained model.')

_MAX_EXAMPLES = flags.DEFINE_integer(
    'max_examples',
    None,
    (
        'Maximum number of examples to load into LIT. '
        'Set --max_examples=200 for a quick start.'
    ),
)

modules = layout.LitModuleName
PENGUIN_LAYOUT = layout.LitCanonicalLayout(
    upper={
        'Main': [
            modules.DiveModule,
            modules.DataTableModule,
            modules.DatapointEditorModule,
        ]
    },
    lower=layout.STANDARD_LAYOUT.lower,
    description='Custom layout for the Palmer Penguins demo.',
)
CUSTOM_LAYOUTS = layout.DEFAULT_LAYOUTS | {'penguins': PENGUIN_LAYOUT}



def get_wsgi_app() -> Optional[dev_server.LitServerType]:
  FLAGS.set_default('server_type', 'external')
  FLAGS.set_default('demo_mode', True)

  unused = flags.FLAGS(sys.argv, known_only=True)
  if unused:
    logging.info('penguin_demo:get_wsgi_app() called with unused args: %s',
                 unused)
  return main([])


def main(argv: Sequence[str]) -> Optional[dev_server.LitServerType]:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  models = {'species classifier': CustomModel(_MODEL_PATH.value)}
  datasets = {'penguins': CustomDataset()}

  if _MAX_EXAMPLES.value is not None:
    for name in datasets:
      logging.info("Dataset: '%s' with %d examples", name, len(datasets[name]))
      datasets[name] = datasets[name].slice[: _MAX_EXAMPLES.value]
      logging.info('  truncated to %d examples', len(datasets[name]))

  generators = {
      'Minimal Targeted Counterfactuals':
          minimal_targeted_counterfactuals.TabularMTC()
  }
  lit_demo = dev_server.Server(
      models,
      datasets,
      generators=generators,
      layouts=CUSTOM_LAYOUTS,
      **server_flags.get_flags())
  return lit_demo.serve()


if __name__ == '__main__':
  app.run(main)