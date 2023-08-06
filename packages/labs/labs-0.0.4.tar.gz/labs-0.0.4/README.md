# Introduction
Labs helps create and define (config file), execute (scale with Dask) and save (artifacts, results, metadata) 
experiments.
It's main purpose is to execute ML experiments, but can be used for other use cases.

Labs is using Dask delayed lazy API for distributed computation. Additionally, Scikit-Learn is also used in the 
[Searcher] module.

__Disclaimer__: Labs is currently experimental and for my own personal use.

Key concepts:
* __[Experiment Design]__ - a user defined experiment. The [Experiment Design] is being expressed by a func, which will be 
executed by an [Experimenter/s].

* __[Experiment]__ - a combination of hyper parameters to be tested while running [Experiment Design].

* __[Experiment Run]__ - using the [Experiment Configuration] and [Experiment Design], numerous [Experiments] will be 
executed. The [Experiment Run] will output best [Experiment] (best hyper parameters combination).

* __[Experiment Configuration]__ - sets of configurations which will define the [Experiments] to be executed in Experiment 
Run.

* __[LabManager]__ - running all the [Experiments Configurations] as defined in a config file. A [LabManager] can perform 
numerous [Experiment Configuration] and [Experiment Design]

* __[Experimenter]__ - an entity which perform the tuning/experimenting process. 

* __[Searcher]__ - an entity used by an [Experimenter] to create the [Experiments] in Experiment Run. 
Example Searchers: Grid Search, Random Sampling, Bayesian Search (with the great skopt package). The [Searcher] use the 
defined space in [Experiment Configuration].

## 1. Installation process
```shell
pip install labs
```

## 2. Docs
(Documentation is not completed yet)
1. [Quick Start](https://github.com/Brillone/labs/blob/master/Docs/Quick%20Start.md)
2. [Experimenters](https://github.com/Brillone/labs/blob/master/Docs/Experimenters.md)
3. [Searchers](https://github.com/Brillone/labs/blob/master/Docs/Searchers.md)
4. [LabManager](https://github.com/Brillone/labs/blob/master/Docs/LabManager.md)
5. [Live Reporting](https://github.com/Brillone/labs/blob/master/Docs/Live%20Reporting.md)
6. [Configs](https://github.com/Brillone/labs/blob/master/Docs/Configs.md)
7. [Suggested Steps](https://github.com/Brillone/labs/blob/master/Docs/Suggested%20Steps.md)

## 3. Future
Currently, the project is very new and not completed.

The project need more development to support distributed computation options. 
The future plan is to use Dask rich and developed ecosystem, for simple and fast development of distributed computation
options. 

### Future developments:
* pytest testing.
* Flow options - checkpoint saving, time caps, delta improvement and more.
* Docker support.
* Kubernetes support.  
* Experiments Artifact saved in cloud storage options.
* MLFlow interaction.
