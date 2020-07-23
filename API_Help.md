# Making a module
Do not `import Bomb` at the top of the module file. This is because `ModuleManager.py` 
will import the module file, so importing `Bomb` will result in a circular import.

## Model class
1. Inherit from `BaseModule.ModuleModel`.
2. Only element of constructor is reference to controller.
3. Make functions which interface with controller -> view.

## View class
1. Inherit from `BaseModule.ModuleView`.
