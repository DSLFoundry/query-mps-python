# query-mps-python
Perform simple queries on .mps files using python without starting MPS

In it's current state it is extremely rudimentary. The use case is to parse out a few fields during a build.
There is currently no awareness of the metamodel, only of the local index in a .mps file.
Therefore even things such as inheritance and interface implementation (e.g. INamedConcept) are not supported.

As the need arises, functions may be added in the future. Contributions are very much appreciated.