# SynaCell

Synapses and cells.

Spiking neural network (SNN) consisted of cells with processing algorithms, connected by synapses with realistic signal transmission properties. The engine that runs the SNN is written in plain C++ with interface in Python, for simplicity and platform mobility.

## Tests

Test scripts are implemented as a module. You can run them by running the following commands from python after installing `synacell` libraray:

```
import synacell.test
synacell.test.run_all()
```
