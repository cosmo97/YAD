# Aldo
**A**utonomous **L**ight **D**rone **O**pen-source

## Requirements
The drone will weight less than 250 grams and have a maximum speed of 19 m/s.

The drone to flight will require the following components:
- Frame
- Flight controller
- A GPS
- Motors
- Propellers
- ESCs
- Comms
- Battery
- Power module

## Design
To simplify the design and reduce weight the required components are merged in 4
subsystems:
- The [Board](./Board/README.md) that will accomodate all eletronics: GPS,
flight controller, ESCs, comms and the power module.
- A [Frame](./Frame/README.md) to sustain produced stress.
- The [Propulsion](./Propulsion/README.md): composed by motors and propellers.
- A [Battery](./Battery/README.md).
