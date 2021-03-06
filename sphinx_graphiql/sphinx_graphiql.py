import fett
from docutils import statemachine
from docutils.parsers.rst import Directive
from docutils.utils.error_reporting import ErrorString


class SphinxGraphiQL(Directive):
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {"query": str, "response": str, "endpoint": str, "view_only": str}

    GRAPHIQL_TEMPLATE = '''
.. raw:: html

   <div class="graphiql {{ if view_only }}view-only{{end}}">
   Loading...
   <div class="endpoint">
   {{ endpoint }}
   </div>
   <div class="query">
   {{ query }}
   </div>
   <div class="response">
   {{ response }}
   </div>
   </div>
'''

    def run(self):
        raw_template = fett.Template(self.GRAPHIQL_TEMPLATE)
        try:
            rendered_template = raw_template.render(self.options)
        except Exception as error:
            raise self.severe('Failed to render template: {}'.format(ErrorString(error)))

        rendered_lines = statemachine.string2lines(rendered_template, 4, convert_whitespace=1)

        self.state_machine.insert_input(rendered_lines, '')

        return []

