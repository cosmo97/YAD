# First drone name
First of all we need a name for this drone.

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
- The [PCB](./Board/README.md) that will accomodate all eletronics.
- A [supporting frame](./Frame/README.md) to sustain produced stress.
- [Motors and propellers](./Propulsion/README.md).
- A [battery](./Battery/README.md).

## Implementation

## Test
