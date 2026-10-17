# Script blocks

A `script` step runs your own code from inside the flow, with variables crossing in and out by name.

```kdl
script <lang> code="..." [inputs="a b"] [outputs="x y"]
```

- `inputs` is a space-separated list of flow variables to expose to the script.
- `outputs` is a space-separated list of variables the script's results bind back to.
- `code` is the script source in a single (escaped) KDL string.
- Values cross the boundary as strings; the flow's variable model has no other types.

```kdl
set a "3"
set b "4"
script js code="let sum = String(Number(a) + Number(b));" inputs="a b" outputs=sum
```

## js

Runs on an embedded JavaScript engine (boa), inside the app, with no network or filesystem access. Each input variable is injected as a global before the code runs, and each output global is read back afterwards. The engine is ES2020-ish; test anything exotic in the Debug panel first.

```kdl
script js code="let t = in1 + '|' + in2; let n = t.length;" inputs="in1 in2" outputs="t n"
```

## python

Runs with `python3` as a subprocess, so it needs Python on PATH. Inputs arrive as environment variables; outputs are read from a JSON object printed on the last stdout line. If the last line is not JSON, the whole stdout goes to the first declared output.

```kdl
script python code="import os,json\nprint(json.dumps({'product': str(int(os.environ['a'])*int(os.environ['b']))}))" inputs="a b" outputs=product
```

## shell

Runs with `sh -c`, same input/output contract as Python: inputs as environment variables, outputs from the last stdout line as JSON, or the whole stdout into the first output.

```kdl
script shell code="echo \"${a}-${b}\"" inputs="a b" outputs=dashed
```

## Failure behavior

A failing script never fails the item. A JS error, a missing interpreter, or a non-zero subprocess exit simply binds no outputs (or partial ones); the flow continues with the previous values. Check your outputs in a `key-check` (`has "sum"`) when a script's success matters.

Two things to keep in mind:

- Scripts run inline in the item's runner, so a long script holds one of the job's bots for its whole duration. There is no script timeout.
- Python and shell scripts run as subprocesses with the engine's privileges, with a clean environment (plus `PATH` and your inputs). Only run configs from sources you trust.
